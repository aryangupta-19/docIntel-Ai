from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

import io
from PIL import Image

def load_and_chunk_report(path: str, chunk_size: int= 1000, chunk_overlap: int=150):
    """
    Loads an uploaded document PDF and splits it into
    overlapping chunks suitable for embedding + retrieval.

    chunk_size: max characters per chunk
    chunk_overlap: characters shared between consecutive chunks,
                   so context isn't lost at chunk boundaries

    """
    loader= PyPDFLoader(path)
    pages = loader.load()

    # Determine whether usable text was extracted by PyPDFLoader.
    total_text = 0
    for p in pages:
        try:
            total_text += len(p.page_content.strip() or "")
        except Exception:
            continue

    # If no usable text, run OCR fallback (scanned/image PDFs only).
    if total_text <= 20:
        try:
            import fitz  # PyMuPDF, already present in requirements
        except Exception as e:
            raise RuntimeError("OCR fallback required but PyMuPDF (fitz) is unavailable") from e

        try:
            import pytesseract
        except Exception as e:
            raise RuntimeError(
                "OCR fallback required but pytesseract is not installed or not importable. "
                "Install the Python package and ensure the Tesseract binary is available on PATH."
            ) from e

        # Render pages to images and run OCR per page
        doc = fitz.open(path)
        ocr_docs = []
        for i in range(doc.page_count):
            page = doc.load_page(i)
            pix = page.get_pixmap(alpha=False)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(img)
            text = text.strip()
            if not text:
                continue
            meta = {"source": path, "page": i + 1}
            ocr_docs.append(Document(page_content=text, metadata=meta))

        if ocr_docs:
            pages = ocr_docs
        else:
            raise RuntimeError("OCR fallback ran but no text was extracted from PDF images.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap= chunk_overlap,
        separators= ["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks= splitter.split_documents(pages)
    return chunks


