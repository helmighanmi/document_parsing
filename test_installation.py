#!/usr/bin/env python3
"""
Test script to verify document parser installation and functionality.
"""

import sys
from pathlib import Path


def test_imports():
    """Test if all required libraries can be imported."""
    print("🔍 Testing imports...")
    
    required = {
        'streamlit': 'Streamlit',
        'fitz': 'PyMuPDF',
        'PIL': 'Pillow',
        'requests': 'requests'
    }
    
    optional = {
        'pymupdf4llm': 'PyMuPDF4LLM',
        'pdfplumber': 'pdfplumber',
        'docx': 'python-docx',
        'pptx': 'python-pptx',
        'openpyxl': 'openpyxl',
        'pytesseract': 'pytesseract (OCR)',
        'pdf2image': 'pdf2image',
        'easyocr': 'EasyOCR'
    }
    
    success = []
    failed = []
    optional_missing = []
    
    # Test required imports
    for module, name in required.items():
        try:
            __import__(module)
            success.append(name)
            print(f"  ✅ {name}")
        except ImportError as e:
            failed.append(name)
            print(f"  ❌ {name} - {e}")
    
    # Test optional imports
    for module, name in optional.items():
        try:
            __import__(module)
            success.append(name)
            print(f"  ✅ {name}")
        except ImportError:
            optional_missing.append(name)
            print(f"  ⚠️  {name} (optional)")
    
    print(f"\n📊 Summary:")
    print(f"  Required: {len(success) - len(optional_missing)}/{len(required)}")
    print(f"  Optional: {len(success) - (len(required) - len(failed))}/{len(optional)}")
    
    if failed:
        print(f"\n❌ Missing required packages: {', '.join(failed)}")
        print("   Install with: pip install " + " ".join(failed))
        return False
    
    if optional_missing:
        print(f"\n⚠️  Missing optional packages: {', '.join(optional_missing)}")
        print("   Install with: pip install " + " ".join([k for k, v in optional.items() if v in optional_missing]))
    
    return True


def test_parser():
    """Test basic parser functionality."""
    print("\n🧪 Testing parser...")
    
    try:
        from parsers import DocumentParser
        
        # Test parser initialization
        parser = DocumentParser()
        print("  ✅ Parser initialization")
        
        # Test auto-selection
        parser._auto_select_parser('pdf', 'test.pdf')
        print("  ✅ Auto-selection logic")
        
        # Test tool selection
        parser._get_parser_method('pymupdf')
        print("  ✅ Tool selection")
        
        return True
    except Exception as e:
        print(f"  ❌ Parser test failed: {e}")
        return False


def test_visualizer():
    """Test visualizer functionality."""
    print("\n🎨 Testing visualizer...")
    
    try:
        from visualizer import DocumentVisualizer
        
        # Test visualizer initialization
        visualizer = DocumentVisualizer()
        print("  ✅ Visualizer initialization")
        
        return True
    except Exception as e:
        print(f"  ❌ Visualizer test failed: {e}")
        return False


def check_system_dependencies():
    """Check for system-level dependencies."""
    print("\n🔧 Checking system dependencies...")
    
    import subprocess
    
    dependencies = {
        'tesseract': 'Tesseract OCR',
        'pdftotext': 'Poppler Utils',
        'pdftoppm': 'Poppler Utils (pdf2image)'
    }
    
    available = []
    missing = []
    
    for cmd, name in dependencies.items():
        try:
            subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                check=True,
                timeout=5
            )
            available.append(name)
            print(f"  ✅ {name}")
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            missing.append(name)
            print(f"  ⚠️  {name} (optional)")
    
    if missing:
        print(f"\n⚠️  Missing optional system dependencies:")
        print("   Ubuntu/Debian: sudo apt-get install tesseract-ocr poppler-utils")
        print("   macOS: brew install tesseract poppler")
    
    return True


def create_sample_documents():
    """Create sample documents for testing."""
    print("\n📝 Creating sample documents...")
    
    try:
        # Create a simple text file
        sample_dir = Path("sample_documents")
        sample_dir.mkdir(exist_ok=True)
        
        # Sample text file
        (sample_dir / "sample.txt").write_text(
            "# Sample Document\n\n"
            "This is a sample text document for testing the parser.\n\n"
            "## Features\n"
            "- Multi-line content\n"
            "- Markdown formatting\n"
            "- Easy to parse\n"
        )
        print("  ✅ Created sample.txt")
        
        # Sample markdown file
        (sample_dir / "sample.md").write_text(
            "# Markdown Document\n\n"
            "This demonstrates **markdown** parsing.\n\n"
            "## Code Example\n"
            "```python\n"
            "print('Hello, World!')\n"
            "```\n"
        )
        print("  ✅ Created sample.md")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed to create samples: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("📄 Document Parser API - Installation Test")
    print("=" * 60)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_imports()
    all_passed &= test_parser()
    all_passed &= test_visualizer()
    all_passed &= check_system_dependencies()
    all_passed &= create_sample_documents()
    
    # Final result
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All core tests passed!")
        print("\nYou can now run the app with:")
        print("  streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please install missing dependencies.")
        print("\nInstall core dependencies with:")
        print("  pip install -r requirements.txt")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
