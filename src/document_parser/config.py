# Path: src/document_parser/config.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

"""Typed configuration loaded from environment variables."""

from __future__ import annotations

from dataclasses import dataclass
import os


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True, slots=True)
class ParserSettings:
    """Runtime settings shared by parser, downloader, and UI."""

    max_file_size_mb: int = 100
    scanned_pdf_threshold: float = 0.70
    scanned_detection_sample_size: int = 5
    pdf_render_dpi: int = 300
    pdf_visualization_scale: float = 2.0
    min_image_width: int = 50
    min_image_height: int = 50
    url_connect_timeout_seconds: float = 5.0
    url_read_timeout_seconds: float = 30.0
    max_redirects: int = 3
    allow_local_path_input_in_ui: bool = False
    allow_private_network_urls: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "ParserSettings":
        """Build settings from environment variables with safe defaults."""
        return cls(
            max_file_size_mb=int(os.getenv("MAX_FILE_SIZE_MB", "100")),
            scanned_pdf_threshold=float(os.getenv("SCANNED_PDF_THRESHOLD", "0.70")),
            scanned_detection_sample_size=int(os.getenv("SCANNED_DETECTION_SAMPLE_SIZE", "5")),
            pdf_render_dpi=int(os.getenv("PDF_RENDER_DPI", "300")),
            pdf_visualization_scale=float(os.getenv("PDF_VISUALIZATION_SCALE", "2.0")),
            min_image_width=int(os.getenv("MIN_IMAGE_WIDTH", "50")),
            min_image_height=int(os.getenv("MIN_IMAGE_HEIGHT", "50")),
            url_connect_timeout_seconds=float(os.getenv("URL_CONNECT_TIMEOUT_SECONDS", "5")),
            url_read_timeout_seconds=float(os.getenv("URL_READ_TIMEOUT_SECONDS", "30")),
            max_redirects=int(os.getenv("MAX_REDIRECTS", "3")),
            allow_local_path_input_in_ui=_env_bool("ALLOW_LOCAL_PATH_INPUT_IN_UI", False),
            allow_private_network_urls=_env_bool("ALLOW_PRIVATE_NETWORK_URLS", False),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024
