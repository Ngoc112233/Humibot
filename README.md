# 🎓 Trợ Lý Ảo USSH - Hệ Thống Chatbot RAG

<div align="center">

**Chatbot hỗ trợ sinh viên thông minh sử dụng công nghệ RAG (Retrieval-Augmented Generation)**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)](https://python.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io/)

</div>

---

## 📋 Mục Lục

- [Tổng Quan](#-tổng-quan)
- [Tính Năng](#-tính-năng)
- [Kiến Trúc Hệ Thống](#-kiến-trúc-hệ-thống)
- [Công Nghệ Sử Dụng](#-công-nghệ-sử-dụng)
- [Cài Đặt](#-cài-đặt)
- [Cấu Hình](#-cấu-hình)
- [Sử Dụng](#-sử-dụng)
- [Cấu Trúc Dự Án](#-cấu-trúc-dự-án)
- [Quy Trình Hoạt Động](#-quy-trình-hoạt-động)
- [Tối Ưu Hóa](#-tối-ưu-hóa)
- [Xử Lý Lỗi](#-xử-lý-lỗi)
- [Roadmap](#-roadmap)

---

## 🌟 Tổng Quan

Hệ thống Trợ Lý Ảo USSH là một chatbot thông minh được thiết kế đặc biệt để hỗ trợ sinh viên **Trường Đại học Khoa học Xã hội và Nhân văn - ĐHQG-HCM (USSH)**. Chatbot sử dụng công nghệ RAG (Retrieval-Augmented Generation) tiên tiến để:

- 📚 Trả lời câu hỏi về quy định đào tạo, thi cử
- 📝 Hướng dẫn các thủ tục hành chính
- 💰 Cung cấp thông tin về học phí, học bổng
- 📞 Hướng dẫn liên hệ các phòng ban
- ℹ️ Giải đáp thắc mắc chung về hoạt động sinh viên

### Đặc điểm nổi bật:

✅ **Chính xác**: Trả lời dựa trên văn bản chính thức của nhà trường  
✅ **Nhanh chóng**: Phản hồi trong vài giây  
✅ **Dễ sử dụng**: Giao diện thân thiện, hiện đại  
✅ **Minh bạch**: Hiển thị nguồn tham khảo cho mỗi câu trả lời  
✅ **Linh hoạt**: Hỗ trợ nhiều định dạng tài liệu và LLM providers

---

## ⚡ Tính Năng

### 🔍 Xử Lý Tài Liệu Đa Dạng

- **Hỗ trợ nhiều định dạng**: PDF, DOCX, TXT, Markdown
- **OCR tài liệu scan**: Tự động nhận dạng và trích xuất text từ PDF scan
- **Xử lý hàng loạt**: Tự động load và xử lý toàn bộ thư mục documents
- **Chunking thông minh**: Chia nhỏ tài liệu với RecursiveCharacterTextSplitter
- **Metadata tracking**: Theo dõi nguồn, số trang, loại file

### 🤖 Hệ Thống RAG Nâng Cao

- **Multi-provider LLM**:
  - Google Gemini (miễn phí, khuyến nghị)
  - OpenAI GPT (trả phí, chất lượng cao)
  - Dễ dàng mở rộng thêm providers khác

- **Flexible Embeddings**:
  - Sentence Transformers (local, miễn phí)
  - OpenAI Embeddings (API, trả phí)
  - Hỗ trợ model tiếng Việt: `keepitreal/vietnamese-sbert`

- **Vector Database Options**:
  - ChromaDB (persistent, dễ sử dụng)
  - FAISS (nhanh, hiệu quả)

### 🎯 Retrieval Thông Minh

- **Similarity Search**: Tìm kiếm semantic với cosine similarity
- **Score Filtering**: Lọc kết quả theo ngưỡng similarity score
- **Metadata Filtering**: Lọc theo loại tài liệu, phòng ban, etc.
- **Re-ranking**: Hỗ trợ re-rank kết quả (optional)
- **Hybrid Retrieval**: Kết hợp semantic và keyword search (experimental)

### 🎨 Giao Diện Đa Dạng

#### Web Interface (Streamlit)
- 🎨 Giao diện đẹp với theme USSH chuyên nghiệp
- 💬 Chat UI hiện đại với animation
- 📚 Hiển thị nguồn tham khảo rõ ràng
- ⚙️ Sidebar với cài đặt động
- 💡 Gợi ý câu hỏi thường gặp
- 📱 Responsive design

#### CLI Interface
- 🖥️ Giao diện dòng lệnh đơn giản
- ⚡ Nhanh chóng, tiện lợi cho testing
- 📝 In kết quả có format đẹp

### 📊 Logging và Monitoring

- **Chi tiết**: Log mọi query và response
- **Structured**: Format rõ ràng với timestamp
- **Debugging**: Hỗ trợ các level: DEBUG, INFO, WARNING, ERROR
- **File-based**: Lưu trữ lịch sử trong `logs/chatbot.log`

### 🔧 Cấu Hình Linh Hoạt

- **YAML Configuration**: Cấu hình tập trung trong `config/config.yaml`
- **Environment Variables**: API keys và secrets trong `.env`
- **Hot-swappable**: Thay đổi LLM/embedding provider dễ dàng
- **Customizable Prompts**: Tùy chỉnh system prompt

---

## 🏗️ Kiến Trúc Hệ Thống

```
┌──────────────────────────────────────────────────────────────┐
│                    DOCUMENT SOURCES                          │
│         (PDF, DOCX, TXT, MD - Regular & Scanned)            │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                 DOCUMENT PROCESSING                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  OCR (scan)  │→ │ Text Extract │→ │ Text Chunking   │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                   EMBEDDING LAYER                            │
│         (Sentence-BERT / OpenAI Embeddings)                  │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                  VECTOR DATABASE                             │
│              (ChromaDB / FAISS)                              │
└───────┬──────────────────────────────────────────────────────┘
        │                                          ▲
        │                                          │
        ▼                                          │
┌─────────────────┐                    ┌──────────────────────┐
│  USER QUERY     │                    │   RETRIEVER          │
│  (Câu hỏi SV)   │───────────────────▶│ - Similarity Search  │
└─────────────────┘                    │ - Score Filter       │
                                       │ - Re-ranking         │
                                       └──────────┬───────────┘
                                                  │
                                                  ▼
                                       ┌──────────────────────┐
                                       │    LLM GENERATION    │
                                       │  (Gemini / OpenAI)   │
                                       └──────────┬───────────┘
                                                  │
                                                  ▼
                                       ┌──────────────────────┐
                                       │   FINAL ANSWER       │
                                       │  + Source Citations  │
                                       └──────────────────────┘
```

---

## 🛠️ Công Nghệ Sử Dụng

### Core Framework
- **LangChain**: Framework RAG chính
- **Python 3.8+**: Ngôn ngữ lập trình

### LLM Providers
- **Google Gemini 2.0 Flash**: LLM mặc định (miễn phí, nhanh)
- **OpenAI GPT-4/3.5**: Optional (trả phí)

### Embeddings
- **Sentence Transformers**: 
  - `keepitreal/vietnamese-sbert` (tiếng Việt)
  - `intfloat/multilingual-e5-base` (multilingual)
- **OpenAI text-embedding-ada-002**: Optional

### Vector Databases
- **ChromaDB**: Local, persistent storage
- **FAISS**: Fast similarity search

### Document Processing
- **PyPDF2**: PDF reading
- **pdfplumber**: Advanced PDF parsing
- **python-docx**: Word document processing
- **Tesseract OCR + pdf2image**: OCR cho PDF scan

### Frontend
- **Streamlit**: Web interface framework
- **Custom CSS**: USSH-branded design

### Utilities
- **python-dotenv**: Environment management
- **PyYAML**: Configuration management
- **tqdm**: Progress bars
- **logging**: System logging

---

## 🚀 Cài Đặt

### Yêu Cầu Hệ Thống

- **Python**: 3.8 trở lên
- **RAM**: 4GB tối thiểu (8GB khuyến nghị)
- **Disk**: 2GB cho models và data
- **OS**: Windows, macOS, Linux
- **Internet**: Cần kết nối để download models và sử dụng API

### Bước 1: Clone Repository

```bash
git clone https://github.com/your-repo/chatbot-ussh.git
cd chatbot-ussh
```

### Bước 2: Tạo Virtual Environment (Khuyến nghị)

```bash
# Tạo virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Bước 3: Cài Đặt Dependencies

```bash
pip install --upgrade pip
pip install langchain langchain-community langchain-openai
pip install chromadb sentence-transformers
pip install streamlit python-dotenv pyyaml
pip install pypdf2 pdfplumber python-docx
pip install pytesseract pdf2image pillow
pip install tqdm google-generativeai
```

**Lưu ý**: Nếu sử dụng OCR, cần cài đặt Tesseract:
- **macOS**: `brew install tesseract tesseract-lang`
- **Ubuntu**: `sudo apt-get install tesseract-ocr tesseract-ocr-vie`
- **Windows**: Download từ [GitHub Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

### Bước 4: Cấu Hình API Keys

Tạo file `.env` trong thư mục gốc:

```bash
# Chọn 1 trong các options sau:

# Option 1: Google Gemini (KHUYẾN NGHỊ - Miễn phí)
GOOGLE_API_KEY=your_google_api_key_here

# Option 2: OpenAI (Trả phí)
OPENAI_API_KEY=sk-your_openai_key_here

# Option 3: HuggingFace (Nếu dùng HF models)
HUGGINGFACE_API_KEY=hf_your_token_here
```

**Lấy API Keys**:
- **Google Gemini**: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- **OpenAI**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Bước 5: Chuẩn Bị Documents

```bash
# Tạo thư mục documents
mkdir -p data/documents

# Thêm tài liệu của bạn vào thư mục này
# Ví dụ:
# data/documents/quy_che_dao_tao.pdf
# data/documents/quy_dinh_thi_cử.pdf
# data/documents/huong_dan_dkhp.docx
```

### Bước 6: (Optional) OCR PDF Scan

Nếu có PDF scan, chạy OCR trước:

```bash
python scripts/ocr_pdfs.py
```

Script sẽ:
- Tự động phát hiện PDF scan
- OCR và tạo file TXT
- Lưu kết quả vào `data/documents/`

### Bước 7: Xử Lý Documents và Tạo Vectorstore

```bash
python scripts/process_documents.py
```

Script sẽ:
1. Load tất cả documents từ `data/documents/`
2. Chia thành chunks
3. Tạo embeddings
4. Lưu vào vector database

⏱️ **Thời gian**: 1-5 phút tùy số lượng documents

### Bước 8: Chạy Chatbot!

**Option A: Web Interface (Khuyến nghị)**

```bash
streamlit run app.py
```

Truy cập: [http://localhost:8501](http://localhost:8501)

**Option B: CLI Interface**

```bash
python chatbot.py
```

---

## ⚙️ Cấu Hình

### File `config/config.yaml`

#### Document Processing

```yaml
document_processing:
  supported_formats: [pdf, docx, txt, md]
  chunk_size: 1000          # Kích thước mỗi chunk (ký tự)
  chunk_overlap: 200        # Độ overlap giữa các chunks
  separators: ["\n\n", "\n", " ", ""]
```

#### Embeddings

```yaml
embedding:
  provider: "sentence-transformers"  # hoặc "openai"
  model_name: "keepitreal/vietnamese-sbert"  # Model tiếng Việt
  batch_size: 32
```

**Các model embeddings khác**:
- `intfloat/multilingual-e5-base` (multilingual, tốt)
- `all-MiniLM-L6-v2` (English, nhanh)
- `text-embedding-ada-002` (OpenAI, trả phí)

#### Vector Database

```yaml
vectorstore:
  type: "chromadb"              # hoặc "faiss"
  persist_directory: "./data/vectorstore"
  collection_name: "student_support_docs"
  distance_metric: "cosine"
```

#### LLM Configuration

```yaml
llm:
  provider: "gemini"            # hoặc "openai"
  model_name: "models/gemini-2.0-flash"
  temperature: 0.7              # 0.0 - 1.0 (cao = sáng tạo hơn)
  max_tokens: 1500
  top_p: 0.9
  
  system_prompt: |
    Bạn là trợ lý ảo hỗ trợ sinh viên của trường đại học.
    Nhiệm vụ của bạn là trả lời các câu hỏi của sinh viên dựa trên 
    thông tin từ các văn bản, quy định của trường.
    
    Hãy trả lời một cách:
    - Chính xác dựa trên thông tin được cung cấp
    - Rõ ràng, dễ hiểu
    - Thân thiện và lịch sự
    - Nếu không có thông tin, hãy nói rõ là bạn không tìm thấy thông tin
```

#### Retrieval Settings

```yaml
retrieval:
  top_k: 5                      # Số chunks retrieve
  score_threshold: 0.5          # Ngưỡng similarity tối thiểu
  rerank: false                 # Có re-rank không
```

#### Response Configuration

```yaml
response:
  language: "vi"                # vi hoặc en
  include_sources: true         # Hiển thị nguồn
  max_source_length: 200
  stream: false
```

#### Logging

```yaml
logging:
  level: "INFO"                 # DEBUG, INFO, WARNING, ERROR
  file: "./logs/chatbot.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

---

## 💡 Sử Dụng

### Web Interface

1. **Khởi động**: `streamlit run app.py`
2. **Đặt câu hỏi**: Nhập câu hỏi vào ô chat
3. **Xem kết quả**: Đọc câu trả lời và nguồn tham khảo
4. **Điều chỉnh**: Sử dụng sidebar để thay đổi cài đặt

**Tính năng Web UI**:
- 💬 Chat history
- 📚 Hiển thị nguồn tham khảo chi tiết
- ⚙️ Điều chỉnh `top_k` (độ sâu tìm kiếm)
- 🗑️ Xóa lịch sử chat
- 💡 Câu hỏi gợi ý

### CLI Interface

```bash
python chatbot.py
```

```
🎓 CHATBOT HỖ TRỢ SINH VIÊN
------------------------------------------------------------
Đang khởi tạo chatbot...
✅ Chatbot đã sẵn sàng!

Hướng dẫn:
  - Nhập câu hỏi và nhấn Enter
  - Gõ 'exit' hoặc 'quit' để thoát
------------------------------------------------------------

❓ Câu hỏi của bạn: Điều kiện tốt nghiệp USSH là gì?

⏳ Đang tìm kiếm thông tin...

🤖 Trả lời:
Theo quy định của USSH, sinh viên được xét tốt nghiệp khi đáp ứng đủ các điều kiện sau:
1. Hoàn thành đủ số tín chỉ theo chương trình đào tạo
2. Điểm trung bình tích lũy đạt từ 2.0 trở lên
3. Không vi phạm kỷ luật ở mức phải đình chỉ học tập trở lên
...

📚 Nguồn tham khảo:
  1. quy_che_dao_tao.pdf (Trang 15)
  2. quy_dinh_tot_nghiep.pdf (Trang 3)
```

### Python API

```python
from src.chatbot import StudentSupportChatbot

# Khởi tạo chatbot
chatbot = StudentSupportChatbot()

# Đặt câu hỏi
response = chatbot.ask(
    question="Làm thế nào để đăng ký môn học?",
    include_sources=True,
    top_k=5
)

# Lấy câu trả lời
print(response['answer'])

# Lấy nguồn
for source in response['sources']:
    print(f"- {source['source']}")
```

### Update Documents

Khi có tài liệu mới:

```bash
# Option 1: Thêm vào vectorstore hiện tại
python scripts/update_vectorstore.py

# Option 2: Tạo lại vectorstore từ đầu
python scripts/process_documents.py
# Chọn [1] để xóa và tạo mới
```

---

## 📁 Cấu Trúc Dự Án

```
chatbot-ussh/
├── README.md                    # Tài liệu này
├── QUICKSTART.md               # Hướng dẫn nhanh
├── .env                        # API keys (không commit)
├── .gitignore
│
├── config/
│   └── config.yaml             # Cấu hình hệ thống
│
├── data/
│   ├── documents/              # Tài liệu gốc (PDF, DOCX, TXT)
│   │   ├── quy_che_dao_tao.pdf
│   │   ├── quy_dinh_thi.pdf
│   │   └── ...
│   └── vectorstore/            # Vector database
│       ├── chroma.sqlite3
│       └── ...
│
├── logs/
│   └── chatbot.log             # System logs
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── chatbot.py              # Main chatbot logic
│   ├── document_processor.py   # Xử lý documents
│   ├── embeddings.py           # Embedding management
│   ├── retriever.py            # Retrieval logic
│   └── utils.py                # Utility functions
│
├── scripts/                    # Utility scripts
│   ├── ocr_pdfs.py            # OCR PDF scan
│   ├── process_documents.py    # Xử lý và index docs
│   └── update_vectorstore.py   # Update vectorstore
│
├── app.py                      # Streamlit web app
├── chatbot.py                  # CLI interface
│
├── examples/                   # Code examples
│   ├── example_usage.py
│   └── sample_document.txt
│
└── tests/                      # Unit tests
    └── test_chatbot.py
```

---

## 🔄 Quy Trình Hoạt Động

### Phase 1: Xử Lý Dữ Liệu (One-time Setup)

```
Documents (PDF/DOCX/TXT)
        ↓
    [OCR nếu cần]
        ↓
    Load Documents
        ↓
    Extract Text
        ↓
    Text Chunking
    (chunks 1000 ký tự, overlap 200)
        ↓
    Generate Embeddings
    (Vietnamese SBERT)
        ↓
    Store in Vector DB
    (ChromaDB)
```

### Phase 2: Trả Lời Câu Hỏi (Real-time)

```
User Question
        ↓
    Embed Question
        ↓
    Similarity Search
    (cosine similarity)
        ↓
    Retrieve Top-K Chunks
    (k=5, score > 0.5)
        ↓
    Create Context
    (combine chunks)
        ↓
    LLM Generation
    (Gemini 2.0 Flash)
        ↓
    Format Response
    + Source Citations
        ↓
    Return to User
```

### Retrieval Details

1. **Embedding Query**: Chuyển câu hỏi thành vector
2. **Vector Search**: Tìm top-k vectors gần nhất trong database
3. **Score Filtering**: Loại bỏ kết quả có score thấp
4. **Metadata Filtering**: Lọc theo loại tài liệu (optional)
5. **Re-ranking**: Sắp xếp lại theo relevance (optional)
6. **Context Assembly**: Kết hợp chunks thành context

### LLM Prompting

```
System Prompt:
- Vai trò: Trợ lý ảo sinh viên
- Yêu cầu: Chính xác, rõ ràng, thân thiện

Context:
- Top-K retrieved chunks
- Metadata (source, page)

Question:
- Câu hỏi của sinh viên

Output:
- Câu trả lời
- Source citations
```

---

## 🎯 Tối Ưu Hóa

### 1. Cải Thiện Chất Lượng Trả Lời

#### Tối ưu Retrieval

```yaml
# config/config.yaml
retrieval:
  top_k: 7                  # Tăng để có nhiều context hơn
  score_threshold: 0.6      # Tăng để lọc kết quả kém
  rerank: true              # Bật re-ranking
```

#### Tối ưu LLM

```yaml
llm:
  temperature: 0.5          # Giảm để câu trả lời ổn định hơn
  max_tokens: 2000          # Tăng cho câu trả lời dài
```

#### Tối ưu Chunking

```yaml
document_processing:
  chunk_size: 800           # Giảm cho chunks ngắn hơn, cụ thể hơn
  chunk_overlap: 150        # Tăng để giữ context tốt hơn
```

#### Fine-tune System Prompt

Chỉnh sửa `system_prompt` trong `config.yaml` để phù hợp với use case:

```yaml
system_prompt: |
  Bạn là trợ lý ảo của Trường Đại học Khoa học Xã hội và Nhân văn - ĐHQG-HCM.
  
  NHIỆM VỤ:
  - Trả lời câu hỏi của sinh viên dựa trên tài liệu chính thức
  - Luôn trích dẫn nguồn thông tin
  - Nếu không chắc chắn, nói rõ và hướng dẫn liên hệ phòng ban
  
  PHONG CÁCH:
  - Thân thiện, lịch sự
  - Rõ ràng, dễ hiểu
  - Chuyên nghiệp nhưng gần gũi
  
  LƯU Ý:
  - KHÔNG bịa đặt thông tin
  - KHÔNG đưa ra ý kiến cá nhân
  - Luôn dựa vào tài liệu được cung cấp
```

### 2. Tăng Tốc Độ

#### Sử dụng FAISS thay vì ChromaDB

```yaml
vectorstore:
  type: "faiss"             # Nhanh hơn ChromaDB
```

#### Giảm Top-K

```yaml
retrieval:
  top_k: 3                  # Giảm số chunks retrieve
```

#### Cache Embeddings

```python
# Trong code, embeddings đã được cache sẵn
# Không cần re-compute cho mỗi query
```

### 3. Tiết Kiệm Chi Phí

#### Sử dụng Local Models

```yaml
embedding:
  provider: "sentence-transformers"  # Miễn phí
  model_name: "keepitreal/vietnamese-sbert"

llm:
  provider: "gemini"                 # Free tier
  model_name: "models/gemini-2.0-flash"
```

#### Giảm Token Usage

```yaml
llm:
  max_tokens: 1000          # Giảm tokens
retrieval:
  top_k: 3                  # Ít context = ít tokens
```

### 4. Scale Cho Production

#### Batch Processing

```python
# Xử lý nhiều documents cùng lúc
embedding_manager.add_documents(documents)  # Batch add
```

#### Caching

```python
# Streamlit tự động cache
@st.cache_resource
def load_chatbot():
    return StudentSupportChatbot()
```

#### Load Balancing

Nếu triển khai production, cân nhắc:
- Multiple Streamlit instances
- Load balancer (nginx)
- Redis cache cho responses
- Async processing

---

## 🐛 Xử Lý Lỗi

### Lỗi: "GOOGLE_API_KEY không được cấu hình"

**Nguyên nhân**: File `.env` chưa có hoặc API key sai

**Giải pháp**:
```bash
# Tạo file .env
echo "GOOGLE_API_KEY=your_key_here" > .env

# Hoặc export trực tiếp
export GOOGLE_API_KEY=your_key_here
```

### Lỗi: "Vectorstore chưa được tạo"

**Nguyên nhân**: Chưa chạy script xử lý documents

**Giải pháp**:
```bash
python scripts/process_documents.py
```

### Lỗi: Module not found

**Nguyên nhân**: Thiếu dependencies

**Giải pháp**:
```bash
pip install langchain langchain-community chromadb streamlit
# Xem phần Cài Đặt để biết list đầy đủ
```

### Lỗi: OCR không hoạt động

**Nguyên nhân**: Tesseract chưa được cài

**Giải pháp**:
```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu
sudo apt-get install tesseract-ocr tesseract-ocr-vie

# Windows: Download và cài đặt từ GitHub
```

### Lỗi: Out of memory

**Nguyên nhân**: Quá nhiều documents hoặc chunks quá lớn

**Giải pháp**:
```yaml
# Giảm batch size
embedding:
  batch_size: 16

# Hoặc giảm chunk size
document_processing:
  chunk_size: 500
```

### Lỗi: Câu trả lời không chính xác

**Nguyên nhân**: Retrieval không tốt hoặc prompt chưa phù hợp

**Giải pháp**:
1. Tăng `top_k` để có nhiều context hơn
2. Điều chỉnh `system_prompt`
3. Kiểm tra quality của documents
4. Thử model embedding khác

### Lỗi: Streamlit không khởi động

**Nguyên nhân**: Port 8501 đã được sử dụng

**Giải pháp**:
```bash
# Sử dụng port khác
streamlit run app.py --server.port 8502
```

### Debug Mode

Để debug chi tiết:

```yaml
# config/config.yaml
logging:
  level: "DEBUG"
```

Xem logs:
```bash
tail -f logs/chatbot.log
```

---

## 🚀 Roadmap

### ✅ Đã Hoàn Thành

- [x] RAG pipeline cơ bản
- [x] Hỗ trợ nhiều định dạng tài liệu
- [x] OCR cho PDF scan
- [x] Web interface với Streamlit
- [x] CLI interface
- [x] Multi-provider LLM (Gemini, OpenAI)
- [x] Vietnamese embedding support
- [x] Source citations
- [x] Logging system
- [x] YAML configuration

### 🔄 Đang Phát Triển

- [ ] Re-ranking với cross-encoder
- [ ] Hybrid retrieval (semantic + keyword)
- [ ] Multi-turn conversation với history
- [ ] User feedback system
- [ ] Analytics dashboard

### 📋 Kế Hoạch Tương Lai

#### Phase 2: Enhanced Features
- [ ] **Voice Interface**: Chat bằng giọng nói
- [ ] **Multi-language**: Hỗ trợ tiếng Anh
- [ ] **Document Upload**: Upload trực tiếp trong UI
- [ ] **Query Expansion**: Mở rộng câu hỏi tự động
- [ ] **Fact Verification**: Kiểm tra tính chính xác

#### Phase 3: Advanced AI
- [ ] **Fine-tuned Models**: Fine-tune LLM cho USSH
- [ ] **Custom Embeddings**: Train embedding model riêng
- [ ] **Active Learning**: Học từ feedback
- [ ] **RAG Fusion**: Kết hợp nhiều retrieval strategies
- [ ] **Self-correction**: Tự sửa lỗi

#### Phase 4: Integration & Deployment
- [ ] **Website Integration**: Embed vào website USSH
- [ ] **Facebook Messenger Bot**: Chatbot trên Messenger
- [ ] **Zalo Bot**: Tích hợp Zalo
- [ ] **Mobile App**: Ứng dụng di động
- [ ] **API Gateway**: RESTful API cho integrations

#### Phase 5: Enterprise Features
- [ ] **Admin Panel**: Quản lý documents, users, settings
- [ ] **Analytics**: Dashboard thống kê
- [ ] **A/B Testing**: Test các cấu hình khác nhau
- [ ] **Multi-tenancy**: Hỗ trợ nhiều trường
- [ ] **SSO Integration**: Đăng nhập SSO

#### Phase 6: Advanced Deployment
- [ ] **Docker Containerization**: Deploy dễ dàng
- [ ] **Kubernetes**: Auto-scaling
- [ ] **CI/CD Pipeline**: Tự động deploy
- [ ] **Monitoring**: Prometheus + Grafana
- [ ] **Cloud Deployment**: AWS/GCP/Azure

---

## 📚 Tài Liệu Tham Khảo

### Frameworks & Libraries
- [LangChain Documentation](https://python.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)

### LLM Providers
- [Google Gemini API](https://ai.google.dev/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

### RAG Resources
- [RAG Best Practices](https://www.llamaindex.ai/blog/a-cheat-sheet-and-some-recipes-for-building-advanced-rag-803a9d94c41b)
- [Advanced RAG Techniques](https://arxiv.org/abs/2312.10997)

### Vietnamese NLP
- [Vietnamese SBERT Models](https://huggingface.co/keepitreal/vietnamese-sbert)
- [VietAI Resources](https://github.com/VietAI)

---

## 🤝 Đóng Góp

Chúng tôi hoan nghênh mọi đóng góp! Để đóng góp:

1. Fork repository
2. Tạo branch mới: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add some feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Tạo Pull Request

### Guidelines

- Code phải có docstrings
- Follow PEP 8 style guide
- Thêm tests cho features mới
- Update documentation

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Team

**Phát triển bởi**: Team Chatbot USSH

**Liên hệ**:
- 📧 Email: support@ussh.edu.vn
- 🌐 Website: [https://ussh.edu.vn](https://ussh.edu.vn)
- 💬 Issues: [GitHub Issues](https://github.com/your-repo/issues)

---

## 🙏 Acknowledgments

- Trường Đại học Khoa học Xã hội và Nhân văn - ĐHQG-HCM
- LangChain community
- Streamlit team
- Open source contributors

---

## ⚠️ Disclaimer

Chatbot này được phát triển nhằm mục đích hỗ trợ sinh viên. Thông tin cung cấp chỉ mang tính tham khảo. Đối với các thông tin quan trọng, sinh viên nên xác nhận trực tiếp với phòng ban liên quan.

---

<div align="center">

**🎓 Made with ❤️ for USSH Students**

⭐ Star repo nếu bạn thấy hữu ích!

</div>
