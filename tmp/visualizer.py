from typing import List, Dict, Any, Optional
import logging
from PIL import Image, ImageDraw
import io

logger = logging.getLogger(__name__)


class DocumentVisualizer:
    """Visualize document parsing results with bounding boxes."""
    
    def __init__(self):
        """Initialize visualizer."""
        self.text_color = (0, 0, 255, 100)  # Blue with transparency
        self.image_color = (255, 0, 0, 100)  # Red with transparency
        self.line_width = 2
    
    def draw_bboxes(
        self,
        pdf_path: str,
        page_num: int,
        bboxes: List[Dict[str, Any]],
        scale: float = 2.0
    ) -> Optional[Image.Image]:
        """
        Draw bounding boxes on PDF page.
        
        Args:
            pdf_path: Path to PDF file
            page_num: Page number (0-indexed)
            bboxes: List of bounding box dictionaries
            scale: Scale factor for rendering
            
        Returns:
            PIL Image with drawn bounding boxes
        """
        try:
            import fitz
            
            # Open PDF
            doc = fitz.open(pdf_path)
            
            if page_num >= len(doc):
                logger.error(f"Page {page_num} out of range")
                return None
            
            page = doc[page_num]
            
            # Render page to image
            mat = fitz.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # Create RGBA version for transparency
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create overlay for semi-transparent boxes
            overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Draw bounding boxes
            for bbox_data in bboxes:
                bbox_type = bbox_data.get('type', 'text')
                bbox = bbox_data.get('bbox', [])
                
                if len(bbox) != 4:
                    continue
                
                # Scale bounding box coordinates
                x0, y0, x1, y1 = bbox
                x0 *= scale
                y0 *= scale
                x1 *= scale
                y1 *= scale
                
                # Choose color based on type
                color = self.image_color if bbox_type == 'image' else self.text_color
                
                # Draw filled rectangle
                draw.rectangle(
                    [(x0, y0), (x1, y1)],
                    outline=color,
                    fill=color,
                    width=self.line_width
                )
            
            # Composite overlay on original image
            img = Image.alpha_composite(img, overlay)
            
            # Convert back to RGB for display
            img = img.convert('RGB')
            
            doc.close()
            
            return img
            
        except Exception as e:
            logger.exception(f"Error drawing bounding boxes: {e}")
            return None
    
    def create_visualization_grid(
        self,
        pdf_path: str,
        pages: List[int],
        bboxes_per_page: Dict[int, List[Dict[str, Any]]],
        cols: int = 2
    ) -> Optional[Image.Image]:
        """
        Create a grid visualization of multiple pages.
        
        Args:
            pdf_path: Path to PDF file
            pages: List of page numbers to visualize
            bboxes_per_page: Dictionary mapping page numbers to bboxes
            cols: Number of columns in grid
            
        Returns:
            PIL Image with grid of visualizations
        """
        try:
            images = []
            
            for page_num in pages:
                bboxes = bboxes_per_page.get(page_num, [])
                img = self.draw_bboxes(pdf_path, page_num, bboxes)
                if img:
                    images.append(img)
            
            if not images:
                return None
            
            # Calculate grid dimensions
            rows = (len(images) + cols - 1) // cols
            
            # Get max dimensions
            max_width = max(img.width for img in images)
            max_height = max(img.height for img in images)
            
            # Create grid image
            grid_width = max_width * cols
            grid_height = max_height * rows
            grid = Image.new('RGB', (grid_width, grid_height), 'white')
            
            # Paste images into grid
            for idx, img in enumerate(images):
                row = idx // cols
                col = idx % cols
                x = col * max_width
                y = row * max_height
                grid.paste(img, (x, y))
            
            return grid
            
        except Exception as e:
            logger.exception(f"Error creating visualization grid: {e}")
            return None
    
    def visualize_text_blocks(
        self,
        pdf_path: str,
        page_num: int,
        blocks: List[Dict[str, Any]],
        show_text: bool = True
    ) -> Optional[Image.Image]:
        """
        Visualize text blocks with optional text overlay.
        
        Args:
            pdf_path: Path to PDF file
            page_num: Page number (0-indexed)
            blocks: List of text block dictionaries
            show_text: Whether to overlay text content
            
        Returns:
            PIL Image with text block visualization
        """
        try:
            import fitz
            from PIL import ImageFont
            
            doc = fitz.open(pdf_path)
            page = doc[page_num]
            
            # Render page
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data)).convert('RGB')
            
            draw = ImageDraw.Draw(img)
            
            # Try to load a font
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            except:
                font = ImageFont.load_default()
            
            for block in blocks:
                bbox = block.get('bbox', [])
                if len(bbox) != 4:
                    continue
                
                x0, y0, x1, y1 = [coord * 2 for coord in bbox]
                
                # Draw bounding box
                draw.rectangle(
                    [(x0, y0), (x1, y1)],
                    outline='blue',
                    width=2
                )
                
                # Optionally draw text
                if show_text and block.get('text'):
                    text = block['text'][:50]  # Truncate long text
                    draw.text((x0 + 2, y0 + 2), text, fill='red', font=font)
            
            doc.close()
            
            return img
            
        except Exception as e:
            logger.exception(f"Error visualizing text blocks: {e}")
            return None
