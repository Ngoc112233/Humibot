# 🚀 Hướng Dẫn Bắt Đầu Nhanh

## Yêu cầu hệ thống

- Python 3.8 trở lên
- 4GB RAM (tối thiểu)
- Kết nối internet (để download models và sử dụng API)

## Các Bước Cài Đặt

### 1. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình API Keys

Tạo file `.env` từ template:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` và thêm API key (chọn 1 trong 3 options):

**Option 1: Google Gemini (Khuyến nghị - Có free tier)**
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

Lấy API key tại: https://makersuite.google.com/app/apikey

**Option 2: OpenAI (Trả phí, chất lượng cao)**
```bash
OPENAI_API_KEY=sk-your_openai_api_key_here
```

**Option 3: Local LLM (Miễn phí, cần GPU)**
- Cài đặt Ollama: https://ollama.ai/
- Pull model: `ollama pull llama2`
- Không cần API key

### 3. Chuẩn bị Documents

Tạo thư mục và thêm tài liệu:

```bash
mkdir -p data/documents
```

Thêm các file PDF, DOCX, hoặc TXT của trường vào thư mục `data/documents/`

**Ví dụ:**
- `data/documents/quy_che_dao_tao.pdf`
- `data/documents/quy_dinh_thi.pdf`
- `data/documents/huong_dan_dang_ky_hoc.docx`

### 4. Xử lý Documents và Tạo Vector Database

```bash
python scripts/process_documents.py
```

Script này sẽ:
- Đọc tất cả documents từ `data/documents/`
- Chia thành các chunks nhỏ
- Tạo embeddings
- Lưu vào vector database

⏱️ Thời gian xử lý: ~1-5 phút (tùy số lượng documents)

### 5. Chạy Chatbot

**Option A: CLI Interface**

```bash
python chatbot.py
```

**Option B: Web Interface (Streamlit)**

```bash
streamlit run app.py
```

Truy cập: http://localhost:8501

## Test Nhanh

Sau khi chạy chatbot, thử các câu hỏi sau:

- "Điều kiện để được xét tốt nghiệp là gì?"
- "Quy định về điểm danh và nghỉ học?"
- "Làm thế nào để đăng ký môn học?"

## Troubleshooting

### Lỗi: "OPENAI_API_KEY không được cấu hình"

**Giải pháp:** 
- Kiểm tra file `.env` đã tạo chưa
- Đảm bảo API key đúng format
- Hoặc đổi sang provider khác trong `config/config.yaml`

### Lỗi: "Vectorstore chưa được tạo"

**Giải pháp:**
```bash
python scripts/process_documents.py
```

### Lỗi: Module not found

**Giải pháp:**
```bash
pip install -r requirements.txt --upgrade
```

### Documents không được load

**Kiểm tra:**
- File có đúng định dạng (PDF, DOCX, TXT, MD) không?
- File có bị corrupt không?
- Thử với 1 file đơn giản trước (TXT)

## Cấu Hình Nâng Cao

### Thay đổi Embedding Model

Chỉnh sửa `config/config.yaml`:

```yaml
embedding:
  provider: "sentence-transformers"
  model_name: "keepitreal/vietnamese-sbert"  # Model tiếng Việt
```

**Models khác:**
- `intfloat/multilingual-e5-base` (multilingual, tốt)
- `all-MiniLM-L6-v2` (English, nhanh)

### Thay đổi LLM

```yaml
llm:
  provider: "gemini"  # hoặc "openai", "ollama"
  model_name: "gemini-pro"
  temperature: 0.7
```

### Tối ưu cho tiếng Việt

1. Sử dụng embedding model tiếng Việt:
   - `keepitreal/vietnamese-sbert`
   - `uitnlp/visobert`

2. Sử dụng LLM hỗ trợ tiếng Việt tốt:
   - Google Gemini (rất tốt cho tiếng Việt)
   - GPT-4 (tốt nhưng đắt)
   - Viettel AI models (nếu có API)

## Update Documents

Khi có tài liệu mới:

```bash
# Thêm file vào data/documents/
# Sau đó chạy:
python scripts/update_vectorstore.py
```

## Performance Tips

### Tăng tốc độ xử lý:
- Giảm `chunk_size` trong config (nhanh hơn nhưng ít chính xác hơn)
- Sử dụng FAISS thay vì ChromaDB
- Giảm `top_k` trong retrieval

### Cải thiện chất lượng:
- Tăng `top_k` (retrieve nhiều context hơn)
- Sử dụng model embedding tốt hơn
- Fine-tune prompt trong `config/config.yaml`

## Next Steps

✅ Chatbot đã chạy thành công!

**Các bước tiếp theo:**

1. **Thêm nhiều documents** vào `data/documents/`
2. **Tùy chỉnh prompt** trong `config/config.yaml` để phù hợp với trường
3. **Deploy lên server** (xem DEPLOYMENT.md)
4. **Tích hợp vào website** hoặc Facebook Messenger

## Hỗ Trợ

- 📖 Đọc README.md đầy đủ
- 🐛 Báo lỗi: Tạo issue trên GitHub
- 💬 Hỏi đáp: Discussions tab

---

**Chúc bạn thành công! 🎉**





