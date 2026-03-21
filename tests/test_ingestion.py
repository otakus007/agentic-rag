from unittest.mock import patch, MagicMock

def test_ingestion_module_imports():
    from src.ingestion import parser, embedder
    assert parser is not None
    assert embedder is not None
