"""
Streamlit Web Interface cho Student Support Chatbot
"""

import streamlit as st
from pathlib import Path
import sys
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.chatbot import StudentSupportChatbot
from src.utils import load_config


# Page configuration
st.set_page_config(
    page_title="Trợ Lý Ảo USSH - ĐHQG-HCM",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Modern and beautiful design
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 900px;
    }
    
    /* Header styling - USSH colors */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
        padding: 0.5rem 0;
    }
    
    .school-name {
        text-align: center;
        color: #1976d2;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .subtitle {
        text-align: center;
        color: #546e7a;
        font-size: 1.05rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1.2rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        animation: fadeIn 0.3s ease-in;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        color: white;
        margin-left: 20%;
        box-shadow: 0 2px 8px rgba(30, 136, 229, 0.3);
    }
    
    .user-message strong {
        color: white;
        opacity: 0.95;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #ffffff 0%, #f5f9ff 100%);
        color: #263238;
        margin-right: 20%;
        border-left: 4px solid #42a5f5;
        box-shadow: 0 2px 8px rgba(66, 165, 245, 0.15);
    }
    
    /* Source box */
    .source-box {
        background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        padding: 1rem;
        border-radius: 0.8rem;
        margin-top: 1rem;
        font-size: 0.9rem;
        border-left: 4px solid #ffa726;
        box-shadow: 0 2px 6px rgba(255, 167, 38, 0.15);
    }
    
    .source-box strong {
        color: #e65100;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e88e5 0%, #1565c0 100%);
    }
    
    /* Input box */
    .stChatInput {
        border-radius: 2rem;
    }
    
    /* Hide default streamlit branding */
    .st-emotion-cache-1y4p8pa {
        display: none;
    }
    
    /* Example questions */
    .example-question {
        background: #f8f9fa;
        padding: 0.8rem 1.2rem;
        border-radius: 2rem;
        margin: 0.5rem 0;
        border: 2px solid #e9ecef;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .example-question:hover {
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        color: white;
        border-color: #1976d2;
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
    }
    
    /* USSH Logo placeholder */
    .logo-container {
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1.2rem;
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        border-radius: 1rem;
        box-shadow: 0 6px 20px rgba(30, 136, 229, 0.4);
    }
    
    .logo-text {
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="🤖 Đang khởi tạo chatbot...")
def load_chatbot():
    """
    Load chatbot (cached để không phải reload mỗi lần)
    """
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return StudentSupportChatbot()
    except Exception as e:
        st.error("❌ Không thể khởi tạo chatbot")
        with st.expander("🔍 Chi tiết lỗi (dành cho admin)"):
            st.code(str(e))
            st.info("""
            **Các bước kiểm tra:**
            1. File .env đã có API keys chưa?
            2. Đã chạy `python scripts/process_documents.py`?
            3. Đã cài đặt dependencies?
            """)
        return None


def display_chat_message(role: str, content: str, sources: list = None):
    """
    Hiển thị chat message
    
    Args:
        role: 'user' hoặc 'assistant'
        content: Nội dung message
        sources: Danh sách nguồn tham khảo (nếu có)
    """
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 Bạn:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 Trợ lý:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
        
        # Display sources if available
        if sources:
            sources_html = "<div class='source-box'><strong>📚 Nguồn tham khảo:</strong><br>"
            for i, source in enumerate(sources, 1):
                page_info = f" (Trang {source['page']})" if source.get('page') else ""
                sources_html += f"{i}. {source['source']}{page_info}<br>"
            sources_html += "</div>"
            st.markdown(sources_html, unsafe_allow_html=True)


def main():
    """
    Main Streamlit app
    """
    # Logo và Header
    st.markdown('''
    <div class="logo-container">
        <p class="logo-text">🎓 ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH</p>
        <p class="logo-text" style="font-size: 0.95rem;">TRƯỜNG ĐẠI HỌC KHOA HỌC XÃ HỘI VÀ NHÂN VĂN</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">Trợ Lý Ảo USSH</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Giải đáp thắc mắc về quy định đào tạo, thủ tục hành chính và hoạt động sinh viên</p>', unsafe_allow_html=True)
    
    # Load config
    config = load_config()
    
    # Sidebar (collapsed by default) - chỉ hiện khi cần
    with st.sidebar:
        st.markdown("### ⚙️ Cài đặt")
        
        # Settings
        top_k = st.slider(
            "📚 Độ sâu tìm kiếm",
            min_value=1,
            max_value=10,
            value=config['retrieval']['top_k'],
            help="Số lượng tài liệu tham khảo"
        )
        
        include_sources = st.checkbox(
            "📖 Hiển thị nguồn",
            value=True,
            help="Hiển thị nguồn tài liệu"
        )
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Xóa lịch sử", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Examples
        st.markdown("### 💡 Câu hỏi thường gặp")
        example_questions = [
            "Điều kiện tốt nghiệp USSH?",
            "Quy định về điểm danh?",
            "Đăng ký môn học thế nào?",
            "Học phí và miễn giảm?",
            "Liên hệ phòng CTSV?"
        ]
        
        for i, question in enumerate(example_questions):
            if st.button(f"💬 {question}", key=f"ex_{i}", use_container_width=True):
                st.session_state.current_question = question
        
        st.markdown("---")
        
        # Compact info
        with st.expander("ℹ️ Về chatbot"):
            st.caption(f"""
            **Trường:** USSH - ĐHQG-HCM  
            **Chức năng:** Tra cứu thông tin, quy định  
            **Nguồn:** Văn bản chính thức của nhà trường  
            **AI Model:** {config['llm']['model_name'].split('/')[-1]}
            
            ---
            
            📧 **Phản hồi/Góp ý:** 
            Nếu có thông tin chưa chính xác, vui lòng liên hệ phòng Công tác Sinh viên.
            """)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = load_chatbot()
    
    # Check if chatbot is loaded
    if st.session_state.chatbot is None:
        st.stop()
        return
    
    # Welcome message khi mới vào
    if len(st.session_state.messages) == 0:
        st.info("""
        👋 **Chào mừng bạn đến với Trợ lý Ảo USSH!**
        
        Tôi có thể giúp bạn:
        - 📚 Tra cứu quy định đào tạo, thi cử
        - 📝 Hướng dẫn thủ tục hành chính
        - 💰 Thông tin về học phí, học bổng
        - 📞 Liên hệ các phòng ban
        
        Hãy đặt câu hỏi của bạn bên dưới!
        """)
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(
            message["role"],
            message["content"],
            message.get("sources")
        )
    
    # Chat input
    question = st.chat_input("💬 Nhập câu hỏi của bạn... (VD: Điều kiện tốt nghiệp tại USSH là gì?)")
    
    # Handle example question click
    if "current_question" in st.session_state:
        question = st.session_state.current_question
        del st.session_state.current_question
    
    # Process question
    if question:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })
        
        # Display user message
        display_chat_message("user", question)
        
        # Get bot response
        with st.spinner("🔍 Đang tìm kiếm thông tin..."):
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                response = st.session_state.chatbot.ask(
                    question,
                    include_sources=include_sources,
                    top_k=top_k
                )
        
        # Add bot message
        bot_message = {
            "role": "assistant",
            "content": response['answer'],
            "sources": response.get('sources', []) if include_sources else None
        }
        st.session_state.messages.append(bot_message)
        
        # Display bot message
        display_chat_message(
            "assistant",
            response['answer'],
            response.get('sources') if include_sources else None
        )
        
        # Rerun to update chat
        st.rerun()
    
    # Footer - USSH branding
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center; color: #1976d2; font-size: 0.75rem; padding: 1rem; border-top: 2px solid #e3f2fd;'>"
        "🎓 <strong>Trường ĐH Khoa học Xã hội và Nhân văn - ĐHQG-HCM</strong><br>"
        "<span style='color: #546e7a;'>💡 Đặt câu hỏi cụ thể để nhận được câu trả lời chính xác nhất</span>"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

