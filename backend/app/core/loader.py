from pypdf import PdfReader
import io

def extract_text_from_pdf(file: bytes) -> str:
    reader = PdfReader(io.BytesIO(file))
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text