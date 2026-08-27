#!/usr/bin/env python3
"""
Example script demonstrating various ways to use the Document Parser API.
"""

from parsers import DocumentParser
from visualizer import DocumentVisualizer
from pathlib import Path


def example_1_basic_usage():
    """Example 1: Basic document parsing with auto-detection."""
    print("\n" + "="*60)
    print("Example 1: Basic Usage with Auto-Detection")
    print("="*60)
    
    parser = DocumentParser()
    
    # Parse a text file
    results = parser.parse('sample_documents/sample.txt')
    
    print(f"Tool used: {results['tool_used']}")
    print(f"Content length: {len(results['content'])} characters")
    print(f"Number of pages: {len(results['pages'])}")
    print("\nFirst 200 characters:")
    print(results['content'][:200])


def example_2_pdf_with_analysis():
    """Example 2: PDF parsing with document analysis."""
    print("\n" + "="*60)
    print("Example 2: PDF with Document Analysis")
    print("="*60)
    
    # This example requires a PDF file
    # Create a simple text PDF or use your own
    pdf_path = 'sample_documents/sample.pdf'
    
    if not Path(pdf_path).exists():
        print(f"⚠️  PDF file not found: {pdf_path}")
        print("Please place a PDF file at this location or update the path.")
        return
    
    parser = DocumentParser(
        detect_scanned=True,
        extract_images=False
    )
    
    results = parser.parse(pdf_path)
    
    print(f"Tool used: {results['tool_used']}")
    
    if results.get('pdf_analysis'):
        analysis = results['pdf_analysis']
        print(f"\nPDF Analysis:")
        print(f"  Type: {analysis['type']}")
        print(f"  Total pages: {analysis['total_pages']}")
        print(f"  Scanned pages: {len(analysis.get('scanned_pages', []))}")
        print(f"  Hybrid pages: {len(analysis.get('hybrid_pages', []))}")
        print(f"  Digital pages: {len(analysis.get('digital_pages', []))}")


def example_3_specific_tool():
    """Example 3: Using a specific parsing tool."""
    print("\n" + "="*60)
    print("Example 3: Using Specific Tools")
    print("="*60)
    
    # Try different tools on the same document
    tools = ['pymupdf', 'pymupdf4llm']
    
    for tool in tools:
        try:
            parser = DocumentParser(tool=tool)
            results = parser.parse('sample_documents/sample.txt')
            
            print(f"\n{tool}:")
            print(f"  Content length: {len(results['content'])} chars")
            print(f"  Tool used: {results['tool_used']}")
        except Exception as e:
            print(f"\n{tool}: Not available - {e}")


def example_4_ocr_scanned_pdf():
    """Example 4: OCR for scanned PDFs."""
    print("\n" + "="*60)
    print("Example 4: OCR for Scanned Documents")
    print("="*60)
    
    scanned_pdf = 'sample_documents/scanned.pdf'
    
    if not Path(scanned_pdf).exists():
        print(f"⚠️  Scanned PDF not found: {scanned_pdf}")
        print("This example requires a scanned PDF file.")
        return
    
    try:
        parser = DocumentParser(
            tool='tesseract_ocr',
            ocr_lang='eng'
        )
        
        results = parser.parse(scanned_pdf)
        
        print(f"Tool used: {results['tool_used']}")
        print(f"Pages processed: {len(results['pages'])}")
        print("\nFirst page content preview:")
        if results['pages']:
            print(results['pages'][0]['content'][:300])
    except ImportError as e:
        print(f"⚠️  OCR not available: {e}")
        print("Install with: pip install pytesseract pdf2image")


def example_5_table_extraction():
    """Example 5: Table extraction from PDF."""
    print("\n" + "="*60)
    print("Example 5: Table Extraction")
    print("="*60)
    
    table_pdf = 'sample_documents/tables.pdf'
    
    if not Path(table_pdf).exists():
        print(f"⚠️  Table PDF not found: {table_pdf}")
        print("This example requires a PDF with tables.")
        return
    
    try:
        # pdfplumber is best for tables
        parser = DocumentParser(tool='pdfplumber')
        results = parser.parse(table_pdf)
        
        print(f"Tool used: {results['tool_used']}")
        print(f"\nExtracted content with tables:")
        print(results['content'][:500])
    except ImportError as e:
        print(f"⚠️  pdfplumber not available: {e}")
        print("Install with: pip install pdfplumber")


def example_6_office_documents():
    """Example 6: Parsing Office documents."""
    print("\n" + "="*60)
    print("Example 6: Office Document Parsing")
    print("="*60)
    
    office_files = {
        'sample_documents/document.docx': 'Word',
        'sample_documents/presentation.pptx': 'PowerPoint',
        'sample_documents/spreadsheet.xlsx': 'Excel'
    }
    
    parser = DocumentParser()
    
    for filepath, doc_type in office_files.items():
        if Path(filepath).exists():
            try:
                results = parser.parse(filepath)
                print(f"\n{doc_type} ({Path(filepath).name}):")
                print(f"  Tool: {results['tool_used']}")
                print(f"  Content length: {len(results['content'])} chars")
                
                if results.get('metadata'):
                    for key, value in results['metadata'].items():
                        print(f"  {key}: {value}")
            except Exception as e:
                print(f"  Error: {e}")
        else:
            print(f"\n{doc_type}: File not found ({filepath})")


def example_7_batch_processing():
    """Example 7: Batch processing multiple documents."""
    print("\n" + "="*60)
    print("Example 7: Batch Processing")
    print("="*60)
    
    # Get all files in sample_documents directory
    sample_dir = Path('sample_documents')
    
    if not sample_dir.exists():
        print(f"⚠️  Directory not found: {sample_dir}")
        return
    
    files = list(sample_dir.glob('*'))
    
    if not files:
        print("No files found in sample_documents/")
        return
    
    parser = DocumentParser()
    results_summary = []
    
    for filepath in files:
        if filepath.is_file():
            try:
                results = parser.parse(str(filepath))
                results_summary.append({
                    'file': filepath.name,
                    'tool': results['tool_used'],
                    'pages': len(results.get('pages', [])),
                    'size': len(results['content'])
                })
                print(f"✅ {filepath.name} - {results['tool_used']}")
            except Exception as e:
                print(f"❌ {filepath.name} - Error: {str(e)[:50]}")
    
    # Print summary
    print("\n📊 Processing Summary:")
    print(f"{'File':<30} {'Tool':<20} {'Pages':<10} {'Size':<10}")
    print("-" * 70)
    for item in results_summary:
        print(f"{item['file']:<30} {item['tool']:<20} {item['pages']:<10} {item['size']:<10}")


def example_8_image_extraction():
    """Example 8: Extract images from documents."""
    print("\n" + "="*60)
    print("Example 8: Image Extraction")
    print("="*60)
    
    pdf_path = 'sample_documents/sample.pdf'
    
    if not Path(pdf_path).exists():
        print(f"⚠️  PDF file not found: {pdf_path}")
        return
    
    parser = DocumentParser(extract_images=True)
    results = parser.parse(pdf_path)
    
    print(f"Images extracted: {len(results.get('images', []))}")
    
    if results.get('images'):
        for idx, img_data in enumerate(results['images']):
            print(f"  Image {idx + 1}:")
            print(f"    Page: {img_data.get('page', 'N/A')}")
            print(f"    Format: {img_data.get('ext', 'N/A')}")
            print(f"    Size: {len(img_data.get('image', b''))} bytes")


def example_9_url_parsing():
    """Example 9: Parse document from URL."""
    print("\n" + "="*60)
    print("Example 9: URL Document Parsing")
    print("="*60)
    
    # Example URL (use a real PDF URL)
    url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    
    print(f"Downloading from: {url}")
    
    try:
        parser = DocumentParser()
        results = parser.parse(url)
        
        print(f"✅ Downloaded and parsed successfully")
        print(f"Tool used: {results['tool_used']}")
        print(f"Content length: {len(results['content'])} characters")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_10_bounding_box_visualization():
    """Example 10: Visualize bounding boxes."""
    print("\n" + "="*60)
    print("Example 10: Bounding Box Visualization")
    print("="*60)
    
    pdf_path = 'sample_documents/sample.pdf'
    
    if not Path(pdf_path).exists():
        print(f"⚠️  PDF file not found: {pdf_path}")
        return
    
    # Parse with tool that provides bboxes
    parser = DocumentParser(tool='pymupdf4llm')
    results = parser.parse(pdf_path)
    
    if results.get('pages') and results['pages'][0].get('bboxes'):
        visualizer = DocumentVisualizer()
        
        print(f"Pages with bboxes: {len(results['pages'])}")
        
        # Visualize first page
        page_data = results['pages'][0]
        print(f"Bounding boxes on page 1: {len(page_data['bboxes'])}")
        
        try:
            img = visualizer.draw_bboxes(
                pdf_path,
                0,  # First page
                page_data['bboxes']
            )
            
            if img:
                # Save visualization
                output_path = 'sample_documents/visualization.png'
                img.save(output_path)
                print(f"✅ Saved visualization to: {output_path}")
        except Exception as e:
            print(f"❌ Visualization error: {e}")
    else:
        print("No bounding box data available")


def main():
    """Run all examples."""
    print("\n" + "🎨"*30)
    print("Document Parser API - Usage Examples")
    print("🎨"*30)
    
    # Create sample documents directory if it doesn't exist
    Path('sample_documents').mkdir(exist_ok=True)
    
    # Run examples
    example_1_basic_usage()
    example_2_pdf_with_analysis()
    example_3_specific_tool()
    example_4_ocr_scanned_pdf()
    example_5_table_extraction()
    example_6_office_documents()
    example_7_batch_processing()
    example_8_image_extraction()
    example_9_url_parsing()
    example_10_bounding_box_visualization()
    
    print("\n" + "="*60)
    print("✅ Examples completed!")
    print("="*60)
    print("\nTo run the web interface:")
    print("  streamlit run app.py")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()
