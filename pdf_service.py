import fitz


def extract_text_from_file(filepath):
    """Extracts text from either a PDF or a TXT file based on file extension."""
    ext = filepath.rsplit(".", 1)[1].lower()
    text = ""

    # 1. Extract text from Plain Text files (.txt)
    if ext == "txt":
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="latin-1") as f:
                text = f.read()

    # 2. Extract text from PDF files (.pdf) using PyMuPDF (fitz)
    elif ext == "pdf":
        try:
            with fitz.open(filepath) as pdf:
                for page in pdf:
                    text += page.get_text()
        except Exception as e:
            print(f"Error reading PDF: {e}")

    return text.strip()


# Backup alias for backward compatibility
def extract_text_from_pdf(pdf_path):
    return extract_text_from_file(pdf_path)