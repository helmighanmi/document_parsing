# Path: src/document_parser/visualizer.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

"""PDF visualization helpers kept independent from the Streamlit UI."""

from __future__ import annotations

import io
import logging
from typing import Any

from PIL import Image, ImageDraw

logger = logging.getLogger(__name__)


class DocumentVisualizer:
    """Render PDF pages and overlay parser bounding boxes."""

    def __init__(self) -> None:
        self.text_color = (0, 0, 255, 100)
        self.image_color = (255, 0, 0, 100)
        self.line_width = 2

    def draw_bboxes(
        self,
        pdf_path: str,
        page_num: int,
        bboxes: list[dict[str, Any]],
        scale: float = 2.0,
    ) -> Image.Image | None:
        if page_num < 0 or scale <= 0:
            raise ValueError("page_num must be non-negative and scale must be positive")
        try:
            import fitz

            with fitz.open(pdf_path) as document:
                if page_num >= len(document):
                    logger.error("Page %s is out of range", page_num)
                    return None
                page = document[page_num]
                pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale))

            image = Image.open(io.BytesIO(pixmap.tobytes("png"))).convert("RGBA")
            overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)

            for item in bboxes:
                bbox = item.get("bbox", [])
                if len(bbox) != 4:
                    continue
                x0, y0, x1, y1 = (float(value) * scale for value in bbox)
                color = self.image_color if item.get("type") == "image" else self.text_color
                draw.rectangle([(x0, y0), (x1, y1)], outline=color, fill=color, width=self.line_width)

            return Image.alpha_composite(image, overlay).convert("RGB")
        except Exception:
            logger.exception("Failed to draw PDF bounding boxes")
            return None

    def create_visualization_grid(
        self,
        pdf_path: str,
        pages: list[int],
        bboxes_per_page: dict[int, list[dict[str, Any]]],
        cols: int = 2,
    ) -> Image.Image | None:
        if cols <= 0:
            raise ValueError("cols must be greater than zero")
        rendered = [
            image
            for page_num in pages
            if (image := self.draw_bboxes(pdf_path, page_num, bboxes_per_page.get(page_num, []))) is not None
        ]
        if not rendered:
            return None

        rows = (len(rendered) + cols - 1) // cols
        width = max(image.width for image in rendered)
        height = max(image.height for image in rendered)
        grid = Image.new("RGB", (width * cols, height * rows), "white")
        for index, image in enumerate(rendered):
            grid.paste(image, ((index % cols) * width, (index // cols) * height))
        return grid
