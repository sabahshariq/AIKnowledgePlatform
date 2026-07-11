from pypdf import PdfReader

def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    full_text = ""

    for page in reader.pages:
        page_text=page.extract_text()

        if page_text:
            full_text += page_text + "\n"

    return full_text