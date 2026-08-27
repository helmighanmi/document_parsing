# Path: src/document_parser/security.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

"""Safe external-source ingestion helpers."""

from __future__ import annotations

from contextlib import suppress
import ipaddress
from pathlib import Path
import socket
import tempfile
from urllib.parse import urljoin, urlparse

import requests

from .config import ParserSettings
from .exceptions import FileTooLargeError, SourceSecurityError

_CONTENT_TYPE_SUFFIXES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "text/csv": ".csv",
    "text/plain": ".txt",
    "text/markdown": ".md",
    "text/html": ".html",
}


def _is_public_ip(value: str) -> bool:
    ip = ipaddress.ip_address(value)
    return not (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def validate_public_url(url: str, *, allow_private_networks: bool = False) -> None:
    """Reject unsupported schemes and private/reserved network destinations."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise SourceSecurityError("Only HTTP and HTTPS URLs are supported.")
    if not parsed.hostname:
        raise SourceSecurityError("URL must include a hostname.")
    if parsed.username or parsed.password:
        raise SourceSecurityError("Credentials embedded in URLs are not allowed.")
    if allow_private_networks:
        return

    try:
        addresses = {
            result[4][0]
            for result in socket.getaddrinfo(
                parsed.hostname,
                parsed.port or (443 if parsed.scheme == "https" else 80),
                type=socket.SOCK_STREAM,
            )
        }
    except socket.gaierror as exc:
        raise SourceSecurityError(f"Could not resolve URL hostname: {parsed.hostname}") from exc

    if not addresses or any(not _is_public_ip(address) for address in addresses):
        raise SourceSecurityError("Private, loopback, link-local, and reserved network URLs are blocked.")


def _infer_suffix(url: str, content_type: str | None) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix:
        return suffix
    if content_type:
        media_type = content_type.split(";", 1)[0].strip().lower()
        return _CONTENT_TYPE_SUFFIXES.get(media_type, ".bin")
    return ".bin"


def download_to_temp(url: str, settings: ParserSettings, session: requests.Session | None = None) -> Path:
    """Download a public URL with redirect validation and a strict byte limit."""
    client = session or requests.Session()
    current_url = url
    response: requests.Response | None = None

    for redirect_count in range(settings.max_redirects + 1):
        validate_public_url(current_url, allow_private_networks=settings.allow_private_network_urls)
        response = client.get(
            current_url,
            stream=True,
            allow_redirects=False,
            timeout=(settings.url_connect_timeout_seconds, settings.url_read_timeout_seconds),
            headers={"User-Agent": "document-parser/2.0"},
        )

        if response.is_redirect or response.is_permanent_redirect:
            location = response.headers.get("Location")
            response.close()
            if not location:
                raise SourceSecurityError("Redirect response did not include a Location header.")
            if redirect_count >= settings.max_redirects:
                raise SourceSecurityError("URL exceeded the configured redirect limit.")
            current_url = urljoin(current_url, location)
            continue
        break

    if response is None:
        raise SourceSecurityError("URL download could not be started.")

    try:
        response.raise_for_status()
        validate_public_url(response.url or current_url, allow_private_networks=settings.allow_private_network_urls)

        content_length = response.headers.get("Content-Length")
        if content_length:
            try:
                declared_size = int(content_length)
            except ValueError:
                declared_size = None
            if declared_size is not None and declared_size > settings.max_file_size_bytes:
                raise FileTooLargeError(
                    f"Remote file exceeds the {settings.max_file_size_mb} MB configured limit."
                )

        suffix = _infer_suffix(response.url or current_url, response.headers.get("Content-Type"))
        fd, temp_name = tempfile.mkstemp(prefix="document_parser_", suffix=suffix)
        path = Path(temp_name)
        written = 0
        try:
            with open(fd, "wb", closefd=True) as handle:
                for chunk in response.iter_content(chunk_size=64 * 1024):
                    if not chunk:
                        continue
                    written += len(chunk)
                    if written > settings.max_file_size_bytes:
                        raise FileTooLargeError(
                            f"Remote file exceeds the {settings.max_file_size_mb} MB configured limit."
                        )
                    handle.write(chunk)
        except Exception:
            with suppress(FileNotFoundError):
                path.unlink()
            raise
        return path
    finally:
        response.close()
