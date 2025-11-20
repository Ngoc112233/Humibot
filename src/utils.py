"""
Utility functions cho chatbot system
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load cấu hình từ file YAML
    
    Args:
        config_path: Đường dẫn đến file config
        
    Returns:
        Dictionary chứa cấu hình
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def load_environment() -> Dict[str, Optional[str]]:
    """
    Load environment variables từ file .env
    
    Returns:
        Dictionary chứa các environment variables
    """
    load_dotenv()
    
    return {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'google_api_key': os.getenv('GOOGLE_API_KEY'),
        'huggingface_api_key': os.getenv('HUGGINGFACE_API_KEY'),
        'llm_provider': os.getenv('LLM_PROVIDER', 'gemini'),
        'embedding_model': os.getenv('EMBEDDING_MODEL', 'sentence-transformers'),
    }


def setup_logging(log_file: str = "logs/chatbot.log", level: str = "INFO") -> logging.Logger:
    """
    Thiết lập logging cho hệ thống
    
    Args:
        log_file: Đường dẫn file log
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Logger instance
    """
    # Tạo thư mục logs nếu chưa tồn tại
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Cấu hình logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def ensure_directory(directory: str) -> Path:
    """
    Đảm bảo thư mục tồn tại, tạo nếu chưa có
    
    Args:
        directory: Đường dẫn thư mục
        
    Returns:
        Path object
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Đếm số lượng tokens trong text
    
    Args:
        text: Text cần đếm
        model: Model name để chọn tokenizer phù hợp
        
    Returns:
        Số lượng tokens
    """
    try:
        import tiktoken
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        # Fallback: ước lượng đơn giản (1 token ~ 4 ký tự)
        return len(text) // 4


def format_sources(sources: list, max_length: int = 200) -> str:
    """
    Format danh sách sources thành string hiển thị
    
    Args:
        sources: List các source documents
        max_length: Độ dài tối đa của mỗi source
        
    Returns:
        Formatted string
    """
    formatted = []
    for i, source in enumerate(sources, 1):
        content = source.page_content[:max_length]
        if len(source.page_content) > max_length:
            content += "..."
        
        metadata = source.metadata
        source_info = f"[{i}] {metadata.get('source', 'Unknown')}"
        if 'page' in metadata:
            source_info += f" (Trang {metadata['page']})"
        
        formatted.append(f"{source_info}\n{content}")
    
    return "\n\n".join(formatted)


def validate_api_keys(config: Dict[str, Any], env: Dict[str, Optional[str]]) -> bool:
    """
    Kiểm tra xem các API keys cần thiết đã được cấu hình chưa
    
    Args:
        config: Configuration dictionary
        env: Environment variables dictionary
        
    Returns:
        True nếu valid, False nếu thiếu keys
    """
    llm_provider = config['llm']['provider']
    embedding_provider = config['embedding']['provider']
    
    required_keys = []
    
    # Check LLM provider
    if llm_provider == 'openai':
        required_keys.append(('OPENAI_API_KEY', env['openai_api_key']))
    elif llm_provider == 'gemini':
        required_keys.append(('GOOGLE_API_KEY', env['google_api_key']))
    elif llm_provider == 'huggingface':
        required_keys.append(('HUGGINGFACE_API_KEY', env['huggingface_api_key']))
    
    # Check embedding provider
    if embedding_provider == 'openai':
        required_keys.append(('OPENAI_API_KEY', env['openai_api_key']))
    
    # Validate
    missing_keys = [key for key, value in required_keys if not value]
    
    if missing_keys:
        print(f"⚠️  Thiếu API keys: {', '.join(missing_keys)}")
        print("Vui lòng tạo file .env và thêm các keys cần thiết.")
        return False
    
    return True







