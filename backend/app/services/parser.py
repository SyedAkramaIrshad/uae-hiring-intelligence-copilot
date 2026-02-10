from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader


def parse_bytes(filename: str, content: bytes) -> str:
    lower = filename.lower()
    if lower.endswith('.pdf'):
        text = _parse_pdf(content)
        if text.strip():
            return text
    try:
        return content.decode('utf-8', errors='ignore')
    except Exception:
        return ''


def _parse_pdf(content: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(content))
        pages = [p.extract_text() or '' for p in reader.pages]
        return '\n'.join(pages)
    except Exception:
        return ''
