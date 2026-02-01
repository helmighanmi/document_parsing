"""
Configuration file for Document Parser API.
Customize these settings based on your needs.
"""

# ===========================
# Parser Configuration
# ===========================

# Default parser tool (None for auto-detection)
DEFAULT_TOOL = None

# Supported tools
AVAILABLE_TOOLS = [
    "pymupdf",
    "pymupdf4llm",
    "docling",
    "unstructured",
    "pdfplumber",
    "python-docx",
    "python-pptx",
    "openpyxl",
    "tesseract_ocr",
    "easyocr"
]

# ===========================
# PDF Processing
# ===========================

# Threshold for determining if PDF is scanned (percentage of pages without text)
SCANNED_PDF_THRESHOLD = 0.7

# Number of pages to sample when detecting scanned PDFs
SCANNED_DETECTION_SAMPLE_SIZE = 5

# DPI for rendering PDF pages for OCR
PDF_RENDER_DPI = 300

# Scale factor for PDF page rendering in visualization
PDF_VISUALIZATION_SCALE = 2.0

# ===========================
# OCR Configuration
# ===========================

# Default OCR language
DEFAULT_OCR_LANGUAGE = 'eng'

# Available OCR languages
# Install additional languages: sudo apt-get install tesseract-ocr-<lang>
AVAILABLE_OCR_LANGUAGES = [
    'eng',  # English
    'fra',  # French
    'deu',  # German
    'spa',  # Spanish
    'ita',  # Italian
    'por',  # Portuguese
    'rus',  # Russian
    'chi_sim',  # Chinese Simplified
    'chi_tra',  # Chinese Traditional
    'jpn',  # Japanese
    'kor',  # Korean
    'ara',  # Arabic
]

# Tesseract OCR configuration
TESSERACT_CONFIG = '--psm 3'  # Page segmentation mode

# EasyOCR settings
EASYOCR_GPU = False  # Set to True if GPU is available

# ===========================
# Image Extraction
# ===========================

# Whether to extract images by default
EXTRACT_IMAGES_DEFAULT = False

# Minimum image size to extract (width x height in pixels)
MIN_IMAGE_SIZE = (50, 50)

# Maximum number of images to extract per page
MAX_IMAGES_PER_PAGE = 20

# Supported image formats for extraction
SUPPORTED_IMAGE_FORMATS = ['png', 'jpg', 'jpeg', 'gif', 'bmp']

# ===========================
# Visualization
# ===========================

# Bounding box colors (R, G, B, Alpha)
BBOX_TEXT_COLOR = (0, 0, 255, 100)  # Blue with transparency
BBOX_IMAGE_COLOR = (255, 0, 0, 100)  # Red with transparency
BBOX_TABLE_COLOR = (0, 255, 0, 100)  # Green with transparency

# Bounding box line width
BBOX_LINE_WIDTH = 2

# ===========================
# File Processing
# ===========================

# Maximum file size for upload (in MB)
MAX_FILE_SIZE_MB = 100

# Temporary file cleanup
AUTO_CLEANUP_TEMP_FILES = True

# Supported file extensions by category
SUPPORTED_EXTENSIONS = {
    'pdf': ['.pdf'],
    'word': ['.docx', '.doc'],
    'powerpoint': ['.pptx', '.ppt'],
    'excel': ['.xlsx', '.xls', '.csv'],
    'text': ['.txt', '.md', '.markdown', '.html', '.htm']
}

# ===========================
# Performance
# ===========================

# Maximum number of pages to process in parallel
MAX_PARALLEL_PAGES = 4

# Timeout for URL downloads (seconds)
URL_DOWNLOAD_TIMEOUT = 30

# Cache parsed results
ENABLE_CACHING = True
CACHE_SIZE_MB = 500

# ===========================
# Streamlit UI
# ===========================

# Page title and icon
PAGE_TITLE = "Document Parser API Demo"
PAGE_ICON = "📄"

# Layout
PAGE_LAYOUT = "wide"

# Theme
THEME = {
    'primaryColor': '#1f77b4',
    'backgroundColor': '#ffffff',
    'secondaryBackgroundColor': '#f0f2f6',
    'textColor': '#262730'
}

# ===========================
# Logging
# ===========================

# Logging level
LOG_LEVEL = 'INFO'  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Log file path (None for console only)
LOG_FILE = None

# Log format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# ===========================
# Advanced Settings
# ===========================

# Auto-selection preferences (priority order)
PARSER_PRIORITY = {
    'pdf': ['pymupdf4llm', 'pymupdf', 'pdfplumber'],
    'word': ['python-docx'],
    'powerpoint': ['python-pptx'],
    'excel': ['openpyxl'],
    'text': ['builtin']
}

# Fallback parser if preferred parser fails
ENABLE_FALLBACK = True

# Table extraction settings
TABLE_EXTRACTION = {
    'min_words_vertical': 3,
    'min_words_horizontal': 3,
    'edge_min_length': 3,
    'intersection_tolerance': 3
}

# ===========================
# Development Settings
# ===========================

# Debug mode
DEBUG = False

# Show detailed error messages
SHOW_DETAILED_ERRORS = True

# Enable experimental features
ENABLE_EXPERIMENTAL = False
