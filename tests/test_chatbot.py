"""
Unit tests cho chatbot system
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import load_config, load_environment
from src.document_processor import DocumentProcessor
from src.embeddings import EmbeddingManager
from langchain.schema import Document


class TestDocumentProcessor:
    """Test DocumentProcessor"""
    
    def test_initialization(self):
        config = load_config()
        processor = DocumentProcessor(config)
        assert processor.chunk_size > 0
        assert processor.chunk_overlap >= 0
    
    def test_split_documents(self):
        config = load_config()
        processor = DocumentProcessor(config)
        
        # Create dummy document
        docs = [Document(
            page_content="This is a test document. " * 100,
            metadata={"source": "test.txt"}
        )]
        
        chunks = processor.split_documents(docs)
        assert len(chunks) > 0
        assert all(isinstance(chunk, Document) for chunk in chunks)


class TestEmbeddingManager:
    """Test EmbeddingManager"""
    
    def test_initialization(self):
        config = load_config()
        env = load_environment()
        
        # Skip if no API keys
        if not any([env.get('openai_api_key'), env.get('google_api_key')]):
            pytest.skip("No API keys configured")
        
        manager = EmbeddingManager(config, env)
        assert manager.embeddings is not None


def test_config_loading():
    """Test config loading"""
    config = load_config()
    assert 'document_processing' in config
    assert 'embedding' in config
    assert 'vectorstore' in config
    assert 'llm' in config


def test_environment_loading():
    """Test environment loading"""
    env = load_environment()
    assert isinstance(env, dict)
    assert 'llm_provider' in env


if __name__ == "__main__":
    pytest.main([__file__, "-v"])







