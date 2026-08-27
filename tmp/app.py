import streamlit as st
import os
from pathlib import Path
import tempfile
from parsers import DocumentParser
from visualizer import DocumentVisualizer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import json
import re
import hashlib
from datetime import datetime


def _stable_id(*parts: str) -> str:
    s = "|".join(parts)
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:16]


def _clean_text(s: str) -> str:
    # Remove excessive whitespace, keep paragraphs
    s = s.replace("\r", "\n")
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()


def chunk_text(text: str, max_chars: int = 900, overlap: int = 120):
    """
    Simple character chunker. Good enough for a first RAG pipeline.
    You can replace with token-based chunking later.
    """
    text = _clean_text(text)
    if not text:
        return []

    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + max_chars)
        chunk = text[start:end]

        # try to cut at paragraph boundary if possible
        if end < n:
            cut = chunk.rfind("\n\n")
            if cut > max_chars * 0.5:
                end = start + cut
                chunk = text[start:end]

        chunks.append(chunk.strip())

        if end == n:
            break
        start = max(0, end - overlap)

    return [c for c in chunks if c]


def build_rag_json(results: dict, document_path: str, chunk_size: int = 900, overlap: int = 120) -> dict:
    """
    Build a RAG-friendly JSON:
      - "chunks": list of {id, text, metadata}
      - metadata contains page number if available
    """
    file_name = results.get("file_name") or (Path(document_path).name if document_path else "document")
    tool_used = results.get("tool_used", "unknown")
    file_type = results.get("file_type", "unknown")

    rag = {
        "schema": "rag_chunks_v1",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "document": {
            "file_name": file_name,
            "file_type": file_type,
            "tool_used": tool_used,
            "file_size": results.get("file_size"),
            "pdf_analysis": results.get("pdf_analysis"),
        },
        "chunks": []
    }

    # Prefer page-by-page if available (best for citations)
    pages = results.get("pages") or []
    if pages:
        for p in pages:
            page_num = p.get("page_number")
            page_text = p.get("content", "") or ""
            page_text = _clean_text(page_text)

            if not page_text:
                continue

            page_chunks = chunk_text(page_text, max_chars=chunk_size, overlap=overlap)
            for i, ch in enumerate(page_chunks):
                chunk_id = _stable_id(file_name, str(page_num), str(i), ch[:40])
                rag["chunks"].append({
                    "id": chunk_id,
                    "text": ch,
                    "metadata": {
                        "file_name": file_name,
                        "file_type": file_type,
                        "tool_used": tool_used,
                        "page": page_num,
                        "chunk_index": i,
                        # Optional: if you later add bbox per chunk, put it here
                        # "bbox": ...
                    }
                })

    else:
        # Fallback: full content (markdown or plain text)
        content = results.get("content", "") or ""
        content = _clean_text(content)
        for i, ch in enumerate(chunk_text(content, max_chars=chunk_size, overlap=overlap)):
            chunk_id = _stable_id(file_name, "doc", str(i), ch[:40])
            rag["chunks"].append({
                "id": chunk_id,
                "text": ch,
                "metadata": {
                    "file_name": file_name,
                    "file_type": file_type,
                    "tool_used": tool_used,
                    "chunk_index": i,
                }
            })

    return rag

# Page configuration
st.set_page_config(
    page_title="Document Parser API Demo",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if 'parsed_results' not in st.session_state:
    st.session_state.parsed_results = None
if 'document_path' not in st.session_state:
    st.session_state.document_path = None

def main():
    st.title("📄 Universal Document Parser API")
    st.markdown("Parse and visualize documents with multiple parsing engines")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Input method selection
    input_method = st.sidebar.radio(
        "Input Method",
        ["Upload File", "File Path", "URL"]
    )
    
    document_path = None
    
    # Handle different input methods
    if input_method == "Upload File":
        uploaded_file = st.sidebar.file_uploader(
            "Choose a document",
            type=['pdf', 'docx', 'doc', 'pptx', 'ppt', 'xlsx', 'xls', 'txt', 'md', 'html']
        )
        
        if uploaded_file:
            # Save uploaded file to temp directory
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                document_path = tmp_file.name
                
    elif input_method == "File Path":
        document_path = st.sidebar.text_input("Enter file path")
        
    elif input_method == "URL":
        url = st.sidebar.text_input("Enter URL")
        if url:
            document_path = url
    
    # Tool selection
    st.sidebar.subheader("🔧 Parser Selection")
    
    available_tools = [
        "Auto (Recommended)",
        "PyMuPDF",
        "PyMuPDF4LLM",
        "Docling",
        "Unstructured",
        "pdfplumber",
        "python-docx",
        "python-pptx",
        "openpyxl",
        "Tesseract OCR",
        "EasyOCR"
    ]
    
    selected_tool = st.sidebar.selectbox(
        "Select parsing tool",
        available_tools,
        help="Choose a specific tool or let the system auto-detect the best option"
    )
    
    # Additional options
    st.sidebar.subheader("📋 Options")
    
    detect_scanned = st.sidebar.checkbox(
        "Detect scanned/hybrid PDFs",
        value=True,
        help="Analyze if PDF is scanned, digital, or hybrid"
    )
    
    extract_images = st.sidebar.checkbox(
        "Extract images",
        value=False,
        help="Extract embedded images from document"
    )
    
    ocr_language = st.sidebar.selectbox(
        "OCR Language",
        ["eng", "fra", "deu", "spa", "chi_sim", "jpn"],
        help="Language for OCR processing"
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📥 Document Processing")
        
        if document_path:
            st.info(f"**Document:** {Path(document_path).name if not document_path.startswith('http') else document_path}")
            
            # Process button
            if st.button("🚀 Parse Document", type="primary"):
                with st.spinner("Parsing document..."):
                    try:
                        # Initialize parser
                        tool = None if selected_tool == "Auto (Recommended)" else selected_tool.lower().replace(" ", "_")
                        
                        parser = DocumentParser(
                            tool=tool,
                            detect_scanned=detect_scanned,
                            extract_images=extract_images,
                            ocr_lang=ocr_language
                        )
                        
                        # Parse document
                        results = parser.parse(document_path)
                        
                        # Store in session state
                        st.session_state.parsed_results = results
                        st.session_state.document_path = document_path
                        
                        st.success(f"✅ Document parsed successfully using **{results.get('tool_used', 'Unknown')}**")
                        
                        # Display metadata
                        if results.get('metadata'):
                            with st.expander("📊 Document Metadata"):
                                st.json(results['metadata'])
                        
                        # Display PDF analysis
                        if results.get('pdf_analysis'):
                            analysis = results['pdf_analysis']
                            st.subheader("📄 PDF Analysis")
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Document Type", analysis.get('type', 'Unknown'))
                            with col_b:
                                st.metric("Total Pages", analysis.get('total_pages', 'N/A'))
                            with col_c:
                                st.metric("Has Text", "Yes" if analysis.get('has_text') else "No")
                            
                            if analysis.get('scanned_pages'):
                                st.warning(f"⚠️ Scanned pages detected: {analysis['scanned_pages']}")
                            if analysis.get('hybrid_pages'):
                                st.info(f"ℹ️ Hybrid pages detected: {analysis['hybrid_pages']}")
                        
                    except Exception as e:
                        st.error(f"❌ Error parsing document: {str(e)}")
                        logger.exception("Parsing error")
        else:
            st.info("👈 Please select a document from the sidebar")
    
    with col2:
        st.header("ℹ️ Supported Formats")
        st.markdown("""
        **Documents:**
        - PDF (digital, scanned, hybrid)
        - Word (.docx, .doc)
        - PowerPoint (.pptx, .ppt)
        - Excel (.xlsx, .xls)
        - Text files (.txt, .md)
        - HTML
        
        **Parsing Tools:**
        - PyMuPDF (Fast PDF parsing)
        - PyMuPDF4LLM (LLM-optimized)
        - Docling (Advanced document understanding)
        - Unstructured (Multi-format)
        - pdfplumber (Table extraction)
        - Tesseract OCR (Scanned documents)
        - EasyOCR (Modern OCR)
        """)
    
    # Display results
    if st.session_state.parsed_results:
        st.divider()
        st.header("📖 Parsed Content")
        
        results = st.session_state.parsed_results
        st.subheader("🧩 Export for RAG")

        col_r1, col_r2, col_r3 = st.columns([1, 1, 2])

        with col_r1:
            chunk_size = st.number_input("Chunk size (chars)", min_value=200, max_value=3000, value=900, step=100)

        with col_r2:
            overlap = st.number_input("Overlap (chars)", min_value=0, max_value=500, value=120, step=20)

        with col_r3:
            st.caption("JSON contains chunks + metadata (page, tool, filename). Ideal for embeddings & vector DB.")

        rag_json = build_rag_json(results, st.session_state.document_path, chunk_size=int(chunk_size), overlap=int(overlap))
        rag_bytes = json.dumps(rag_json, ensure_ascii=False, indent=2).encode("utf-8")

        st.download_button(
            label="⬇️ Download RAG JSON",
            data=rag_bytes,
            file_name=f"{rag_json['document']['file_name']}.rag.json",
            mime="application/json",
        )

        st.caption(f"Chunks generated: {len(rag_json['chunks'])}")
        
        # View mode selection
        view_mode = st.radio(
            "View Mode",
            ["Markdown View", "Page-by-Page View", "Bounding Box Visualization"],
            horizontal=True
        )
        
        if view_mode == "Markdown View":
            # Display full markdown content
            if results.get('content'):
                st.markdown("---")
                st.markdown(results['content'])
            else:
                st.warning("No content extracted")
                
        elif view_mode == "Page-by-Page View":
            # Display content page by page
            if results.get('pages'):
                total_pages = len(results['pages'])
                page_num = st.slider(
                    "Select Page",
                    1,
                    total_pages,
                    1,
                    help=f"Navigate through {total_pages} pages"
                )
                
                page_content = results['pages'][page_num - 1]
                st.subheader(f"Page {page_num} of {total_pages}")
                st.markdown("---")
                st.markdown(page_content.get('content', 'No content'))
                
                # Show page metadata
                if page_content.get('metadata'):
                    with st.expander("Page Metadata"):
                        st.json(page_content['metadata'])
            else:
                st.warning("No page-level content available")
                
        elif view_mode == "Bounding Box Visualization":
            # Visualize bounding boxes
            if results.get('pages') and results['pages'][0].get('bboxes'):
                visualizer = DocumentVisualizer()
                
                total_pages = len(results['pages'])
                page_num = st.slider(
                    "Select Page",
                    1,
                    total_pages,
                    1,
                    key="bbox_page",
                    help=f"Navigate through {total_pages} pages"
                )
                
                page_data = results['pages'][page_num - 1]
                
                if page_data.get('bboxes'):
                    st.subheader(f"Page {page_num} - Bounding Boxes")
                    
                    # Show legend
                    col_legend1, col_legend2 = st.columns(2)
                    with col_legend1:
                        st.markdown("🔴 **Red**: Images")
                    with col_legend2:
                        st.markdown("🔵 **Blue**: Text")
                    
                    # Display visualization
                    try:
                        img = visualizer.draw_bboxes(
                            st.session_state.document_path,
                            page_num - 1,
                            page_data['bboxes']
                        )
                        if img:
                            st.image(img, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error visualizing bounding boxes: {str(e)}")
                else:
                    st.warning("No bounding box information available for this page")
            else:
                st.info("Bounding box visualization is only available for certain document types and parsers")
        
        # Display extracted images
        if results.get('images'):
            st.divider()
            st.subheader(f"🖼️ Extracted Images ({len(results['images'])})")
            
            cols = st.columns(3)
            for idx, img_data in enumerate(results['images']):
                with cols[idx % 3]:
                    st.image(img_data['image'], caption=f"Image {idx + 1}", use_container_width=True)
                    if img_data.get('page'):
                        st.caption(f"Page {img_data['page']}")

if __name__ == "__main__":
    main()
