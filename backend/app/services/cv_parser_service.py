import fitz  # PyMuPDF
import docx
from io import BytesIO

def parse_cv(file_path: str, file_content: bytes) -> str:
    """
    Parses the content of a CV file (PDF or DOCX) and returns the raw text.

    Args:
        file_path: The original filename to determine the file type.
        file_content: The byte content of the file.

    Returns:
        The extracted text content as a string.

    Raises:
        ValueError: If the file type is not .pdf or .docx.
    """
    text = ""
    if file_path.endswith(".pdf"):
        # Use a context manager to ensure the file is properly closed
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    elif file_path.endswith(".docx"):
        # Open the document from an in-memory byte stream
        doc = docx.Document(BytesIO(file_content))
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        # Fail fast for unsupported types
        raise ValueError(f"Unsupported file type: {file_path}")
    return text
