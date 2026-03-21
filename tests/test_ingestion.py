from unittest.mock import patch, MagicMock
from src.ingestion.parser import parse_pdf
from src.ingestion.embedder import embed_and_upsert


def test_ingestion_module_imports():
    from src.ingestion import parser, embedder
    assert parser is not None
    assert embedder is not None


# --- Task 2: Parser tests ---

@patch("src.ingestion.parser.extract_pdf_blocks")
def test_parse_pdf_returns_normalized_blocks(mock_extract):
    mock_extract.return_value = [
        {"content": "Chapter 1: Introduction", "block_type": "heading", "page_number": 1},
        {"content": "This is the intro text.", "block_type": "paragraph", "page_number": 1},
        {"content": "Data table here.", "block_type": "table", "page_number": 2},
    ]
    blocks = parse_pdf("/tmp/test.pdf")
    assert len(blocks) == 3
    assert blocks[0]["content"] == "Chapter 1: Introduction"
    assert blocks[0]["block_type"] == "heading"
    assert blocks[0]["page_number"] == 1
    assert blocks[2]["page_number"] == 2


@patch("src.ingestion.parser.extract_pdf_blocks")
def test_parse_pdf_filters_empty_blocks(mock_extract):
    mock_extract.return_value = [
        {"content": "Real content", "block_type": "paragraph", "page_number": 1},
        {"content": "   ", "block_type": "paragraph", "page_number": 1},
        {"content": "", "block_type": "paragraph", "page_number": 2},
    ]
    blocks = parse_pdf("/tmp/test.pdf")
    assert len(blocks) == 1
    assert blocks[0]["content"] == "Real content"


# --- Task 3: Embedder tests ---

@patch("src.ingestion.embedder.get_qdrant_client")
@patch("src.ingestion.embedder.get_embedding")
def test_embed_and_upsert_calls_qdrant(mock_embed, mock_qdrant_factory):
    mock_embed.return_value = [0.1] * 1536
    
    mock_qdrant = MagicMock()
    mock_qdrant.get_collections.return_value = MagicMock(collections=[])
    mock_qdrant_factory.return_value = mock_qdrant
    
    blocks = [
        {"content": "Test block", "block_type": "paragraph", "page_number": 1}
    ]
    count = embed_and_upsert(blocks, agent_id="test_agent")
    
    assert count == 1
    mock_qdrant.create_collection.assert_called_once()
    mock_qdrant.upsert.assert_called_once()


@patch("src.ingestion.embedder.get_qdrant_client")
@patch("src.ingestion.embedder.get_embedding")
def test_embed_and_upsert_payload_contains_metadata(mock_embed, mock_qdrant_factory):
    mock_embed.return_value = [0.1] * 1536
    
    mock_qdrant = MagicMock()
    mock_qdrant.get_collections.return_value = MagicMock(collections=[])
    mock_qdrant_factory.return_value = mock_qdrant
    
    blocks = [
        {"content": "Important fact", "block_type": "heading", "page_number": 3}
    ]
    embed_and_upsert(blocks, agent_id="agent_42")
    
    # Verify the upsert call has correct metadata in the payload
    upsert_call = mock_qdrant.upsert.call_args
    points = upsert_call.kwargs.get("points") or upsert_call[1].get("points")
    assert len(points) == 1
    payload = points[0].payload
    assert payload["content"] == "Important fact"
    assert payload["block_type"] == "heading"
    assert payload["page_number"] == 3
    assert payload["agent_id"] == "agent_42"
