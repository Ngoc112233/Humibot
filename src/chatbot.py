"""
Chatbot Module - Main RAG Pipeline
"""

import os
from typing import Dict, Any, List, Optional
import google.generativeai as genai

try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from src.embeddings import EmbeddingManager
from src.retriever import AdvancedRetriever
from src.utils import load_config, load_environment, setup_logging


class StudentSupportChatbot:
    """
    Chatbot hỗ trợ sinh viên sử dụng RAG
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Khởi tạo chatbot
        
        Args:
            config_path: Đường dẫn đến file config
        """
        # Load configuration
        self.config = load_config(config_path)
        self.env = load_environment()
        
        # Setup logging
        self.logger = setup_logging(
            log_file=self.config['logging']['file'],
            level=self.config['logging']['level']
        )
        
        # Initialize components
        self.embedding_manager = EmbeddingManager(self.config, self.env)
        
        # Load vectorstore
        if not self.embedding_manager.load_vectorstore():
            raise ValueError(
                "Vectorstore chưa được tạo. "
                "Vui lòng chạy scripts/process_documents.py trước."
            )
        
        # Initialize retriever
        self.retriever = AdvancedRetriever(self.embedding_manager, self.config)
        
        # Initialize LLM
        self.llm = self._initialize_llm()
        
        # Create prompt template
        self.prompt_template = self._create_prompt_template()
        
        self.logger.info("✅ Chatbot đã được khởi tạo thành công")
    
    def _initialize_llm(self):
        """
        Khởi tạo LLM dựa trên config
        
        Returns:
            LLM instance
        """
        provider = self.config['llm']['provider']
        model_name = self.config['llm']['model_name']
        
        self.logger.info(f"🤖 Khởi tạo LLM: {provider} - {model_name}")
        
        if provider == 'openai':
            if not self.env.get('openai_api_key'):
                raise ValueError("OPENAI_API_KEY không được cấu hình")
            
            return ChatOpenAI(
                model_name=model_name,
                temperature=self.config['llm']['temperature'],
                max_tokens=self.config['llm']['max_tokens'],
                openai_api_key=self.env['openai_api_key']
            )
        
        elif provider == 'gemini':
            if not self.env.get('google_api_key'):
                raise ValueError("GOOGLE_API_KEY không được cấu hình")
            
            # Configure Gemini
            genai.configure(api_key=self.env['google_api_key'])
            return genai.GenerativeModel(model_name)
        
        else:
            raise ValueError(f"LLM provider không được hỗ trợ: {provider}")
    
    def _create_prompt_template(self) -> str:
        """
        Tạo prompt template cho RAG
        
        Returns:
            Prompt template string
        """
        system_prompt = self.config['llm']['system_prompt']
        
        template = f"""{system_prompt}

CONTEXT (Thông tin từ tài liệu của trường):
{{context}}

QUESTION (Câu hỏi của sinh viên):
{{question}}

ANSWER (Câu trả lời của bạn):
"""
        return template
    
    def ask(self, 
            question: str, 
            include_sources: bool = True,
            **kwargs) -> Dict[str, Any]:
        """
        Trả lời câu hỏi của sinh viên
        
        Args:
            question: Câu hỏi
            include_sources: Có trả về nguồn tham khảo không
            **kwargs: Additional parameters (top_k, etc.)
            
        Returns:
            Dictionary chứa câu trả lời và metadata
        """
        self.logger.info(f"❓ Question: {question}")
        
        try:
            # Step 1: Retrieve relevant documents
            top_k = kwargs.get('top_k', self.config['retrieval']['top_k'])
            documents = self.retriever.retrieve(question, top_k=top_k)
            
            if not documents:
                return {
                    'question': question,
                    'answer': "Xin lỗi, tôi không tìm thấy thông tin liên quan đến câu hỏi của bạn trong cơ sở dữ liệu.",
                    'sources': [],
                    'confidence': 0.0
                }
            
            # Step 2: Create context from retrieved documents
            context = self.retriever.get_context_string(documents)
            
            # Step 3: Generate answer using LLM
            answer = self._generate_answer(question, context)
            
            # Step 4: Kiểm tra xem có phải câu trả lời "không biết" không
            no_answer_keywords = [
                'xin lỗi', 'không tìm thấy', 'không có thông tin',
                'không rõ', 'không biết', 'chưa có thông tin',
                'không tìm được', 'không có dữ liệu', 'không đề cập'
            ]
            
            is_no_answer = any(keyword in answer.lower() for keyword in no_answer_keywords)
            
            # Step 5: Get source references (chỉ khi có câu trả lời phù hợp)
            if is_no_answer:
                sources = []
            else:
                sources = self.retriever.get_source_references(documents) if include_sources else []
            
            response = {
                'question': question,
                'answer': answer,
                'sources': sources,
                'num_sources': len(documents)
            }
            
            self.logger.info(f"✅ Answer generated successfully (no_answer: {is_no_answer})")
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error: {str(e)}")
            return {
                'question': question,
                'answer': f"Xin lỗi, đã có lỗi xảy ra: {str(e)}",
                'sources': [],
                'error': str(e)
            }
    
    def _generate_answer(self, question: str, context: str) -> str:
        """
        Generate answer sử dụng LLM
        
        Args:
            question: Câu hỏi
            context: Context từ retrieved documents
            
        Returns:
            Generated answer
        """
        provider = self.config['llm']['provider']
        
        # Format prompt
        prompt = self.prompt_template.format(
            context=context,
            question=question
        )
        
        if provider == 'gemini':
            # Sử dụng Gemini API
            response = self.llm.generate_content(prompt)
            # Clean response text - remove HTML tags and file references
            answer = response.text.replace('</div>', '').strip()
            # Remove file references in parentheses at the end of the answer
            if answer.endswith(')'):
                last_open_paren = answer.rfind('(')
                if last_open_paren > 0 and '.txt' in answer[last_open_paren:]:
                    answer = answer[:last_open_paren].strip()
            return answer
        
        elif provider == 'openai':
            # Sử dụng OpenAI
            response = self.llm.invoke(prompt)
            # Clean response text - remove HTML tags and file references
            answer = response.content.replace('</div>', '').strip()
            # Remove file references in parentheses at the end of the answer
            if answer.endswith(')'):
                last_open_paren = answer.rfind('(')
                if last_open_paren > 0 and '.txt' in answer[last_open_paren:]:
                    answer = answer[:last_open_paren].strip()
            return answer
        
        else:
            raise ValueError(f"Provider không được hỗ trợ: {provider}")
    
    def chat(self, history: List[Dict[str, str]], question: str) -> Dict[str, Any]:
        """
        Multi-turn conversation với context history
        
        Args:
            history: List of previous Q&A pairs
            question: Current question
            
        Returns:
            Response dictionary
        """
        # TODO: Implement conversation history handling
        # For now, just treat as single question
        return self.ask(question)
    
    def format_response(self, response: Dict[str, Any]) -> str:
        """
        Format response để hiển thị cho user
        
        Args:
            response: Response dictionary từ ask()
            
        Returns:
            Formatted string
        """
        output = f"🤖 Trả lời:\n{response['answer']}\n"
        
        if response.get('sources'):
            output += "\n📚 Nguồn tham khảo:\n"
            for i, source in enumerate(response['sources'], 1):
                page_info = f" (Trang {source['page']})" if source['page'] else ""
                output += f"  {i}. {source['source']}{page_info}\n"
        
        return output


def main():
    """
    CLI interface cho chatbot
    """
    print("=" * 60)
    print("🎓 CHATBOT HỖ TRỢ SINH VIÊN")
    print("=" * 60)
    print("\nĐang khởi tạo chatbot...")
    
    try:
        chatbot = StudentSupportChatbot()
        print("✅ Chatbot đã sẵn sàng!\n")
        print("Hướng dẫn:")
        print("  - Nhập câu hỏi và nhấn Enter")
        print("  - Gõ 'exit' hoặc 'quit' để thoát\n")
        print("-" * 60)
        
        # Chat loop
        while True:
            # Get user input
            question = input("\n❓ Câu hỏi của bạn: ").strip()
            
            # Check exit
            if question.lower() in ['exit', 'quit', 'thoát']:
                print("\n👋 Cảm ơn bạn đã sử dụng chatbot. Hẹn gặp lại!")
                break
            
            if not question:
                continue
            
            # Get answer
            print("\n⏳ Đang tìm kiếm thông tin...")
            response = chatbot.ask(question)
            
            # Display response
            print("\n" + chatbot.format_response(response))
            print("-" * 60)
            
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        print("\nVui lòng kiểm tra:")
        print("  1. File .env đã được cấu hình đúng")
        print("  2. Vectorstore đã được tạo (chạy scripts/process_documents.py)")
        print("  3. API keys hợp lệ")


if __name__ == "__main__":
    main()

