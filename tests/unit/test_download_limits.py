# Path: tests/unit/test_download_limits.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

import socket

import pytest

from document_parser.config import ParserSettings
from document_parser.exceptions import FileTooLargeError
from document_parser.security import download_to_temp


class FakeResponse:
    is_redirect = False
    is_permanent_redirect = False
    url = "https://example.test/large.pdf"
    headers = {"Content-Length": "200", "Content-Type": "application/pdf"}

    def raise_for_status(self) -> None:
        return None

    def iter_content(self, chunk_size: int):
        yield b"x" * 200

    def close(self) -> None:
        return None


class FakeSession:
    def get(self, *args, **kwargs):
        return FakeResponse()


def test_download_rejects_content_length_over_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *args, **kwargs: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))],
    )
    settings = ParserSettings(max_file_size_mb=0)
    with pytest.raises(FileTooLargeError):
        download_to_temp("https://example.test/large.pdf", settings, session=FakeSession())
