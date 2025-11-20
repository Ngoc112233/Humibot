#!/usr/bin/env python3
"""
Script để xử lý documents và tạo vectorstore
Chạy script này để chuẩn bị dữ liệu cho chatbot
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import load_config, load_environment, validate_api_keys, ensure_directory
from src.document_processor import DocumentProcessor
from src.embeddings import EmbeddingManager


def main():
    """
    Main function để process documents
    """
    print("=" * 70)
    print("📚 XỬ LÝ VÀ INDEX DOCUMENTS CHO CHATBOT")
    print("=" * 70)
    
    # Load configuration
    print("\n🔧 Loading configuration...")
    config = load_config()
    env = load_environment()
    
    # Validate API keys
    if not validate_api_keys(config, env):
        print("\n❌ Vui lòng cấu hình API keys trong file .env")
        return
    
    # Kiểm tra thư mục documents
    docs_dir = "data/documents"
    if not Path(docs_dir).exists() or not any(Path(docs_dir).iterdir()):
        print(f"\n⚠️  Thư mục {docs_dir} trống hoặc không tồn tại")
        print(f"\nVui lòng:")
        print(f"  1. Tạo thư mục: mkdir -p {docs_dir}")
        print(f"  2. Thêm các file tài liệu (PDF, DOCX, TXT) vào thư mục")
        print(f"  3. Chạy lại script này")
        return
    
    # Ensure vectorstore directory exists
    ensure_directory(config['vectorstore']['persist_directory'])
    
    try:
        # Step 1: Process documents
        print("\n" + "=" * 70)
        print("BƯỚC 1: XỬ LÝ DOCUMENTS")
        print("=" * 70)
        
        processor = DocumentProcessor(config)
        documents = processor.process_documents(docs_dir)
        
        if not documents:
            print("\n❌ Không có documents nào được xử lý thành công")
            return
        
        # Show statistics
        stats = processor.get_document_stats(documents)
        print("\n📊 Thống kê Documents:")
        print(f"   ✓ Tổng số chunks: {stats['total_chunks']}")
        print(f"   ✓ Tổng số ký tự: {stats['total_characters']:,}")
        print(f"   ✓ Kích thước chunk trung bình: {stats['avg_chunk_size']} ký tự")
        print(f"   ✓ Số file nguồn: {stats['unique_sources']}")
        print(f"   ✓ Loại file: {stats['file_types']}")
        
        # Step 2: Create embeddings and vectorstore
        print("\n" + "=" * 70)
        print("BƯỚC 2: TẠO EMBEDDINGS VÀ VECTORSTORE")
        print("=" * 70)
        
        embedding_manager = EmbeddingManager(config, env)
        
        # Check if vectorstore already exists
        vectorstore_exists = Path(config['vectorstore']['persist_directory']).exists()
        
        if vectorstore_exists:
            print("\n⚠️  Vectorstore đã tồn tại!")
            choice = input("Bạn muốn:\n  [1] Xóa và tạo mới\n  [2] Thêm vào vectorstore hiện tại\n  [3] Hủy\nChọn (1/2/3): ")
            
            if choice == '1':
                print("\n🔨 Tạo vectorstore mới...")
                embedding_manager.create_vectorstore(documents)
            elif choice == '2':
                print("\n➕ Thêm documents vào vectorstore hiện tại...")
                embedding_manager.load_vectorstore()
                embedding_manager.add_documents(documents)
            else:
                print("\n❌ Đã hủy")
                return
        else:
            print("\n🔨 Tạo vectorstore mới...")
            embedding_manager.create_vectorstore(documents)
        
        # Step 3: Test retrieval
        print("\n" + "=" * 70)
        print("BƯỚC 3: TEST RETRIEVAL")
        print("=" * 70)
        
        test_query = "sinh viên"
        print(f"\n🔍 Test query: '{test_query}'")
        
        results = embedding_manager.similarity_search(test_query, k=3)
        print(f"✓ Tìm thấy {len(results)} kết quả")
        
        if results:
            print("\nVí dụ kết quả đầu tiên:")
            print(f"  - Source: {results[0].metadata.get('source', 'Unknown')}")
            print(f"  - Content preview: {results[0].page_content[:150]}...")
        
        # Success
        print("\n" + "=" * 70)
        print("✅ HOÀN TẤT!")
        print("=" * 70)
        print("\nBước tiếp theo:")
        print("  1. Chạy chatbot CLI: python chatbot.py")
        print("  2. Hoặc chạy web interface: streamlit run app.py")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()







