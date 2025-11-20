"""
Embeddings Module
Quản lý các embedding models và vector database
"""

from typing import List, Dict, Any, Optional
from pathlib import Path

try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document

try:
    from langchain_community.vectorstores import Chroma, FAISS
except ImportError:
    from langchain.vectorstores import Chroma, FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


class EmbeddingManager:
    """
    Class quản lý embeddings và vector database
    """
    
    def __init__(self, config: Dict[str, Any], env: Dict[str, Any]):
        """
        Khởi tạo Embedding Manager
        
        Args:
            config: Configuration dictionary
            env: Environment variables dictionary
        """
        self.config = config
        self.env = env
        
        # Khởi tạo embedding model
        self.embeddings = self._initialize_embeddings()
        
        # Cấu hình vector database
        self.vectorstore_type = config['vectorstore']['type']
        self.persist_directory = config['vectorstore']['persist_directory']
        self.collection_name = config['vectorstore']['collection_name']
        
        self.vectorstore = None
    
    def _initialize_embeddings(self):
        """
        Khởi tạo embedding model dựa trên config
        
        Returns:
            Embedding model instance
        """
        provider = self.config['embedding']['provider']
        model_name = self.config['embedding']['model_name']
        
        print(f"🔧 Khởi tạo embedding model: {provider} - {model_name}")
        
        if provider == 'openai':
            if not self.env.get('openai_api_key'):
                raise ValueError("OPENAI_API_KEY không được cấu hình")
            return OpenAIEmbeddings(
                model=model_name,
                openai_api_key=self.env['openai_api_key']
            )
        
        elif provider in ['sentence-transformers', 'huggingface']:
            # Sử dụng HuggingFace embeddings (local hoặc API)
            model_kwargs = {'device': 'cpu'}  # Có thể đổi thành 'cuda' nếu có GPU
            encode_kwargs = {'normalize_embeddings': True}
            
            return HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs,
            )
        
        else:
            raise ValueError(f"Embedding provider không được hỗ trợ: {provider}")
    
    def create_vectorstore(self, documents: List[Document]) -> None:
        """
        Tạo vector database từ documents
        
        Args:
            documents: List of Document objects
        """
        if not documents:
            print("⚠️  Không có documents để tạo vectorstore")
            return
        
        print(f"🔨 Tạo {self.vectorstore_type} vectorstore với {len(documents)} documents...")
        
        try:
            if self.vectorstore_type == 'chromadb':
                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory,
                    collection_name=self.collection_name,
                )
                self.vectorstore.persist()
                
            elif self.vectorstore_type == 'faiss':
                self.vectorstore = FAISS.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                )
                # Lưu FAISS index
                Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
                self.vectorstore.save_local(self.persist_directory)
            
            else:
                raise ValueError(f"Vector store type không được hỗ trợ: {self.vectorstore_type}")
            
            print(f"✅ Vectorstore đã được tạo và lưu tại {self.persist_directory}")
            
        except Exception as e:
            print(f"❌ Lỗi khi tạo vectorstore: {str(e)}")
            raise
    
    def load_vectorstore(self) -> bool:
        """
        Load vectorstore đã tồn tại
        
        Returns:
            True nếu load thành công, False nếu không
        """
        if not Path(self.persist_directory).exists():
            print(f"⚠️  Vectorstore chưa tồn tại tại {self.persist_directory}")
            return False
        
        try:
            print(f"📂 Loading {self.vectorstore_type} vectorstore...")
            
            if self.vectorstore_type == 'chromadb':
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name,
                )
            
            elif self.vectorstore_type == 'faiss':
                self.vectorstore = FAISS.load_local(
                    self.persist_directory,
                    self.embeddings,
                    allow_dangerous_deserialization=True  # Cần thiết cho FAISS
                )
            
            print("✅ Vectorstore đã được load thành công")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi load vectorstore: {str(e)}")
            return False
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Thêm documents vào vectorstore hiện tại
        
        Args:
            documents: List of Document objects
        """
        if self.vectorstore is None:
            print("⚠️  Vectorstore chưa được khởi tạo. Tạo mới...")
            self.create_vectorstore(documents)
            return
        
        print(f"➕ Thêm {len(documents)} documents vào vectorstore...")
        
        try:
            self.vectorstore.add_documents(documents)
            
            # Persist changes
            if self.vectorstore_type == 'chromadb':
                self.vectorstore.persist()
            elif self.vectorstore_type == 'faiss':
                self.vectorstore.save_local(self.persist_directory)
            
            print("✅ Documents đã được thêm thành công")
            
        except Exception as e:
            print(f"❌ Lỗi khi thêm documents: {str(e)}")
    
    def similarity_search(self, 
                         query: str, 
                         k: int = 5,
                         score_threshold: Optional[float] = None) -> List[Document]:
        """
        Tìm kiếm documents tương tự với query
        
        Args:
            query: Câu truy vấn
            k: Số lượng results trả về
            score_threshold: Ngưỡng similarity score (optional)
            
        Returns:
            List of relevant Document objects
        """
        if self.vectorstore is None:
            raise ValueError("Vectorstore chưa được khởi tạo hoặc load")
        
        try:
            if score_threshold is not None:
                # Search với score threshold
                results = self.vectorstore.similarity_search_with_score(query, k=k)
                # Filter theo threshold
                results = [(doc, score) for doc, score in results if score >= score_threshold]
                return [doc for doc, _ in results]
            else:
                # Search thông thường
                return self.vectorstore.similarity_search(query, k=k)
                
        except Exception as e:
            print(f"❌ Lỗi khi tìm kiếm: {str(e)}")
            return []
    
    def similarity_search_with_score(self, 
                                    query: str, 
                                    k: int = 5) -> List[tuple]:
        """
        Tìm kiếm với similarity scores
        
        Args:
            query: Câu truy vấn
            k: Số lượng results
            
        Returns:
            List of (Document, score) tuples
        """
        if self.vectorstore is None:
            raise ValueError("Vectorstore chưa được khởi tạo hoặc load")
        
        try:
            return self.vectorstore.similarity_search_with_score(query, k=k)
        except Exception as e:
            print(f"❌ Lỗi khi tìm kiếm: {str(e)}")
            return []
    
    def get_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """
        Lấy retriever object cho RAG pipeline
        
        Args:
            search_kwargs: Các tham số cho search (k, score_threshold, etc.)
            
        Returns:
            Retriever object
        """
        if self.vectorstore is None:
            raise ValueError("Vectorstore chưa được khởi tạo hoặc load")
        
        if search_kwargs is None:
            search_kwargs = {
                'k': self.config['retrieval']['top_k'],
            }
        
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)


if __name__ == "__main__":
    # Test embedding manager
    from utils import load_config, load_environment
    from document_processor import DocumentProcessor
    
    config = load_config()
    env = load_environment()
    
    # Khởi tạo
    embedding_manager = EmbeddingManager(config, env)
    
    # Test search (nếu vectorstore đã tồn tại)
    if embedding_manager.load_vectorstore():
        results = embedding_manager.similarity_search("điều kiện tốt nghiệp", k=3)
        print(f"\n🔍 Tìm thấy {len(results)} results")
        for i, doc in enumerate(results, 1):
            print(f"\n[{i}] {doc.metadata.get('source', 'Unknown')}")
            print(doc.page_content[:200])







