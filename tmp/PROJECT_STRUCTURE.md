# 📁 Project Structure

Complete overview of the Document Parser API codebase.

## File Organization

```
document-parser-api/
│
├── app.py                      # Main Streamlit application
├── parsers.py                  # Document parsing logic
├── visualizer.py               # Bounding box visualization
├── config.py                   # Configuration settings
│
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container definition
├── docker-compose.yml          # Docker Compose configuration
├── .gitignore                  # Git ignore patterns
│
├── README.md                   # Full documentation
├── QUICKSTART.md              # Quick start guide
├── PROJECT_STRUCTURE.md       # This file
│
├── test_installation.py        # Installation verification script
├── examples.py                 # Usage examples
│
└── sample_documents/           # Sample files for testing
    ├── sample.txt
    └── sample.md
```

## Core Components

### 1. app.py - Streamlit Interface

**Purpose**: Web-based user interface for document parsing.

**Key Features**:
- File upload (drag & drop)
- File path input
- URL download
- Parser selection
- View mode switching
- Bounding box visualization

**Main Functions**:
```python
main()                          # Entry point
# Sidebar configuration
# Input method selection
# Parser options
# Results display
```

**UI Components**:
- Sidebar: Configuration panel
- Main area: Document processing and results
- Info panel: Supported formats and tools

### 2. parsers.py - Document Parser

**Purpose**: Core parsing logic for all document types.

**Class**: `DocumentParser`

**Key Methods**:
```python
__init__(tool, detect_scanned, extract_images, ocr_lang)
parse(document_path)            # Main parsing method
_auto_select_parser()           # Automatic tool selection
_is_scanned_pdf()              # Detect scanned PDFs
_analyze_pdf()                 # Analyze PDF structure

# Parser implementations
_parse_with_pymupdf()          # PyMuPDF parser
_parse_with_pymupdf4llm()      # PyMuPDF4LLM parser
_parse_with_pdfplumber()       # pdfplumber parser
_parse_with_tesseract()        # Tesseract OCR
_parse_with_easyocr()          # EasyOCR
_parse_with_docling()          # Docling parser
_parse_with_unstructured()     # Unstructured parser
_parse_word()                  # Word documents
_parse_powerpoint()            # PowerPoint presentations
_parse_excel()                 # Excel spreadsheets
_parse_text()                  # Text files
```

**Output Format**:
```python
{
    'tool_used': str,           # Parser that was used
    'content': str,             # Full markdown content
    'pages': [                  # Page-by-page content
        {
            'page_number': int,
            'content': str,
            'bboxes': [...],    # Optional bounding boxes
            'metadata': {...}
        }
    ],
    'images': [...],            # Extracted images
    'metadata': {...},          # Document metadata
    'pdf_analysis': {...}       # PDF-specific analysis
}
```

### 3. visualizer.py - Bounding Box Visualizer

**Purpose**: Visualize document layout with bounding boxes.

**Class**: `DocumentVisualizer`

**Key Methods**:
```python
__init__()
draw_bboxes(pdf_path, page_num, bboxes, scale)
create_visualization_grid(pdf_path, pages, bboxes_per_page)
visualize_text_blocks(pdf_path, page_num, blocks)
```

**Color Coding**:
- Blue: Text blocks
- Red: Images
- Green: Tables (future feature)

### 4. config.py - Configuration

**Purpose**: Centralized configuration management.

**Categories**:
- Parser settings
- PDF processing
- OCR configuration
- Image extraction
- Visualization
- Performance
- UI settings
- Logging

**Example Usage**:
```python
from config import DEFAULT_OCR_LANGUAGE, PDF_RENDER_DPI

# Use in parsers.py
ocr_lang = config.DEFAULT_OCR_LANGUAGE
dpi = config.PDF_RENDER_DPI
```

## Supporting Files

### test_installation.py

**Purpose**: Verify installation and dependencies.

**Tests**:
- Required library imports
- Optional library imports
- System dependencies (tesseract, poppler)
- Parser initialization
- Visualizer initialization
- Sample document creation

**Usage**:
```bash
python test_installation.py
```

### examples.py

**Purpose**: Demonstrate API usage patterns.

**Examples**:
1. Basic parsing with auto-detection
2. PDF with document analysis
3. Using specific tools
4. OCR for scanned PDFs
5. Table extraction
6. Office documents
7. Batch processing
8. Image extraction
9. URL parsing
10. Bounding box visualization

**Usage**:
```bash
python examples.py
```

## Data Flow

### 1. Document Input Flow

```
User Input (File/Path/URL)
    ↓
app.py (Streamlit Interface)
    ↓
DocumentParser.parse()
    ↓
File Type Detection
    ↓
Tool Selection (Auto or Manual)
    ↓
Appropriate Parser Method
    ↓
Results Dictionary
    ↓
Display in UI
```

### 2. PDF Parsing Flow

```
PDF File
    ↓
Scanned Detection (if enabled)
    ↓
PDF Analysis (Digital/Scanned/Hybrid)
    ↓
Parser Selection
    ├── Digital → PyMuPDF4LLM
    ├── Scanned → Tesseract OCR
    └── Hybrid → PyMuPDF + OCR
    ↓
Text Extraction
    ↓
Bounding Box Extraction (optional)
    ↓
Image Extraction (optional)
    ↓
Results
```

### 3. Visualization Flow

```
Parsed Results with Bboxes
    ↓
DocumentVisualizer.draw_bboxes()
    ↓
Render PDF Page to Image
    ↓
Draw Bounding Boxes
    ├── Text → Blue
    └── Images → Red
    ↓
Composite Image
    ↓
Display in Streamlit
```

## Extension Points

### Adding a New Parser

1. **Add to parsers.py**:
```python
def _parse_with_newparser(self, doc_path: str) -> Dict[str, Any]:
    """Parse using new parser."""
    # Import library
    import newparser
    
    # Parse document
    content = newparser.parse(doc_path)
    
    # Return standard format
    return {
        'tool_used': 'NewParser',
        'content': content,
        'pages': [],
        'images': [],
        'metadata': {}
    }
```

2. **Add to method map**:
```python
def _get_parser_method(self, tool_name: str) -> callable:
    method_map = {
        # ... existing tools ...
        'newparser': self._parse_with_newparser,
    }
```

3. **Add to UI** (app.py):
```python
available_tools = [
    # ... existing tools ...
    "NewParser",
]
```

### Adding a New Document Type

1. **Update SUPPORTED_EXTENSIONS** in parsers.py
2. **Implement parser method**
3. **Update auto-selection logic**
4. **Add to UI documentation**

### Adding Visualization Features

1. **Add method to visualizer.py**
2. **Add color configuration to config.py**
3. **Add UI controls in app.py**

## Dependencies

### Core (Required)
- streamlit: Web interface
- PyMuPDF: PDF parsing
- Pillow: Image processing
- requests: URL downloads

### Document Formats
- python-docx: Word documents
- python-pptx: PowerPoint
- openpyxl: Excel spreadsheets

### Advanced PDF
- pymupdf4llm: LLM-optimized parsing
- pdfplumber: Table extraction

### OCR (Optional)
- pytesseract: Tesseract wrapper
- pdf2image: PDF to image conversion
- easyocr: Modern OCR

### Advanced Parsing (Optional)
- docling: Advanced document understanding
- unstructured: Multi-format parsing

## Configuration

### Environment Variables

Set in docker-compose.yml or .env:
```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Runtime Configuration

Modify config.py:
```python
# Parser settings
DEFAULT_TOOL = None
SCANNED_PDF_THRESHOLD = 0.7

# Performance
MAX_PARALLEL_PAGES = 4
ENABLE_CACHING = True

# UI
PAGE_LAYOUT = "wide"
```

## Deployment Options

### 1. Local Development
```bash
streamlit run app.py
```

### 2. Docker
```bash
docker build -t document-parser .
docker run -p 8501:8501 document-parser
```

### 3. Docker Compose
```bash
docker-compose up -d
```

### 4. Cloud Deployment
- Streamlit Cloud
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances

## Testing Strategy

### Unit Tests (Future)
```python
tests/
├── test_parsers.py
├── test_visualizer.py
└── test_integration.py
```

### Manual Testing
1. Run `test_installation.py`
2. Run `examples.py`
3. Test in Streamlit UI
4. Try different document types
5. Test edge cases

## Performance Considerations

### Optimization Strategies
1. **Caching**: Results caching for repeated documents
2. **Parallel Processing**: Multi-page PDFs
3. **Lazy Loading**: On-demand image extraction
4. **Streaming**: Large file handling

### Resource Usage
- Memory: ~100-500MB per document
- CPU: Varies by parser and document size
- Disk: Temporary files for URL downloads

## Security Considerations

### Input Validation
- File size limits (config.MAX_FILE_SIZE_MB)
- File type validation
- URL whitelist (future feature)

### Temporary File Handling
- Auto-cleanup of temp files
- Secure file permissions
- Isolated processing

## Maintenance

### Regular Updates
- Update requirements.txt
- Test with new library versions
- Update documentation
- Add new parsers as available

### Monitoring
- Log parsing errors
- Track tool usage statistics
- Monitor performance metrics

## Contributing Guidelines

### Code Style
- PEP 8 compliance
- Type hints where appropriate
- Docstrings for all functions
- Meaningful variable names

### Documentation
- Update README.md
- Add examples
- Comment complex logic
- Update PROJECT_STRUCTURE.md

## Roadmap

### Planned Features
- [ ] Batch processing UI
- [ ] Custom parser plugins
- [ ] Advanced table extraction
- [ ] Document comparison
- [ ] Export to multiple formats
- [ ] API endpoints (REST)
- [ ] Authentication system
- [ ] Cloud storage integration

### Performance Improvements
- [ ] Parallel page processing
- [ ] Result caching
- [ ] Incremental parsing
- [ ] GPU acceleration for OCR

---

Last Updated: 2024
Version: 1.0.0
