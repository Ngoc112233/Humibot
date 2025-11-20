"""
Retriever Module
Quản lý retrieval logic cho RAG system
"""

from typing import List, Dict, Any, Tuple

try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document


class AdvancedRetriever:
    """
    Advanced retriever với các tính năng mở rộng như re-ranking, filtering
    """
    
    def __init__(self, embedding_manager, config: Dict[str, Any]):
        """
        Khởi tạo Advanced Retriever
        
        Args:
            embedding_manager: EmbeddingManager instance
            config: Configuration dictionary
        """
        self.embedding_manager = embedding_manager
        self.config = config
        self.top_k = config['retrieval']['top_k']
        self.score_threshold = config['retrieval'].get('score_threshold', 0.0)
        self.use_rerank = config['retrieval'].get('rerank', False)
    
    def retrieve(self, query: str, **kwargs) -> List[Document]:
        """
        Retrieve relevant documents cho query
        
        Args:
            query: Câu truy vấn
            **kwargs: Additional parameters (top_k, filters, etc.)
            
        Returns:
            List of relevant Documents
        """
        top_k = kwargs.get('top_k', self.top_k)
        
        # Get documents with scores
        results = self.embedding_manager.similarity_search_with_score(
            query, 
            k=top_k
        )
        
        # Filter by score threshold
        if self.score_threshold > 0:
            results = [(doc, score) for doc, score in results 
                      if score >= self.score_threshold]
        
        # Apply metadata filters if provided
        metadata_filter = kwargs.get('metadata_filter')
        if metadata_filter:
            results = self._apply_metadata_filter(results, metadata_filter)
        
        # Re-ranking (nếu enabled)
        if self.use_rerank and len(results) > 0:
            results = self._rerank_results(query, results)
        
        # Return documents only (without scores)
        documents = [doc for doc, _ in results]
        
        return documents
    
    def retrieve_with_scores(self, query: str, **kwargs) -> List[Tuple[Document, float]]:
        """
        Retrieve documents kèm theo similarity scores
        
        Args:
            query: Câu truy vấn
            **kwargs: Additional parameters
            
        Returns:
            List of (Document, score) tuples
        """
        top_k = kwargs.get('top_k', self.top_k)
        
        results = self.embedding_manager.similarity_search_with_score(query, k=top_k)
        
        # Filter by score threshold
        if self.score_threshold > 0:
            results = [(doc, score) for doc, score in results 
                      if score >= self.score_threshold]
        
        return results
    
    def _apply_metadata_filter(self, 
                               results: List[Tuple[Document, float]], 
                               filters: Dict[str, Any]) -> List[Tuple[Document, float]]:
        """
        Filter results dựa trên metadata
        
        Args:
            results: List of (Document, score) tuples
            filters: Dictionary chứa các điều kiện filter
            
        Returns:
            Filtered results
        """
        filtered = []
        
        for doc, score in results:
            match = True
            for key, value in filters.items():
                if doc.metadata.get(key) != value:
                    match = False
                    break
            
            if match:
                filtered.append((doc, score))
        
        return filtered
    
    def _rerank_results(self, 
                       query: str, 
                       results: List[Tuple[Document, float]]) -> List[Tuple[Document, float]]:
        """
        Re-rank results sử dụng cross-encoder hoặc heuristics
        
        Args:
            query: Original query
            results: Initial results
            
        Returns:
            Re-ranked results
        """
        # TODO: Implement re-ranking với cross-encoder
        # Placeholder: Giữ nguyên order hiện tại
        return results
    
    def get_context_string(self, documents: List[Document]) -> str:
        """
        Chuyển đổi list documents thành context string cho LLM
        
        Args:
            documents: List of retrieved Documents
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "Không tìm thấy thông tin liên quan."
        
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', '')
            page_info = f" (Trang {page})" if page else ""
            
            context_parts.append(
                f"[Tài liệu {i}] Nguồn: {source}{page_info}\n"
                f"{doc.page_content}\n"
            )
        
        return "\n".join(context_parts)
    
    def get_source_references(self, documents: List[Document]) -> List[Dict[str, str]]:
        """
        Lấy danh sách nguồn tham khảo từ documents
        
        Args:
            documents: List of Documents
            
        Returns:
            List of source reference dictionaries
        """
        sources = []
        seen = set()
        
        for doc in documents:
            source_id = (
                doc.metadata.get('source', 'Unknown'),
                doc.metadata.get('page', '')
            )
            
            # Tránh duplicate
            if source_id not in seen:
                sources.append({
                    'source': doc.metadata.get('source', 'Unknown'),
                    'page': doc.metadata.get('page', ''),
                    'file_type': doc.metadata.get('file_type', ''),
                })
                seen.add(source_id)
        
        return sources


class HybridRetriever(AdvancedRetriever):
    """
    Hybrid retriever kết hợp semantic search và keyword search
    """
    
    def __init__(self, embedding_manager, config: Dict[str, Any]):
        super().__init__(embedding_manager, config)
        self.semantic_weight = 0.7  # Trọng số cho semantic search
        self.keyword_weight = 0.3   # Trọng số cho keyword search
    
    def retrieve(self, query: str, **kwargs) -> List[Document]:
        """
        Retrieve sử dụng hybrid approach
        
        Args:
            query: Câu truy vấn
            **kwargs: Additional parameters
            
        Returns:
            List of relevant Documents
        """
        # Semantic search
        semantic_results = super().retrieve_with_scores(query, **kwargs)
        
        # Keyword search (simple implementation)
        keyword_results = self._keyword_search(query, **kwargs)
        
        # Combine and re-rank
        combined = self._combine_results(semantic_results, keyword_results)
        
        return [doc for doc, _ in combined[:self.top_k]]
    
    def _keyword_search(self, query: str, **kwargs) -> List[Tuple[Document, float]]:
        """
        Simple keyword-based search
        
        Args:
            query: Câu truy vấn
            **kwargs: Additional parameters
            
        Returns:
            List of (Document, score) tuples
        """
        # TODO: Implement proper keyword search (BM25, etc.)
        # Placeholder: Return empty list
        return []
    
    def _combine_results(self, 
                        semantic_results: List[Tuple[Document, float]],
                        keyword_results: List[Tuple[Document, float]]) -> List[Tuple[Document, float]]:
        """
        Kết hợp và tính điểm cho cả semantic và keyword results
        
        Args:
            semantic_results: Results từ semantic search
            keyword_results: Results từ keyword search
            
        Returns:
            Combined and sorted results
        """
        # Simple implementation: Weighted combination
        doc_scores = {}
        
        # Add semantic scores
        for doc, score in semantic_results:
            doc_id = id(doc)
            doc_scores[doc_id] = (doc, score * self.semantic_weight)
        
        # Add keyword scores
        for doc, score in keyword_results:
            doc_id = id(doc)
            if doc_id in doc_scores:
                existing_doc, existing_score = doc_scores[doc_id]
                doc_scores[doc_id] = (existing_doc, existing_score + score * self.keyword_weight)
            else:
                doc_scores[doc_id] = (doc, score * self.keyword_weight)
        
        # Sort by combined score
        sorted_results = sorted(doc_scores.values(), key=lambda x: x[1], reverse=True)
        
        return sorted_results


if __name__ == "__main__":
    # Test retriever
    from utils import load_config, load_environment
    from embeddings import EmbeddingManager
    
    config = load_config()
    env = load_environment()
    
    embedding_manager = EmbeddingManager(config, env)
    
    if embedding_manager.load_vectorstore():
        retriever = AdvancedRetriever(embedding_manager, config)
        
        # Test query
        query = "Quy định về điểm thi và xét tốt nghiệp"
        docs = retriever.retrieve(query)
        
        print(f"\n🔍 Query: {query}")
        print(f"📄 Tìm thấy {len(docs)} documents\n")
        
        # Print context
        context = retriever.get_context_string(docs)
        print("Context:")
        print(context)
        
        # Print sources
        sources = retriever.get_source_references(docs)
        print("\n📚 Nguồn tham khảo:")
        for source in sources:
            print(f"  - {source['source']} {source['page']}")







