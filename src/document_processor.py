"""
Document Processing Module
Xử lý và chia nhỏ documents từ nhiều định dạng
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm

from langchain.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class DocumentProcessor:
    """
    Class xử lý documents từ nhiều nguồn và định dạng khác nhau
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Khởi tạo Document Processor
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.chunk_size = config['document_processing']['chunk_size']
        self.chunk_overlap = config['document_processing']['chunk_overlap']
        self.supported_formats = config['document_processing']['supported_formats']
        
        # Khởi tạo text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=config['document_processing']['separators'],
            length_function=len,
        )
        
    def load_document(self, file_path: str) -> List[Document]:
        """
        Load một document từ file
        
        Args:
            file_path: Đường dẫn đến file
            
        Returns:
            List of Document objects
        """
        file_extension = Path(file_path).suffix.lower().replace('.', '')
        
        try:
            if file_extension == 'pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension == 'docx':
                loader = Docx2txtLoader(file_path)
            elif file_extension == 'txt':
                loader = TextLoader(file_path, encoding='utf-8')
            elif file_extension == 'md':
                loader = UnstructuredMarkdownLoader(file_path)
            else:
                print(f"⚠️  Định dạng không được hỗ trợ: {file_extension}")
                return []
            
            documents = loader.load()
            
            # Thêm metadata
            for doc in documents:
                doc.metadata['source'] = os.path.basename(file_path)
                doc.metadata['file_path'] = file_path
                doc.metadata['file_type'] = file_extension
            
            return documents
            
        except Exception as e:
            print(f"❌ Lỗi khi load file {file_path}: {str(e)}")
            return []
    
    def load_documents_from_directory(self, directory: str) -> List[Document]:
        """
        Load tất cả documents từ một thư mục
        
        Args:
            directory: Đường dẫn thư mục chứa documents
            
        Returns:
            List of Document objects
        """
        all_documents = []
        directory_path = Path(directory)
        
        if not directory_path.exists():
            print(f"❌ Thư mục không tồn tại: {directory}")
            return []
        
        # Tìm tất cả files với định dạng được hỗ trợ
        files = []
        for ext in self.supported_formats:
            files.extend(directory_path.rglob(f"*.{ext}"))
        
        print(f"📚 Tìm thấy {len(files)} file(s) để xử lý...")
        
        # Load từng file
        for file_path in tqdm(files, desc="Loading documents"):
            docs = self.load_document(str(file_path))
            all_documents.extend(docs)
        
        print(f"✅ Đã load {len(all_documents)} document(s)")
        return all_documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Chia documents thành các chunks nhỏ hơn
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of chunked Document objects
        """
        print(f"✂️  Đang chia documents thành chunks...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"✅ Đã tạo {len(chunks)} chunk(s)")
        return chunks
    
    def process_documents(self, directory: str) -> List[Document]:
        """
        Process pipeline hoàn chỉnh: load + split
        
        Args:
            directory: Đường dẫn thư mục chứa documents
            
        Returns:
            List of processed Document chunks
        """
        # Load documents
        documents = self.load_documents_from_directory(directory)
        
        if not documents:
            print("⚠️  Không có document nào được load")
            return []
        
        # Split into chunks
        chunks = self.split_documents(documents)
        
        return chunks
    
    def get_document_stats(self, documents: List[Document]) -> Dict[str, Any]:
        """
        Lấy thống kê về documents
        
        Args:
            documents: List of Document objects
            
        Returns:
            Dictionary chứa thống kê
        """
        total_chars = sum(len(doc.page_content) for doc in documents)
        
        # Thống kê theo loại file
        file_types = {}
        sources = set()
        
        for doc in documents:
            file_type = doc.metadata.get('file_type', 'unknown')
            file_types[file_type] = file_types.get(file_type, 0) + 1
            sources.add(doc.metadata.get('source', 'unknown'))
        
        return {
            'total_chunks': len(documents),
            'total_characters': total_chars,
            'avg_chunk_size': total_chars // len(documents) if documents else 0,
            'unique_sources': len(sources),
            'file_types': file_types,
        }


def add_custom_metadata(documents: List[Document], 
                        metadata: Dict[str, Any]) -> List[Document]:
    """
    Thêm custom metadata vào documents
    
    Args:
        documents: List of Document objects
        metadata: Dictionary chứa metadata cần thêm
        
    Returns:
        List of Document objects với metadata đã update
    """
    for doc in documents:
        doc.metadata.update(metadata)
    
    return documents


if __name__ == "__main__":
    # Test document processor
    from utils import load_config
    
    config = load_config()
    processor = DocumentProcessor(config)
    
    # Test với thư mục documents
    docs = processor.process_documents("data/documents")
    
    if docs:
        stats = processor.get_document_stats(docs)
        print("\n📊 Thống kê Documents:")
        print(f"   - Tổng số chunks: {stats['total_chunks']}")
        print(f"   - Tổng số ký tự: {stats['total_characters']:,}")
        print(f"   - Kích thước trung bình: {stats['avg_chunk_size']} ký tự/chunk")
        print(f"   - Số file nguồn: {stats['unique_sources']}")
        print(f"   - Loại file: {stats['file_types']}")







