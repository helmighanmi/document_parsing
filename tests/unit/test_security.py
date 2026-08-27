# Path: tests/unit/test_security.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

import socket

import pytest

from document_parser.exceptions import SourceSecurityError
from document_parser.security import validate_public_url


def test_rejects_non_http_scheme() -> None:
    with pytest.raises(SourceSecurityError):
        validate_public_url("file:///etc/passwd")


def test_rejects_embedded_credentials() -> None:
    with pytest.raises(SourceSecurityError):
        validate_public_url("https://user:password@example.com/file.pdf")


def test_rejects_private_network_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *args, **kwargs: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 443))],
    )
    with pytest.raises(SourceSecurityError):
        validate_public_url("https://example.test/document.pdf")


def test_allows_public_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *args, **kwargs: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))],
    )
    validate_public_url("https://example.test/document.pdf")
