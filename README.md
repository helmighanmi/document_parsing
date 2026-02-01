# 📄 Universal Document Parser API

A powerful document parsing API with Streamlit demo interface that supports multiple file formats and parsing engines.

## 🌟 Features

- **Multi-format Support**: PDF, Word, PowerPoint, Excel, Text files, HTML
- **Multiple Parsing Engines**:
  - PyMuPDF (Fast PDF parsing)
  - PyMuPDF4LLM (LLM-optimized markdown output)
  - pdfplumber (Excellent for tables)
  - Docling (Advanced document understanding)
  - Unstructured (Multi-format parsing)
  - python-docx, python-pptx, openpyxl (Office formats)
  - Tesseract OCR, EasyOCR (Scanned documents)

- **Smart Features**:
  - Auto-detection of best parsing tool
  - Scanned/hybrid PDF detection
  - Bounding box visualization
  - Page-by-page navigation
  - Image extraction
  - Markdown export
  - Table extraction

## 🚀 Installation

### Prerequisites

For OCR functionality, install system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils

# macOS
brew install tesseract poppler
```

### Python Dependencies

```bash
# Basic installation
pip install -r requirements.txt

# Or install core dependencies only
pip install streamlit PyMuPDF pymupdf4llm pdfplumber python-docx python-pptx openpyxl Pillow requests
```

### Optional Dependencies

For advanced features:

```bash
# OCR support
pip install pytesseract pdf2image easyocr

# Advanced parsing (requires additional system dependencies)
pip install docling unstructured
```

## 💻 Usage

### Run the Streamlit Demo

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the API Programmatically

```python
from parsers import DocumentParser

# Initialize parser
parser = DocumentParser(
    tool=None,  # Auto-select best tool
    detect_scanned=True,
    extract_images=True,
    ocr_lang='eng'
)

# Parse a document
results = parser.parse('path/to/document.pdf')

# Access results
print(results['content'])  # Markdown content
print(results['metadata'])  # Document metadata
print(results['pages'])     # Page-by-page content
```

### Specify a Specific Tool

```python
# Use PyMuPDF4LLM specifically
parser = DocumentParser(tool='pymupdf4llm')
results = parser.parse('document.pdf')

# Use Tesseract OCR for scanned PDFs
parser = DocumentParser(tool='tesseract_ocr', ocr_lang='eng')
results = parser.parse('scanned.pdf')

# Use pdfplumber for table-heavy documents
parser = DocumentParser(tool='pdfplumber')
results = parser.parse('tables.pdf')
```

## 📖 Interface Guide

### Input Methods

1. **Upload File**: Drag and drop or browse for files
2. **File Path**: Enter local file path
3. **URL**: Enter URL to download and parse

### Parser Selection

- **Auto (Recommended)**: Automatically selects best parser based on document type
- **Manual Selection**: Choose specific parser for your use case

### Display Options

1. **Markdown View**: Full document in markdown format
2. **Page-by-Page View**: Navigate through individual pages
3. **Bounding Box Visualization**: 
   - Blue boxes: Text blocks
   - Red boxes: Images

### PDF Analysis

For PDFs, the system automatically detects:
- Document Type: Digital, Scanned, or Hybrid
- Pages with/without text
- Scanned pages requiring OCR
- Hybrid pages with both text and images

## 🔧 Supported File Types

| Format | Extensions | Best Parser |
|--------|-----------|-------------|
| PDF (Digital) | `.pdf` | PyMuPDF4LLM |
| PDF (Scanned) | `.pdf` | Tesseract OCR / EasyOCR |
| PDF (Tables) | `.pdf` | pdfplumber |
| Word | `.docx`, `.doc` | python-docx |
| PowerPoint | `.pptx`, `.ppt` | python-pptx |
| Excel | `.xlsx`, `.xls` | openpyxl |
| Text | `.txt`, `.md`, `.html` | Built-in |

## 🎯 Use Cases

### 1. Academic Paper Analysis
```python
parser = DocumentParser(tool='pymupdf4llm')
results = parser.parse('research_paper.pdf')
markdown = results['content']  # LLM-ready markdown
```

### 2. Invoice Processing
```python
parser = DocumentParser(tool='pdfplumber')
results = parser.parse('invoice.pdf')
# Tables are extracted and formatted in markdown
```

### 3. Scanned Document OCR
```python
parser = DocumentParser(
    tool='tesseract_ocr',
    ocr_lang='eng',
    detect_scanned=True
)
results = parser.parse('scanned_contract.pdf')
```

### 4. Multi-format Documentation
```python
parser = DocumentParser()  # Auto-detect
for doc in ['report.pdf', 'data.xlsx', 'slides.pptx']:
    results = parser.parse(doc)
    print(f"{doc}: {results['tool_used']}")
```

## 🎨 Visualization Examples

The bounding box visualization helps you understand:
- Document layout and structure
- Image placement
- Text block organization
- Table detection

Perfect for:
- Document analysis
- Layout understanding
- Debugging parsing issues
- Quality control

## 📊 Output Format

```python
{
    'tool_used': 'PyMuPDF4LLM',
    'content': '# Document Title\n\n...',  # Full markdown
    'pages': [
        {
            'page_number': 1,
            'content': 'Page content...',
            'bboxes': [...],  # Optional
            'metadata': {...}
        }
    ],
    'images': [
        {
            'page': 1,
            'image': b'...',
            'ext': 'png'
        }
    ],
    'metadata': {
        'page_count': 10,
        ...
    },
    'pdf_analysis': {  # For PDFs only
        'type': 'Digital',
        'total_pages': 10,
        'scanned_pages': [],
        'hybrid_pages': [5, 6]
    }
}
```

## 🔍 Tool Selection Logic

The auto-selection algorithm:

1. **Check file type** (PDF, Word, Excel, etc.)
2. **For PDFs**:
   - Analyze first few pages
   - Detect if scanned (>70% pages without text)
   - Choose OCR if scanned, otherwise PyMuPDF4LLM
3. **For other formats**:
   - Use format-specific parser (python-docx, python-pptx, etc.)

## 🌐 Free Tools (No GPU/Payment Required)

All included tools are free and open-source:
- ✅ PyMuPDF - MIT License
- ✅ pdfplumber - MIT License
- ✅ python-docx - MIT License
- ✅ python-pptx - MIT License
- ✅ openpyxl - MIT License
- ✅ Tesseract OCR - Apache 2.0 License
- ✅ EasyOCR - Apache 2.0 License (CPU mode available)

Optional tools:
- Docling - Free but may require more resources
- Unstructured - Free with some features requiring API

## 🐛 Troubleshooting

### OCR Not Working
```bash
# Install Tesseract
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# For other languages
sudo apt-get install tesseract-ocr-fra  # French
sudo apt-get install tesseract-ocr-deu  # German
```

### PDF to Image Conversion Fails
```bash
# Install Poppler
sudo apt-get install poppler-utils
```

### Import Errors
```bash
# Install missing packages
pip install <package_name>
```

## 📝 Contributing

This is a learning project. Feel free to:
- Add new parsing engines
- Improve visualization features
- Add support for more formats
- Enhance OCR accuracy

## 🎓 Learning Resources

Great for students learning:
- Document processing
- Computer vision (OCR, layout detection)
- Python libraries (Streamlit, PIL, PyMuPDF)
- API design
- Multi-tool integration

## 📄 License

This project is for educational purposes. Individual libraries have their own licenses (see requirements.txt).

## 🔗 Related Tools

- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [pdfplumber](https://github.com/jsvine/pdfplumber)

## 💡 Tips for Job Applications

When adding to your portfolio:
1. Demo the live application
2. Explain tool selection logic
3. Show sample outputs for different document types
4. Discuss challenges (OCR accuracy, table detection)
5. Highlight extensibility and clean code structure

Good luck with your job search! 🚀
