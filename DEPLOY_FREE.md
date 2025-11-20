# 🆓 DEPLOY HUMIBOT MIỄN PHÍ 100%

**3 Phương Án Deploy Hoàn Toàn Miễn Phí cho humibot.id.vn**

---

## 📋 Tổng Quan Các Phương Án

| Phương Án | Độ Khó | Thời Gian | Custom Domain | Giới Hạn | Khuyến Nghị |
|-----------|--------|-----------|---------------|----------|-------------|
| **Streamlit Cloud** | ⭐ Dễ nhất | 10 phút | ✅ Có | RAM 1GB | ⭐⭐⭐⭐⭐ |
| **Google Cloud Run** | ⭐⭐ Trung bình | 20 phút | ✅ Có | Free tier | ⭐⭐⭐⭐ |
| **Render** | ⭐⭐ Trung bình | 15 phút | ✅ Có | RAM 512MB | ⭐⭐⭐ |

---

## 🌟 PHƯƠNG ÁN 1: STREAMLIT COMMUNITY CLOUD (KHUYẾN NGHỊ)

**Ưu điểm:**
- ✅ Hoàn toàn MIỄN PHÍ
- ✅ Dễ nhất, chỉ cần 3 clicks
- ✅ Tự động deploy từ GitHub
- ✅ Hỗ trợ custom domain MIỄN PHÍ
- ✅ SSL tự động
- ✅ Không cần config gì thêm

**Nhược điểm:**
- ⚠️ RAM giới hạn 1GB (đủ cho chatbot này)
- ⚠️ App sleep sau 7 ngày không dùng (có thể ping để keep alive)

### BƯỚC 1: Chuẩn Bị GitHub Repository

#### 1.1. Push Code Lên GitHub

```bash
# Từ máy Mac
cd "/Volumes/ổ cứng C/DA-test"

# Init git (nếu chưa có)
git init

# Tạo .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv
.DS_Store
logs/*.log
*.log
data/vectorstore/

# QUAN TRỌNG: Không commit .env
.env
EOF

# Add và commit
git add .
git commit -m "Initial commit for HumiBot"

# Tạo repo trên GitHub:
# 1. Truy cập https://github.com/new
# 2. Repository name: humibot
# 3. Public (bắt buộc cho free tier)
# 4. Create repository

# Link và push
git remote add origin https://github.com/YOUR_USERNAME/humibot.git
git branch -M main
git push -u origin main
```

#### 1.2. Tạo File secrets.toml Template

Streamlit Cloud cần file này để quản lý secrets:

```bash
mkdir -p .streamlit
cat > .streamlit/secrets.toml << 'EOF'
# Secrets for Streamlit Cloud
# NOTE: File này chỉ là template, không commit vào git
# Secrets thật sẽ config trên Streamlit Cloud dashboard

# Google API Key
GOOGLE_API_KEY = "your_key_here"
EOF

# Đừng commit file này
echo ".streamlit/secrets.toml" >> .gitignore
git add .gitignore
git commit -m "Add secrets template"
git push
```

#### 1.3. Tạo packages.txt (Cho System Dependencies)

```bash
cat > packages.txt << 'EOF'
tesseract-ocr
tesseract-ocr-vie
poppler-utils
EOF

git add packages.txt
git commit -m "Add system packages"
git push
```

### BƯỚC 2: Deploy Lên Streamlit Cloud

#### 2.1. Đăng Ký Streamlit Cloud

1. Truy cập: **https://share.streamlit.io/**
2. Click **"Sign up with GitHub"**
3. Authorize Streamlit Cloud

#### 2.2. Deploy App

1. Click **"New app"**
2. Chọn:
   - **Repository:** `YOUR_USERNAME/humibot`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Click **"Advanced settings"**
4. Thêm **Secrets** (quan trọng!):

```toml
GOOGLE_API_KEY = "AIzaSy...your_actual_key_here"
```

5. Click **"Deploy!"**

⏱️ Đợi 5-10 phút để build và deploy.

**URL mặc định:** `https://your-username-humibot-xxxxx.streamlit.app`

### BƯỚC 3: Cấu Hình Custom Domain (humibot.id.vn)

#### 3.1. Trên Streamlit Cloud

1. Mở app dashboard
2. Click **"⚙️ Settings"** → **"General"**
3. Kéo xuống **"Custom subdomain"**
4. Nhập: `humibot` (sẽ thành humibot.streamlit.app)
5. Save

#### 3.2. Cấu Hình DNS

**Option A: CNAME Record (Khuyến nghị)**

Vào trang quản lý domain, thêm:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | @ | humibot.streamlit.app | 3600 |
| CNAME | www | humibot.streamlit.app | 3600 |

**Lưu ý:** Một số nhà đăng ký không cho phép CNAME cho root domain (@). Nếu vậy, dùng Option B.

**Option B: URL Redirect**

1. Tại DNS settings, tạo:
   - CNAME: `www` → `humibot.streamlit.app`
2. Tại Domain settings, tạo:
   - URL Redirect: `humibot.id.vn` → `https://www.humibot.id.vn`

**Option C: Cloudflare (Tốt nhất)**

1. Add domain vào Cloudflare (free): https://dash.cloudflare.com/
2. Thay đổi nameservers (theo hướng dẫn của Cloudflare)
3. Trong Cloudflare DNS:
   - CNAME: `@` → `humibot.streamlit.app` (Proxy: ON)
   - CNAME: `www` → `humibot.streamlit.app` (Proxy: ON)

#### 3.3. Xác Minh Domain (Nếu Cần)

Một số trường hợp Streamlit yêu cầu verify domain:

1. Dashboard → Settings → Custom domain
2. Add domain: `humibot.id.vn`
3. Thêm TXT record theo hướng dẫn
4. Verify

### BƯỚC 4: Keep App Alive (Tránh Sleep)

Streamlit app sleep sau 7 ngày không dùng. Giải pháp:

**Option A: UptimeRobot (Free)**

1. Đăng ký: https://uptimerobot.com/
2. Add Monitor:
   - Type: HTTPS
   - URL: `https://humibot.id.vn`
   - Interval: 5 minutes
3. UptimeRobot sẽ ping định kỳ → app không sleep

**Option B: Cron Job (Nếu có server khác)**

```bash
# Thêm vào crontab
*/5 * * * * curl -s https://humibot.id.vn > /dev/null
```

**Option C: GitHub Actions (Free)**

Tạo file `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Streamlit App Alive

on:
  schedule:
    - cron: '*/30 * * * *'  # Mỗi 30 phút
  workflow_dispatch:

jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - name: Ping app
        run: |
          curl -s https://humibot.id.vn > /dev/null
          echo "App pinged successfully"
```

Commit và push:
```bash
git add .github/workflows/keep-alive.yml
git commit -m "Add keep-alive workflow"
git push
```

### ✅ Hoàn Thành!

Truy cập: **https://humibot.id.vn**

---

## 🌐 PHƯƠNG ÁN 2: GOOGLE CLOUD RUN (Free Tier)

**Ưu điểm:**
- ✅ Free tier hào phóng (2 triệu requests/tháng)
- ✅ Tự động scale
- ✅ Performance tốt
- ✅ Hỗ trợ custom domain

**Nhược điểm:**
- ⚠️ Phức tạp hơn Streamlit Cloud
- ⚠️ Cần credit card (không charge nếu trong free tier)

### BƯỚC 1: Setup Google Cloud

1. Truy cập: https://console.cloud.google.com/
2. Tạo project mới: `humibot`
3. Enable APIs:
   - Cloud Run API
   - Cloud Build API
   - Artifact Registry API

### BƯỚC 2: Cài Google Cloud CLI

**macOS:**
```bash
brew install --cask google-cloud-sdk
gcloud init
gcloud auth login
```

### BƯỚC 3: Deploy

```bash
cd "/Volumes/ổ cứng C/DA-test"

# Tạo file .gcloudignore
cat > .gcloudignore << 'EOF'
.git/
.gitignore
__pycache__/
*.pyc
.env
venv/
logs/
EOF

# Deploy với Cloud Run
gcloud run deploy humibot \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY="your_api_key_here"

# Sẽ nhận được URL: https://humibot-xxxxx-uc.a.run.app
```

### BƯỚC 4: Map Custom Domain

```bash
# Map domain
gcloud run domain-mappings create \
  --service humibot \
  --domain humibot.id.vn \
  --region asia-southeast1

# Làm theo hướng dẫn add DNS records
```

### BƯỚC 5: Tối Ưu Chi Phí

Để đảm bảo luôn free:

```bash
gcloud run services update humibot \
  --region asia-southeast1 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 3 \
  --concurrency 80
```

---

## 🎨 PHƯƠNG ÁN 3: RENDER (Free Tier)

**Ưu điểm:**
- ✅ Đơn giản như Heroku
- ✅ Free tier tốt
- ✅ Tự động deploy từ GitHub
- ✅ SSL miễn phí

**Nhược điểm:**
- ⚠️ App sleep sau 15 phút không dùng
- ⚠️ RAM chỉ 512MB (có thể không đủ)

### BƯỚC 1: Push Code Lên GitHub

(Giống Streamlit Cloud)

### BƯỚC 2: Deploy Trên Render

1. Truy cập: https://render.com/
2. Sign up với GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect repository: `humibot`
5. Cấu hình:
   - **Name:** `humibot`
   - **Environment:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
     ```
   - **Plan:** `Free`

6. Environment Variables:
   - `GOOGLE_API_KEY` = `your_key_here`

7. Click **"Create Web Service"**

### BƯỚC 3: Custom Domain

1. Dashboard → Settings → Custom Domains
2. Add domain: `humibot.id.vn`
3. Thêm DNS records theo hướng dẫn:
   - CNAME: `@` → `humibot.onrender.com`

### BƯỚC 4: Keep Alive

Dùng UptimeRobot (giống Streamlit Cloud)

---

## 📊 SO SÁNH CHI TIẾT

### Free Tier Limits

| Feature | Streamlit Cloud | Google Cloud Run | Render |
|---------|----------------|------------------|--------|
| **RAM** | 1GB | 2GB | 512MB |
| **CPU** | 1 vCPU | 1 vCPU | 0.5 vCPU |
| **Requests/tháng** | Unlimited | 2M requests | Unlimited |
| **Build time** | 10 phút | 15 phút | 10 phút |
| **Sleep policy** | 7 ngày không dùng | Instant | 15 phút |
| **Custom domain** | ✅ Free | ✅ Free | ✅ Free |
| **SSL** | ✅ Auto | ✅ Auto | ✅ Auto |
| **Deploy time** | 5-10 phút | 3-5 phút | 5-8 phút |

### Khuyến Nghị

1. **Streamlit Cloud** - Dễ nhất, đủ dùng ⭐⭐⭐⭐⭐
2. **Google Cloud Run** - Nếu cần performance cao
3. **Render** - Nếu không thích Streamlit Cloud

---

## 🎯 HƯỚNG DẪN NHANH: DEPLOY STREAMLIT CLOUD (5 PHÚT)

### TL;DR - Các Bước Tối Thiểu

```bash
# 1. Push code lên GitHub
cd "/Volumes/ổ cứng C/DA-test"
git init
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "logs/*.log" >> .gitignore
echo "data/vectorstore/" >> .gitignore
git add .
git commit -m "Initial commit"
# Tạo repo trên github.com
git remote add origin https://github.com/YOUR_USERNAME/humibot.git
git push -u origin main

# 2. Tạo packages.txt
echo "tesseract-ocr" > packages.txt
echo "tesseract-ocr-vie" >> packages.txt
echo "poppler-utils" >> packages.txt
git add packages.txt
git commit -m "Add packages"
git push

# 3. Deploy trên Streamlit Cloud
# - Truy cập: https://share.streamlit.io/
# - Sign in with GitHub
# - New app → chọn repo → app.py
# - Add secret: GOOGLE_API_KEY = "your_key"
# - Deploy!

# 4. Trỏ DNS
# - Vào trang quản lý domain
# - CNAME: @ → your-app.streamlit.app
# - CNAME: www → your-app.streamlit.app

# 5. Setup keep-alive
# - Đăng ký UptimeRobot.com
# - Add monitor: https://humibot.id.vn
# - Done!
```

---

## 🔧 TỐI ƯU CHO FREE TIER

### 1. Giảm Kích Thước Docker Image

Nếu dùng Cloud Run hoặc Render, tối ưu Dockerfile:

```dockerfile
# Sử dụng slim image
FROM python:3.10-slim

# Chỉ cài packages cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements và install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

CMD streamlit run app.py
```

### 2. Giảm RAM Usage

Trong `config/config.yaml`:

```yaml
retrieval:
  top_k: 3  # Giảm từ 5 xuống 3

embedding:
  batch_size: 16  # Giảm từ 32 xuống 16
```

### 3. Lazy Loading

Trong `app.py`, đảm bảo dùng `@st.cache_resource` (đã có):

```python
@st.cache_resource(show_spinner="🤖 Đang khởi tạo chatbot...")
def load_chatbot():
    return StudentSupportChatbot()
```

### 4. Optimize Vectorstore

Nếu vectorstore quá lớn (>100MB), có thể:

1. Upload lên Google Drive
2. Download lúc startup

```python
# Thêm vào đầu app.py
import os
import gdown

if not os.path.exists('data/vectorstore/chroma.sqlite3'):
    os.makedirs('data/vectorstore', exist_ok=True)
    # Download từ Google Drive
    gdown.download_folder(
        'https://drive.google.com/drive/folders/YOUR_FOLDER_ID',
        output='data/vectorstore/',
        quiet=False
    )
```

---

## 🐛 Troubleshooting Free Deployments

### Issue 1: "Out of Memory" trên Streamlit Cloud

**Giải pháp:**
```python
# Trong app.py, giới hạn cache size
@st.cache_resource(max_entries=5)
def load_chatbot():
    return StudentSupportChatbot()
```

### Issue 2: App Sleep Liên Tục

**Giải pháp:**
- Setup UptimeRobot ping mỗi 5 phút
- Hoặc dùng GitHub Actions workflow

### Issue 3: Build Timeout

**Giải pháp:**
- Tối ưu requirements.txt, chỉ giữ packages cần thiết
- Dùng pre-built wheels

### Issue 4: Custom Domain Không Hoạt Động

**Kiểm tra:**
```bash
# Check DNS
nslookup humibot.id.vn

# Check CNAME
dig humibot.id.vn CNAME

# Đợi 24h để DNS propagate
```

---

## 📈 Monitoring & Analytics (Free)

### Google Analytics (Free)

Thêm vào `app.py`:

```python
# Google Analytics
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YOUR_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-YOUR_ID');
</script>
""", unsafe_allow_html=True)
```

### UptimeRobot (Free)

- Uptime monitoring
- Email alerts
- Status page

### Sentry (Free tier)

Error tracking:

```bash
pip install sentry-sdk
```

```python
# Trong app.py
import sentry_sdk
sentry_sdk.init(dsn="your_dsn_here")
```

---

## ✅ Checklist Deploy Free

### Trước Deploy
- [ ] Code đã push lên GitHub (public repo)
- [ ] `.gitignore` đã loại trừ `.env` và vectorstore
- [ ] `packages.txt` đã tạo (cho system dependencies)
- [ ] Google API key đã có

### Streamlit Cloud
- [ ] Đã đăng ký Streamlit Cloud
- [ ] App đã deploy thành công
- [ ] Secret `GOOGLE_API_KEY` đã thêm
- [ ] Custom domain đã cấu hình
- [ ] DNS records đã thêm
- [ ] UptimeRobot đã setup

### Testing
- [ ] Website mở được tại humibot.id.vn
- [ ] SSL hoạt động (https)
- [ ] Chatbot trả lời câu hỏi
- [ ] Không có error trong logs

---

## 💰 Chi Phí Ước Tính

| Phương Án | Setup | Hàng Tháng | Hàng Năm |
|-----------|-------|------------|----------|
| **Streamlit Cloud** | $0 | $0 | $0 |
| **Google Cloud Run** | $0 | $0* | $0* |
| **Render** | $0 | $0 | $0 |
| **Domain (đã mua)** | - | - | - |

*Trong free tier limits

**Tổng chi phí: $0/tháng** ✅

---

## 🚀 Kết Luận

### Khuyến Nghị Cuối Cùng

**Cho người mới bắt đầu:**
→ **Streamlit Cloud** (Dễ nhất, không cần config gì)

**Cho người có kinh nghiệm:**
→ **Google Cloud Run** (Performance tốt, scale tốt)

**Nếu cần đơn giản + không sleep:**
→ **Streamlit Cloud + UptimeRobot**

### Next Steps

1. Chọn phương án (khuyến nghị: Streamlit Cloud)
2. Follow hướng dẫn từng bước
3. Deploy trong 10-30 phút
4. Website live tại humibot.id.vn
5. Hoàn toàn MIỄN PHÍ! 🎉

---

**Chúc bạn deploy thành công với $0! 🆓🚀**

