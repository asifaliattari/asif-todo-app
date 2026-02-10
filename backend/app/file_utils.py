"""
File processing utilities for PDF and DOCX extraction
"""

import os
import PyPDF2
import docx
from typing import Optional


def extract_text_from_pdf(file_path: str) -> Optional[str]:
    """
    Extract text from PDF file

    Args:
        file_path: Path to PDF file

    Returns:
        Extracted text or None if error
    """
    try:
        text = []
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)

        return "\n\n".join(text) if text else None
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None


def extract_text_from_docx(file_path: str) -> Optional[str]:
    """
    Extract text from DOCX file

    Args:
        file_path: Path to DOCX file

    Returns:
        Extracted text or None if error
    """
    try:
        doc = docx.Document(file_path)
        text = []

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)

        return "\n\n".join(text) if text else None
    except Exception as e:
        print(f"Error extracting DOCX text: {e}")
        return None


def extract_text_from_file(file_path: str, file_type: str) -> Optional[str]:
    """
    Extract text from file based on type

    Args:
        file_path: Path to file
        file_type: File extension (pdf, docx, doc)

    Returns:
        Extracted text or None if error
    """
    file_type = file_type.lower().replace('.', '')

    if file_type == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_type in ['docx', 'doc']:
        return extract_text_from_docx(file_path)
    else:
        return None


def chunk_text(text: str, max_tokens: int = 4000) -> list[str]:
    """
    Chunk text into smaller pieces for AI context

    Args:
        text: Full text content
        max_tokens: Max tokens per chunk (approximate by chars)

    Returns:
        List of text chunks
    """
    # Rough estimation: 1 token ≈ 4 characters
    max_chars = max_tokens * 4

    if len(text) <= max_chars:
        return [text]

    # Split into chunks at paragraph breaks
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_length = 0

    for para in paragraphs:
        para_length = len(para)

        if current_length + para_length > max_chars and current_chunk:
            # Save current chunk and start new one
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_length = para_length
        else:
            current_chunk.append(para)
            current_length += para_length + 2  # +2 for '\n\n'

    # Add remaining chunk
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks


def validate_file_type(filename: str) -> bool:
    """
    Validate if file type is allowed

    Args:
        filename: Original filename

    Returns:
        True if allowed, False otherwise
    """
    allowed_extensions = {'.pdf', '.doc', '.docx'}
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in allowed_extensions


def get_file_extension(filename: str) -> str:
    """
    Get file extension

    Args:
        filename: Original filename

    Returns:
        File extension without dot (e.g., 'pdf')
    """
    return os.path.splitext(filename)[1].lower().replace('.', '')
