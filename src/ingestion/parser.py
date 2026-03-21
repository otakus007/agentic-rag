"""MinerU PDF parser wrapper.

Provides a thin abstraction over MinerU's PDF extraction.
The `extract_pdf_blocks` function is the mockable boundary — in production
it calls MinerU internals; in tests it gets patched.
"""
from typing import List, Dict, Any


def extract_pdf_blocks(file_path: str) -> List[Dict[str, Any]]:
    """Low-level MinerU extraction. This is the mockable boundary.
    
    In production, this calls MinerU's `magic_pdf` extraction pipeline.
    Returns raw block dicts with content, type, and page metadata.
    """
    try:
        from magic_pdf.data.data_reader_writer import FileBasedDataReader
        from magic_pdf.pipe.UNIPipe import UNIPipe
        import json

        reader = FileBasedDataReader("")
        pdf_bytes = reader.read(file_path)

        pipe = UNIPipe(pdf_bytes, [], image_writer=None)
        pipe.pipe_classify()
        pipe.pipe_analyze()
        pipe.pipe_parse()

        content = json.loads(pipe.pipe_mk_markdown())
        
        blocks = []
        for i, page in enumerate(content.get("pdf_info", [])):
            for block in page.get("preproc_blocks", []):
                blocks.append({
                    "content": block.get("text", ""),
                    "block_type": block.get("type", "paragraph"),
                    "page_number": i + 1,
                })
        return blocks
    except ImportError:
        raise ImportError(
            "MinerU (magic-pdf) is not installed. "
            "Install it with: pip install magic-pdf"
        )


def parse_pdf(file_path: str) -> List[Dict[str, Any]]:
    """Parse a PDF file and return normalized text blocks.
    
    Each block contains:
    - content: the text content
    - block_type: heading, paragraph, table, etc.
    - page_number: 1-indexed page number
    """
    raw_blocks = extract_pdf_blocks(file_path)
    
    normalized = []
    for block in raw_blocks:
        normalized.append({
            "content": block.get("content", "").strip(),
            "block_type": block.get("block_type", "paragraph"),
            "page_number": block.get("page_number", 1),
        })
    
    # Filter out empty blocks
    return [b for b in normalized if b["content"]]
