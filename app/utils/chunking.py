import re
from typing import List


def sentence_chunk(text: str) -> List[str]:
    """
    Split text into sentence-level chunks.
    This version is intentionally simple and reliable.
    """
    if not text:
        return []

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text.strip())

    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)

    return [s.strip() for s in sentences if s.strip()]

