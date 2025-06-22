from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() for page in reader.pages)

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file format")
    