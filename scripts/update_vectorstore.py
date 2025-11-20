#!/usr/bin/env python3
"""
Script để update vectorstore với documents mới
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import load_config, load_environment
from src.document_processor import DocumentProcessor
from src.embeddings import EmbeddingManager


def main():
    """
    Main function để update vectorstore
    """
    print("=" * 70)
    print("🔄 CẬP NHẬT VECTORSTORE")
    print("=" * 70)
    
    # Load configuration
    config = load_config()
    env = load_environment()
    
    # Check for new documents
    docs_dir = "data/documents"
    print(f"\n📂 Kiểm tra documents trong {docs_dir}...")
    
    # Process documents
    processor = DocumentProcessor(config)
    documents = processor.process_documents(docs_dir)
    
    if not documents:
        print("\n❌ Không có documents mới để thêm")
        return
    
    stats = processor.get_document_stats(documents)
    print(f"\n📊 Tìm thấy {stats['total_chunks']} chunks từ {stats['unique_sources']} file(s)")
    
    # Load existing vectorstore
    print("\n🔧 Loading vectorstore hiện tại...")
    embedding_manager = EmbeddingManager(config, env)
    
    if not embedding_manager.load_vectorstore():
        print("\n⚠️  Vectorstore chưa tồn tại. Tạo mới...")
        embedding_manager.create_vectorstore(documents)
    else:
        # Add new documents
        print("\n➕ Thêm documents mới vào vectorstore...")
        embedding_manager.add_documents(documents)
    
    print("\n✅ Hoàn tất!")


if __name__ == "__main__":
    main()







