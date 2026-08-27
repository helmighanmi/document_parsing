# 🚀 Quick Start Guide

Get started with the Document Parser API in 5 minutes!

## Step 1: Install Dependencies

```bash
# Clone or download the project
cd document-parser-api

# Install Python dependencies
pip install streamlit PyMuPDF pymupdf4llm pdfplumber python-docx python-pptx openpyxl Pillow requests

# (Optional) Install OCR support
sudo apt-get install tesseract-ocr poppler-utils  # Ubuntu/Debian
pip install pytesseract pdf2image
```

## Step 2: Test Installation

```bash
# Run the test script
python test_installation.py
```

You should see ✅ for all core components.

## Step 3: Run the Demo

```bash
# Start Streamlit app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Step 4: Parse Your First Document

### Option A: Using the Web Interface

1. **Upload a file** or enter a file path
2. **Choose a parser** (or use Auto)
3. **Click "Parse Document"**
4. **View results** in Markdown, Page-by-Page, or Visualization mode

### Option B: Using Python API

Create a file `test_parse.py`:

```python
from parsers import DocumentParser

# Initialize parser
parser = DocumentParser()

# Parse a document
results = parser.parse('sample_documents/sample.txt')

# Print results
print("Tool used:", results['tool_used'])
print("Content preview:", results['content'][:200])
print("Total pages:", len(results['pages']))
```

Run it:
```bash
python test_parse.py
```

## Common Use Cases

### 1. Parse a PDF with Auto-Detection

```python
from parsers import DocumentParser

parser = DocumentParser()
results = parser.parse('document.pdf')
print(results['content'])
```

### 2. Parse a Scanned PDF with OCR

```python
parser = DocumentParser(
    tool='tesseract_ocr',
    ocr_lang='eng'
)
results = parser.parse('scanned.pdf')
```

### 3. Extract Tables from PDF

```python
parser = DocumentParser(tool='pdfplumber')
results = parser.parse('tables.pdf')
# Tables are included in markdown format
```

### 4. Parse Multiple Document Types

```python
documents = [
    'report.pdf',
    'data.xlsx',
    'presentation.pptx',
    'notes.docx'
]

parser = DocumentParser()  # Auto-detect

for doc in documents:
    results = parser.parse(doc)
    print(f"{doc}: Parsed with {results['tool_used']}")
```

## Web Interface Features

### 📥 Input Options
- **Upload File**: Drag & drop any supported file
- **File Path**: Enter path to local file
- **URL**: Download and parse from URL

### 🔧 Parser Options
- **Auto**: Smart selection based on file type
- **Manual**: Choose specific parser
- **OCR Language**: Select language for scanned documents

### 📊 View Modes
1. **Markdown View**: Full document as markdown
2. **Page-by-Page**: Navigate individual pages
3. **Bounding Box**: Visualize text (blue) and images (red)

### 📋 Additional Features
- PDF type detection (Digital/Scanned/Hybrid)
- Metadata display
- Image extraction
- Table formatting

## Tips for Best Results

### For Regular PDFs
✅ Use `PyMuPDF4LLM` - produces clean markdown
✅ Enable scanned detection

### For Scanned Documents
✅ Use `Tesseract OCR` or `EasyOCR`
✅ Select correct language
✅ Use high DPI (300+)

### For Tables and Forms
✅ Use `pdfplumber` - best table extraction
✅ Review in Page-by-Page mode

### For Office Documents
✅ Auto mode works great
✅ Tables are preserved in Excel/Word

## Troubleshooting

### Import Errors
```bash
pip install <missing_package>
```

### OCR Not Working
```bash
# Install Tesseract
sudo apt-get install tesseract-ocr

# Verify installation
tesseract --version
```

### PDF to Image Issues
```bash
# Install Poppler
sudo apt-get install poppler-utils

# Verify installation
pdftoppm -v
```

### Streamlit Connection Error
```bash
# Try a different port
streamlit run app.py --server.port 8502
```

## Next Steps

📚 Read the full [README.md](README.md) for detailed documentation

🔧 Customize [config.py](config.py) for your needs

🧪 Explore the code in [parsers.py](parsers.py) and [visualizer.py](visualizer.py)

🎨 Try different parsers and compare results

## Getting Help

- Check the README.md for detailed docs
- Run `python test_installation.py` to verify setup
- Review sample documents in `sample_documents/`
- Check logs for error details

## Example Workflow

```bash
# 1. Test installation
python test_installation.py

# 2. Try parsing sample documents
python -c "
from parsers import DocumentParser
parser = DocumentParser()
result = parser.parse('sample_documents/sample.txt')
print(result['content'])
"

# 3. Run the web interface
streamlit run app.py

# 4. Upload your document and experiment!
```

Happy parsing! 🎉
