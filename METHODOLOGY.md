# PHƯƠNG PHÁP THỰC HIỆN
## USSH SmartCampus Chatbot - Hệ Thống Hỗ Trợ Học Vụ Ứng Dụng Kiến Trúc RAG

---

## 1. TỔNG QUAN PHƯƠNG PHÁP

### 1.1. Giới thiệu

Hệ thống chatbot USSH SmartCampus được xây dựng dựa trên kiến trúc **RAG (Retrieval-Augmented Generation)**, kết hợp hai thành phần chính:
- **Retrieval System**: Hệ thống truy xuất thông tin từ cơ sở tri thức
- **Generation System**: Mô hình ngôn ngữ lớn (LLM) để sinh câu trả lời

Phương pháp này cho phép chatbot trả lời các câu hỏi dựa trên nguồn tài liệu chính thức của trường, đảm bảo tính chính xác và đáng tin cậy.

### 1.2. Lý do chọn phương pháp RAG

**Ưu điểm so với fine-tuning truyền thống:**
- ✓ Không cần fine-tune model (tiết kiệm thời gian, chi phí)
- ✓ Dễ dàng cập nhật tri thức (chỉ cần cập nhật vectorstore)
- ✓ Minh bạch: có thể trích dẫn nguồn
- ✓ Giảm hallucination (bịa đặt thông tin)
- ✓ Không giới hạn bởi context window của LLM

**So với rule-based chatbot:**
- ✓ Linh hoạt hơn, hiểu ngôn ngữ tự nhiên
- ✓ Không cần định nghĩa trước tất cả patterns
- ✓ Có khả năng reasoning và tổng hợp thông tin

---

## 2. KIẾN TRÚC HỆ THỐNG

### 2.1. Kiến trúc tổng quát

```
┌─────────────────────────────────────────────────────────────────┐
│                      OFFLINE PHASE (Setup)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │   Document   │  →   │   Document   │  →   │    Text      │ │
│  │  Collection  │      │  Processing  │      │  Chunking    │ │
│  │ (PDF,DOCX,TXT│      │   (OCR)      │      │ (Splitter)   │ │
│  └──────────────┘      └──────────────┘      └──────┬───────┘ │
│                                                       │          │
│                                                       ▼          │
│                                            ┌──────────────────┐ │
│                                            │    Embedding     │ │
│                                            │   (Vietnamese    │ │
│                                            │     SBERT)       │ │
│                                            └──────┬───────────┘ │
│                                                   │              │
│                                                   ▼              │
│                                            ┌──────────────────┐ │
│                                            │  Vector Database │ │
│                                            │   (ChromaDB)     │ │
│                                            └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    ONLINE PHASE (Runtime)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐                                               │
│  │ User Query   │                                               │
│  │ (Câu hỏi SV) │                                               │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │   Query      │  →   │  Similarity  │  →   │  Retrieve    │ │
│  │  Embedding   │      │   Search     │      │   Top-K      │ │
│  └──────────────┘      │ (Cosine Sim) │      │  Documents   │ │
│                        └──────────────┘      └──────┬───────┘ │
│                                                      │          │
│                                                      ▼          │
│                                            ┌──────────────────┐ │
│                                            │    Context       │ │
│                                            │   Assembly       │ │
│                                            └──────┬───────────┘ │
│                                                   │              │
│                                                   ▼              │
│                                            ┌──────────────────┐ │
│                                            │  Prompt          │ │
│                                            │  Template        │ │
│                                            └──────┬───────────┘ │
│                                                   │              │
│                                                   ▼              │
│                                            ┌──────────────────┐ │
│                                            │      LLM         │ │
│                                            │   (Gemini 2.0)   │ │
│                                            └──────┬───────────┘ │
│                                                   │              │
│                                                   ▼              │
│                                            ┌──────────────────┐ │
│                                            │   Response       │ │
│                                            │  + Citations     │ │
│                                            └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Các module chính

#### **Module 1: Document Processing** (`src/document_processor.py`)
- Chức năng: Xử lý và chuẩn bị dữ liệu
- Input: Tài liệu thô (PDF, DOCX, TXT, MD)
- Output: Các text chunks đã được xử lý

#### **Module 2: Embedding Management** (`src/embeddings.py`)
- Chức năng: Quản lý embedding models và vector database
- Input: Text chunks
- Output: Vector representations

#### **Module 3: Retrieval System** (`src/retriever.py`)
- Chức năng: Truy xuất thông tin liên quan
- Input: User query
- Output: Top-K relevant documents

#### **Module 4: Chatbot Core** (`src/chatbot.py`)
- Chức năng: Điều phối toàn bộ pipeline RAG
- Input: User question
- Output: Generated answer với citations

#### **Module 5: User Interface**
- Web UI: `app.py` (Streamlit)
- CLI: `chatbot.py` (Command-line)

---

## 3. QUY TRÌNH THỰC HIỆN CHI TIẾT

### 3.1. GIAI ĐOẠN 1: Thu thập và Chuẩn bị Dữ liệu

#### 3.1.1. Thu thập tài liệu

**Nguồn dữ liệu:**
- Quy chế đào tạo
- Quy định về thi cử và đánh giá
- Hướng dẫn đăng ký học phần
- Thông tin về học phí, học bổng
- Quy định về công tác sinh viên
- Tài liệu từ các phòng ban (CTSV, ĐT, KHTC)

**Định dạng hỗ trợ:**
- PDF (text-based và scan)
- Microsoft Word (DOCX)
- Plain text (TXT)
- Markdown (MD)

#### 3.1.2. Xử lý OCR (nếu cần)

**Công cụ:** Tesseract OCR + pdf2image

**Quy trình:**
```python
1. Phát hiện PDF scan:
   - Extract text từ page đầu tiên
   - Nếu text < 50 ký tự → coi là scan

2. Chuyển đổi PDF sang images:
   - DPI: 300 (đảm bảo chất lượng)
   - Format: PNG

3. OCR từng trang:
   - Language: vie+eng (tiếng Việt + tiếng Anh)
   - Config: --psm 3 (automatic page segmentation)

4. Lưu kết quả:
   - Format: TXT
   - Encoding: UTF-8
```

**Code implementation:**
```python
def ocr_pdf(pdf_path, output_path, lang='vie+eng'):
    images = convert_from_path(pdf_path, dpi=300)
    all_text = []
    
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang=lang)
        all_text.append(f"--- Trang {i+1} ---\n{text}\n\n")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(all_text)
```

#### 3.1.3. Document Loading

**Sử dụng LangChain Document Loaders:**

| Định dạng | Loader | Đặc điểm |
|-----------|--------|----------|
| PDF | `PyPDFLoader` | Preserve page numbers, metadata |
| DOCX | `Docx2txtLoader` | Extract text và formatting |
| TXT | `TextLoader` | Simple, UTF-8 encoding |
| MD | `UnstructuredMarkdownLoader` | Parse markdown structure |

**Metadata được preserve:**
- `source`: Tên file gốc
- `page`: Số trang (nếu có)
- `file_type`: Loại file (pdf, docx, txt, md)
- `file_path`: Đường dẫn đầy đủ

---

### 3.2. GIAI ĐOẠN 2: Text Chunking

#### 3.2.1. Chiến lược Chunking

**Phương pháp:** RecursiveCharacterTextSplitter

**Lý do chọn:**
- Thông minh: chia theo hierarchy (paragraph → sentence → word)
- Preserve context: giữ nguyên ngữ cảnh quan trọng
- Flexible: tùy chỉnh separators

**Tham số:**
```yaml
chunk_size: 1000        # Số ký tự mỗi chunk
chunk_overlap: 200      # Overlap giữa các chunks
separators:
  - "\n\n"              # Paragraph (ưu tiên cao nhất)
  - "\n"                # Line break
  - " "                 # Space
  - ""                  # Character-level (cuối cùng)
```

**Giải thích tham số:**

**1. Chunk Size = 1000 ký tự**
- Lý do: 
  - Đủ lớn để chứa thông tin đầy đủ (thường 1-2 đoạn văn)
  - Đủ nhỏ để embedding chính xác
  - Tương đương ~250 tokens (1 token ≈ 4 ký tự tiếng Việt)
- Trade-off:
  - Quá lớn: Loss semantic meaning, slow retrieval
  - Quá nhỏ: Thiếu context, nhiều chunks hơn

**2. Chunk Overlap = 200 ký tự**
- Lý do:
  - Tránh cắt ngang thông tin quan trọng
  - Đảm bảo continuity giữa các chunks
  - 20% overlap là tỷ lệ tối ưu (theo best practices)
- Ví dụ:
  ```
  Chunk 1: [0-1000] ký tự
  Chunk 2: [800-1800] ký tự (overlap 200 ký tự với chunk 1)
  ```

**3. Separators Hierarchy**
```python
separators = ["\n\n", "\n", " ", ""]
```
- Mức 1: `\n\n` - Chia theo đoạn văn (preferred)
- Mức 2: `\n` - Chia theo dòng nếu không tìm thấy paragraph
- Mức 3: ` ` - Chia theo từ nếu không tìm thấy line break
- Mức 4: `""` - Chia theo ký tự (worst case)

#### 3.2.2. Implementation

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""],
    length_function=len,
)

chunks = text_splitter.split_documents(documents)
```

**Kết quả ví dụ:**
```
Input: 50 documents (300 pages)
Output: ~800 chunks
Average chunk size: 850 ký tự
```

---

### 3.3. GIAI ĐOẠN 3: Embedding và Vector Database

#### 3.3.1. Embedding Model

**Model được chọn:** `keepitreal/vietnamese-sbert`

**Đặc điểm:**
- Kiến trúc: Sentence-BERT (Bi-encoder)
- Base model: PhoBERT (Vietnamese BERT)
- Output dimension: 768
- Training data: Vietnamese sentence pairs
- Performance: Cosine similarity correlation > 0.85

**Lý do chọn:**
1. **Tối ưu cho tiếng Việt**: Train trên corpus tiếng Việt
2. **Semantic understanding**: Hiểu nghĩa câu, không chỉ từ khóa
3. **Free & Local**: Chạy local, không phí API
4. **Fast inference**: ~50ms/embedding trên CPU

**So sánh với các alternatives:**

| Model | Pros | Cons | Use case |
|-------|------|------|----------|
| `vietnamese-sbert` | Tốt nhất cho tiếng Việt | Cần download model (~500MB) | **Được chọn** |
| `multilingual-e5-base` | Multilingual, SOTA | Kém hơn cho tiếng Việt | Backup option |
| `text-embedding-ada-002` | Chất lượng cao | Trả phí, phụ thuộc API | Production với budget |

#### 3.3.2. Embedding Process

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="keepitreal/vietnamese-sbert",
    model_kwargs={'device': 'cpu'},        # Hoặc 'cuda' nếu có GPU
    encode_kwargs={'normalize_embeddings': True}  # L2 normalization
)

# Generate embeddings
vector = embeddings.embed_query("Điều kiện tốt nghiệp là gì?")
# Output: array of 768 float numbers
```

**Normalization:**
- Tất cả vectors được normalize về unit length
- Lý do: Cosine similarity = dot product khi normalized
- Tăng tốc độ tính toán

#### 3.3.3. Vector Database - ChromaDB

**Kiến trúc ChromaDB:**
```
ChromaDB
├── Collections (student_support_docs)
│   ├── Documents (text chunks)
│   ├── Embeddings (768-dim vectors)
│   ├── Metadata (source, page, etc.)
│   └── IDs (unique identifiers)
├── Indices (HNSW - Hierarchical Navigable Small World)
└── Storage (SQLite + Binary files)
```

**Tính năng chính:**
- **Persistent storage**: Dữ liệu được lưu trên disk
- **Fast search**: HNSW algorithm (logarithmic complexity)
- **Metadata filtering**: Lọc theo source, page, etc.
- **Batch operations**: Thêm nhiều documents cùng lúc

**Implementation:**
```python
from langchain.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./data/vectorstore",
    collection_name="student_support_docs"
)

vectorstore.persist()  # Save to disk
```

**Storage structure:**
```
data/vectorstore/
├── chroma.sqlite3              # Metadata database
└── 38015ad0-6fcf.../          # Collection directory
    ├── data_level0.bin        # HNSW index level 0
    ├── header.bin             # Index metadata
    ├── length.bin             # Vector lengths
    └── link_lists.bin         # HNSW graph structure
```

**Thống kê ví dụ:**
- Number of vectors: 800
- Vector dimension: 768
- Storage size: ~150 MB
- Index build time: ~2 minutes
- Query time: ~50ms

---

### 3.4. GIAI ĐOẠN 4: Retrieval System

#### 3.4.1. Similarity Search Algorithm

**Thuật toán:** HNSW (Hierarchical Navigable Small World)

**Nguyên lý:**
```
1. Build phase (offline):
   - Tạo multi-layer graph
   - Mỗi node là một vector
   - Edges kết nối các vectors gần nhau

2. Search phase (online):
   - Start từ layer cao nhất
   - Greedy search đến local minimum
   - Move down layers
   - Refine search ở layer 0
```

**Complexity:**
- Build: O(N log N)
- Search: O(log N)
- Memory: O(N)

**Distance metric:** Cosine Similarity

```
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)

Với normalized vectors: cosine_similarity(A, B) = A · B
```

**Range:** [-1, 1]
- 1: Hoàn toàn giống nhau
- 0: Không liên quan
- -1: Hoàn toàn đối lập (hiếm khi xảy ra)

#### 3.4.2. Retrieval Process

```python
def retrieve(query: str, top_k: int = 5):
    """
    Bước 1: Embed query
    """
    query_vector = embeddings.embed_query(query)
    
    """
    Bước 2: Similarity search
    """
    results = vectorstore.similarity_search_with_score(
        query,
        k=top_k
    )
    # Returns: [(doc1, score1), (doc2, score2), ...]
    
    """
    Bước 3: Score filtering
    """
    threshold = 0.5
    filtered = [(doc, score) for doc, score in results 
                if score >= threshold]
    
    """
    Bước 4: Return documents
    """
    return [doc for doc, _ in filtered]
```

**Tham số:**
- `top_k = 5`: Lấy 5 chunks liên quan nhất
  - Lý do: Balance giữa context và noise
  - Trade-off: Nhiều hơn → nhiều context nhưng chậm và nhiễu
  
- `score_threshold = 0.5`: Lọc kết quả có similarity < 0.5
  - Lý do: Đảm bảo chất lượng kết quả
  - Trong thực tế: Scores thường 0.6-0.9 cho queries liên quan

#### 3.4.3. Context Assembly

**Mục đích:** Kết hợp các chunks thành context cho LLM

```python
def get_context_string(documents):
    context_parts = []
    
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get('source', 'Unknown')
        page = doc.metadata.get('page', '')
        
        context_parts.append(
            f"[Tài liệu {i}] Nguồn: {source} (Trang {page})\n"
            f"{doc.page_content}\n"
        )
    
    return "\n---\n".join(context_parts)
```

**Kết quả ví dụ:**
```
[Tài liệu 1] Nguồn: quy_che_dao_tao.pdf (Trang 15)
Điều 25. Điều kiện xét tốt nghiệp
Sinh viên được xét tốt nghiệp khi đáp ứng đủ các điều kiện sau:
1. Tích lũy đủ số tín chỉ theo chương trình...
2. Điểm trung bình tích lũy đạt từ 2.0 trở lên...

---

[Tài liệu 2] Nguồn: huong_dan_tot_nghiep.pdf (Trang 3)
Quy trình nộp hồ sơ xét tốt nghiệp:
- Bước 1: Kiểm tra điều kiện...
- Bước 2: Nộp đơn đăng ký...
```

---

### 3.5. GIAI ĐOẠN 5: LLM Generation

#### 3.5.1. LLM Selection

**Model được chọn:** Google Gemini 2.0 Flash

**Thông số kỹ thuật:**
- Model family: Gemini 2.0
- Variant: Flash (optimized for speed)
- Context window: 1M tokens
- Output max: 8K tokens
- Languages: 100+ including Vietnamese
- Pricing: Free tier available

**So sánh với alternatives:**

| Model | Speed | Quality | Cost | Vietnamese | Chọn |
|-------|-------|---------|------|------------|------|
| Gemini 2.0 Flash | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Free | ⭐⭐⭐⭐⭐ | ✅ |
| GPT-4 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $$$$ | ⭐⭐⭐⭐ | ❌ |
| GPT-3.5 Turbo | ⭐⭐⭐⭐ | ⭐⭐⭐ | $$ | ⭐⭐⭐⭐ | ❌ |
| Claude 3 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $$$ | ⭐⭐⭐⭐ | ❌ |

**Lý do chọn Gemini 2.0 Flash:**
1. **Free tier**: Phù hợp cho prototype và academic project
2. **Excellent Vietnamese**: Được train tốt trên tiếng Việt
3. **Fast**: Optimized for low latency
4. **Large context**: 1M tokens (không giới hạn bởi context)
5. **Multi-modal**: Sẵn sàng cho future features (image, audio)

#### 3.5.2. Prompt Engineering

**Prompt Template:**

```python
template = """
{system_prompt}

CONTEXT (Thông tin từ tài liệu của trường):
{context}

QUESTION (Câu hỏi của sinh viên):
{question}

ANSWER (Câu trả lời của bạn):
"""
```

**System Prompt:**
```
Bạn là trợ lý ảo hỗ trợ sinh viên của Trường Đại học Khoa học Xã hội 
và Nhân văn - ĐHQG-HCM (USSH).

NHIỆM VỤ:
- Trả lời các câu hỏi của sinh viên dựa trên thông tin từ các văn bản, 
  quy định của trường được cung cấp trong CONTEXT
- Luôn trích dẫn nguồn thông tin khi trả lời
- Nếu không có thông tin trong CONTEXT, hãy nói rõ và hướng dẫn 
  sinh viên liên hệ phòng ban liên quan

PHONG CÁCH TRẢ LỜI:
- Chính xác: Chỉ dựa trên thông tin được cung cấp
- Rõ ràng: Câu trả lời dễ hiểu, có cấu trúc
- Thân thiện: Giọng điệu lịch sự, gần gũi
- Ngắn gọn: Đi thẳng vào vấn đề, tránh lan man

QUY TẮC QUAN TRỌNG:
1. KHÔNG bịa đặt thông tin không có trong CONTEXT
2. KHÔNG đưa ra ý kiến cá nhân
3. KHÔNG trả lời các câu hỏi không liên quan đến học vụ
4. Luôn kiểm tra lại thông tin trước khi trả lời
```

**Kỹ thuật Prompt Engineering được áp dụng:**

1. **Role Definition**: Định nghĩa rõ vai trò
2. **Task Description**: Mô tả nhiệm vụ cụ thể
3. **Style Guidelines**: Hướng dẫn phong cách
4. **Constraints**: Đặt ra các ràng buộc
5. **Few-shot Examples** (optional): Có thể thêm examples

#### 3.5.3. Generation Process

```python
def generate_answer(question: str, context: str):
    """
    Bước 1: Format prompt
    """
    prompt = template.format(
        system_prompt=system_prompt,
        context=context,
        question=question
    )
    
    """
    Bước 2: Call LLM API
    """
    response = model.generate_content(
        prompt,
        generation_config={
            'temperature': 0.7,      # Creativity level
            'top_p': 0.9,           # Nucleus sampling
            'max_output_tokens': 1500,
            'candidate_count': 1
        }
    )
    
    """
    Bước 3: Extract and clean response
    """
    answer = response.text
    
    # Remove HTML tags if any
    answer = answer.replace('</div>', '').strip()
    
    # Remove file references (e.g., "(document.txt)")
    if answer.endswith(')'):
        last_paren = answer.rfind('(')
        if last_paren > 0 and '.txt' in answer[last_paren:]:
            answer = answer[:last_paren].strip()
    
    return answer
```

**Generation Config Parameters:**

| Parameter | Value | Ý nghĩa | Tác động |
|-----------|-------|---------|----------|
| `temperature` | 0.7 | Độ "sáng tạo" | 0=deterministic, 1=random |
| `top_p` | 0.9 | Nucleus sampling | Chọn từ top 90% probable tokens |
| `max_tokens` | 1500 | Max độ dài output | ~375 từ tiếng Việt |
| `candidate_count` | 1 | Số responses | Chỉ lấy 1 câu trả lời tốt nhất |

**Temperature tuning:**
- `0.0-0.3`: Rất deterministic, phù hợp factual QA
- `0.4-0.7`: **Balanced** (được chọn)
- `0.8-1.0`: Creative, có thể hallucinate

---

### 3.6. GIAI ĐOẠN 6: Response Post-processing

#### 3.6.1. Answer Validation

```python
def validate_answer(answer: str) -> bool:
    """
    Kiểm tra xem câu trả lời có phải là "không biết" không
    """
    no_answer_keywords = [
        'xin lỗi', 'không tìm thấy', 'không có thông tin',
        'không rõ', 'không biết', 'chưa có thông tin',
        'không tìm được', 'không có dữ liệu', 'không đề cập'
    ]
    
    is_no_answer = any(
        keyword in answer.lower() 
        for keyword in no_answer_keywords
    )
    
    return not is_no_answer
```

#### 3.6.2. Source Citation

```python
def get_source_references(documents):
    """
    Extract unique sources từ retrieved documents
    """
    sources = []
    seen = set()
    
    for doc in documents:
        source_id = (
            doc.metadata.get('source', 'Unknown'),
            doc.metadata.get('page', '')
        )
        
        if source_id not in seen:
            sources.append({
                'source': doc.metadata.get('source'),
                'page': doc.metadata.get('page'),
                'file_type': doc.metadata.get('file_type')
            })
            seen.add(source_id)
    
    return sources
```

#### 3.6.3. Final Response Format

```json
{
    "question": "Điều kiện tốt nghiệp USSH là gì?",
    "answer": "Theo quy định của trường, sinh viên được xét tốt nghiệp khi đáp ứng đủ các điều kiện sau:\n1. Hoàn thành đủ số tín chỉ theo chương trình đào tạo\n2. Điểm trung bình tích lũy đạt từ 2.0 trở lên\n3. Không vi phạm kỷ luật...",
    "sources": [
        {
            "source": "quy_che_dao_tao.pdf",
            "page": "15",
            "file_type": "pdf"
        },
        {
            "source": "huong_dan_tot_nghiep.pdf",
            "page": "3",
            "file_type": "pdf"
        }
    ],
    "num_sources": 5,
    "confidence": "high"
}
```

---

## 4. GIAO DIỆN NGƯỜI DÙNG

### 4.1. Web Interface (Streamlit)

**Kiến trúc:**
```python
app.py (Streamlit App)
├── Configuration (Page config, CSS)
├── Session State Management
├── Sidebar (Settings, Examples)
├── Main Chat Interface
│   ├── Chat History Display
│   ├── Message Input
│   └── Response Rendering
└── Footer
```

**Tính năng chính:**

1. **Chat History**: Lưu và hiển thị lịch sử chat
   ```python
   if "messages" not in st.session_state:
       st.session_state.messages = []
   ```

2. **Source Display**: Hiển thị nguồn tham khảo đẹp mắt
   ```python
   st.markdown(f"""
   <div class='source-box'>
       <strong>📚 Nguồn:</strong><br>
       {source['source']} (Trang {source['page']})
   </div>
   """, unsafe_allow_html=True)
   ```

3. **Dynamic Settings**: Điều chỉnh top_k, include_sources
   ```python
   top_k = st.slider("Độ sâu tìm kiếm", 1, 10, 5)
   include_sources = st.checkbox("Hiển thị nguồn", True)
   ```

4. **Example Questions**: Gợi ý câu hỏi thường gặp
   ```python
   example_questions = [
       "Điều kiện tốt nghiệp USSH?",
       "Quy định về điểm danh?",
       ...
   ]
   ```

**UI/UX Design Principles:**
- **USSH Branding**: Sử dụng màu xanh chủ đạo của trường
- **Responsive**: Tự động adapt với mobile/desktop
- **Accessibility**: Dễ sử dụng cho mọi đối tượng
- **Performance**: Cache chatbot instance, lazy loading

### 4.2. CLI Interface

**Đơn giản hơn, phù hợp cho:**
- Testing và debugging
- Server deployment (không cần GUI)
- Automation scripts

```python
while True:
    question = input("\n❓ Câu hỏi: ")
    if question.lower() in ['exit', 'quit']:
        break
    
    response = chatbot.ask(question)
    print(chatbot.format_response(response))
```

---

## 5. TỐI ỰU HÓA VÀ ĐÁNH GIÁ

### 5.1. Metrics Đánh Giá

#### 5.1.1. Retrieval Metrics

**1. Precision@K**
```
Precision@K = (Số documents liên quan trong top-K) / K
```

**2. Recall@K**
```
Recall@K = (Số documents liên quan được retrieve) / (Tổng số documents liên quan)
```

**3. Mean Reciprocal Rank (MRR)**
```
MRR = 1/N × Σ(1/rank_i)
```
Với rank_i là vị trí của document liên quan đầu tiên

#### 5.1.2. Generation Metrics

**1. BLEU Score** (nếu có ground truth)
- Đo độ giống với câu trả lời chuẩn

**2. Human Evaluation**
- Accuracy: Chính xác (1-5)
- Relevance: Liên quan (1-5)
- Completeness: Đầy đủ (1-5)
- Clarity: Rõ ràng (1-5)

**3. Source Attribution Rate**
```
Attribution Rate = (Số câu trả lời có source) / (Tổng số câu trả lời)
```

### 5.2. Optimization Techniques

#### 5.2.1. Retrieval Optimization

**1. Chunk Size Tuning**
```python
# Test different sizes
chunk_sizes = [500, 800, 1000, 1200, 1500]
for size in chunk_sizes:
    evaluate_retrieval(chunk_size=size)
```

**2. Top-K Tuning**
```python
# Find optimal K
ks = [3, 5, 7, 10]
for k in ks:
    evaluate_quality(top_k=k)
```

**3. Score Threshold Tuning**
```python
# Balance precision and recall
thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
for t in thresholds:
    evaluate_retrieval(threshold=t)
```

#### 5.2.2. Generation Optimization

**1. Temperature Tuning**
```python
temperatures = [0.3, 0.5, 0.7, 0.9]
for temp in temperatures:
    responses = generate_batch(temperature=temp)
    evaluate_quality(responses)
```

**2. Prompt Optimization**
- A/B testing different prompts
- Add few-shot examples
- Refine instructions

**3. Context Length Optimization**
```python
# Test với different max context length
max_lengths = [2000, 3000, 4000, 5000]
```

### 5.3. Caching và Performance

#### 5.3.1. Embedding Cache
```python
@lru_cache(maxsize=1000)
def cached_embed_query(query: str):
    return embeddings.embed_query(query)
```

#### 5.3.2. Streamlit Cache
```python
@st.cache_resource
def load_chatbot():
    return StudentSupportChatbot()
```

#### 5.3.3. Batch Processing
```python
# Process documents in batches
batch_size = 100
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    vectorstore.add_documents(batch)
```

---

## 6. LOGGING VÀ MONITORING

### 6.1. Logging System

**Cấu trúc logs:**
```
logs/chatbot.log
├── INFO: System initialization
├── INFO: User query received
├── DEBUG: Retrieved documents (scores)
├── INFO: LLM generation time
├── INFO: Response returned
└── ERROR: Error details (if any)
```

**Log format:**
```
2024-01-15 10:30:45 - chatbot - INFO - ❓ Question: Điều kiện tốt nghiệp?
2024-01-15 10:30:45 - retriever - DEBUG - Retrieved 5 docs (scores: 0.87, 0.82, ...)
2024-01-15 10:30:47 - chatbot - INFO - ✅ Answer generated (time: 2.1s)
```

### 6.2. Monitoring Metrics

**Tracking:**
- Number of queries per day
- Average response time
- Top queries
- Error rate
- Source attribution rate

**Dashboard (future):**
```python
metrics = {
    'total_queries': count_queries(),
    'avg_response_time': calculate_avg_time(),
    'top_queries': get_top_queries(n=10),
    'error_rate': calculate_error_rate(),
    'satisfaction_score': get_user_ratings()
}
```

---

## 7. KẾT LUẬN PHƯƠNG PHÁP

### 7.1. Ưu điểm của Phương pháp

1. **Chính xác cao**: Dựa trên tài liệu chính thức
2. **Minh bạch**: Trích dẫn nguồn rõ ràng
3. **Dễ cập nhật**: Chỉ cần thêm documents mới
4. **Linh hoạt**: Hỗ trợ nhiều LLM và embedding models
5. **Scalable**: Có thể mở rộng cho nhiều trường
6. **Cost-effective**: Sử dụng free tiers

### 7.2. Hạn chế và Hướng Giải quyết

| Hạn chế | Tác động | Giải pháp |
|---------|----------|-----------|
| Phụ thuộc chất lượng documents | Nếu docs kém → kết quả kém | Cải thiện OCR, preprocessing |
| Không xử lý multi-turn conversation | Thiếu context lịch sử | Implement conversation memory |
| Có thể miss information | Nếu chunking không tốt | Optimize chunk size, overlap |
| Latency (~2-3s) | User experience | Caching, async processing |

### 7.3. Hướng Phát triển

**Ngắn hạn (1-3 tháng):**
- Implement re-ranking
- Add conversation history
- Improve OCR quality

**Trung hạn (3-6 tháng):**
- Fine-tune embedding model
- Add analytics dashboard
- Multi-language support

**Dài hạn (6-12 tháng):**
- Voice interface
- Mobile app
- Integration với hệ thống trường

---

## PHỤ LỤC

### A. Cấu hình Đầy đủ

```yaml
# config/config.yaml
document_processing:
  supported_formats: [pdf, docx, txt, md]
  chunk_size: 1000
  chunk_overlap: 200
  separators: ["\n\n", "\n", " ", ""]

embedding:
  provider: "sentence-transformers"
  model_name: "keepitreal/vietnamese-sbert"
  batch_size: 32

vectorstore:
  type: "chromadb"
  persist_directory: "./data/vectorstore"
  collection_name: "student_support_docs"
  distance_metric: "cosine"

llm:
  provider: "gemini"
  model_name: "models/gemini-2.0-flash"
  temperature: 0.7
  max_tokens: 1500
  top_p: 0.9

retrieval:
  top_k: 5
  score_threshold: 0.5
  rerank: false

response:
  language: "vi"
  include_sources: true
  max_source_length: 200

logging:
  level: "INFO"
  file: "./logs/chatbot.log"
```

### B. Dependencies

```
langchain>=0.1.0
langchain-community>=0.1.0
langchain-openai>=0.0.5
chromadb>=0.4.0
sentence-transformers>=2.2.0
streamlit>=1.29.0
python-dotenv>=1.0.0
pyyaml>=6.0
pypdf2>=3.0.0
pdfplumber>=0.10.0
python-docx>=1.0.0
pytesseract>=0.3.10
pdf2image>=1.16.0
pillow>=10.0.0
tqdm>=4.65.0
google-generativeai>=0.3.0
```

### C. Tài liệu Tham khảo

1. Lewis, P., et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks". NeurIPS.
2. Reimers, N., & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks". EMNLP.
3. Malkov, Y., & Yashunin, D. (2018). "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs". IEEE.
4. Google DeepMind (2024). "Gemini 2.0: Technical Report".
5. LangChain Documentation: https://python.langchain.com/

---

**Tài liệu này mô tả chi tiết phương pháp thực hiện hệ thống USSH SmartCampus Chatbot.**

*Phiên bản: 1.0*  
*Ngày cập nhật: 2024*


