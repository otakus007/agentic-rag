from unittest.mock import patch, MagicMock
from types import SimpleNamespace
from src.agent.retriever import retrieve_context


@patch("src.agent.retriever.get_qdrant_client")
@patch("src.agent.retriever.get_embedding")
def test_retrieve_context_returns_results(mock_embed, mock_qdrant_factory):
    mock_embed.return_value = [0.1] * 1536
    mock_qdrant = MagicMock()
    mock_qdrant.get_collections.return_value = MagicMock(
        collections=[SimpleNamespace(name="kb_agent_1")]
    )
    mock_qdrant.search.return_value = [
        MagicMock(
            payload={"content": "Policy doc", "page_number": 2, "block_type": "paragraph"},
            score=0.9
        )
    ]
    mock_qdrant_factory.return_value = mock_qdrant

    results = retrieve_context("what is the policy?", agent_id="agent_1")
    assert len(results) == 1
    assert results[0]["content"] == "Policy doc"
    assert results[0]["score"] == 0.9
    assert results[0]["page_number"] == 2


@patch("src.agent.retriever.get_qdrant_client")
@patch("src.agent.retriever.get_embedding")
def test_retrieve_context_empty_when_no_collection(mock_embed, mock_qdrant_factory):
    mock_embed.return_value = [0.1] * 1536
    mock_qdrant = MagicMock()
    mock_qdrant.get_collections.return_value = MagicMock(collections=[])
    mock_qdrant_factory.return_value = mock_qdrant

    results = retrieve_context("query", agent_id="nonexistent")
    assert results == []
    mock_qdrant.search.assert_not_called()
