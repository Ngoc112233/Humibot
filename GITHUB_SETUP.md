# 🚀 PUSH CODE LÊN GITHUB - HƯỚNG DẪN

**Code đã được commit xong! Bây giờ chỉ cần push lên GitHub.**

---

## ✅ Đã Hoàn Thành

```
✓ Git repository đã được khởi tạo
✓ 42 files đã được commit thành công
✓ Ready to push!
```

---

## 📋 3 BƯỚC TIẾP THEO

### BƯỚC 1: Tạo Repository Trên GitHub (2 phút)

1. **Truy cập:** https://github.com/new

2. **Điền thông tin:**
   - **Repository name:** `humibot` (hoặc tên bạn muốn)
   - **Description:** `HumiBot - USSH Student Support Chatbot with RAG`
   - **Visibility:** 
     - ✅ **Public** (khuyến nghị - cần cho Streamlit Cloud free tier)
     - ⚠️ Private (chỉ nếu dùng paid plans)
   
3. **QUAN TRỌNG:** 
   - ❌ **KHÔNG** tick "Add a README file"
   - ❌ **KHÔNG** tick "Add .gitignore"
   - ❌ **KHÔNG** tick "Choose a license"
   
   *(Vì chúng ta đã có sẵn)*

4. **Click:** "Create repository" màu xanh

### BƯỚC 2: Copy URL Repository

Sau khi tạo xong, GitHub sẽ hiển thị màn hình với URL.

**Ví dụ URL:**
```
https://github.com/YOUR_USERNAME/humibot.git
```

**Copy URL này!** (Click nút copy bên cạnh)

### BƯỚC 3: Push Code Lên GitHub

Mở Terminal và chạy các lệnh sau:

```bash
# Di chuyển vào thư mục project
cd "/Volumes/ổ cứng C/DA-test"

# Thêm remote repository (thay YOUR_USERNAME bằng username GitHub của bạn)
git remote add origin https://github.com/YOUR_USERNAME/humibot.git

# Đổi tên branch thành main (nếu cần)
git branch -M main

# Push code lên GitHub
git push -u origin main
```

**Nhập username và password khi được hỏi:**
- Username: `your_github_username`
- Password: **Personal Access Token** (KHÔNG phải password thông thường)

---

## 🔑 Tạo Personal Access Token (Nếu Chưa Có)

GitHub không cho dùng password thông thường để push code. Bạn cần tạo Personal Access Token:

### Cách Tạo Token:

1. **Truy cập:** https://github.com/settings/tokens

2. **Click:** "Generate new token" → "Generate new token (classic)"

3. **Điền:**
   - **Note:** `HumiBot deployment`
   - **Expiration:** 90 days (hoặc No expiration)
   - **Select scopes:** 
     - ✅ Tick `repo` (toàn bộ)
     - ✅ Tick `workflow` (nếu dùng GitHub Actions)

4. **Click:** "Generate token"

5. **QUAN TRỌNG:** Copy token này ngay! (chỉ hiện 1 lần)
   ```
   ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

6. **Dùng token này làm password** khi push

---

## 💻 Lệnh Push Đầy Đủ

```bash
# 1. Di chuyển vào thư mục
cd "/Volumes/ổ cứng C/DA-test"

# 2. Thêm remote (THAY YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/humibot.git

# 3. Push
git push -u origin main
```

**Khi được hỏi:**
```
Username for 'https://github.com': YOUR_USERNAME
Password for 'https://YOUR_USERNAME@github.com': [PASTE TOKEN Ở ĐÂY]
```

---

## ✅ Kiểm Tra Thành Công

Sau khi push xong, bạn sẽ thấy:

```
Enumerating objects: 52, done.
Counting objects: 100% (52/52), done.
Delta compression using up to 8 threads
Compressing objects: 100% (47/47), done.
Writing objects: 100% (52/52), 245.67 KiB | 8.52 MiB/s, done.
Total 52 (delta 3), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR_USERNAME/humibot.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**Truy cập GitHub repository của bạn:**
```
https://github.com/YOUR_USERNAME/humibot
```

Bạn sẽ thấy toàn bộ code đã được upload! 🎉

---

## 🔒 Bảo Mật

### Files Đã KHÔNG được commit (an toàn):

✅ `.env` (chứa API keys) - KHÔNG có trên GitHub
✅ `data/vectorstore/` (vector database lớn) - KHÔNG có
✅ `logs/*.log` - KHÔNG có
✅ `__pycache__/` - KHÔNG có

### Kiểm Tra:

```bash
# Xem files đã được commit
git ls-files

# Xem files bị ignore
git status --ignored
```

---

## 📝 Lưu Token An Toàn (Optional)

Nếu không muốn nhập token mỗi lần push, có thể lưu credentials:

```bash
# Git sẽ nhớ credentials
git config --global credential.helper store

# Hoặc cache trong 1 giờ
git config --global credential.helper 'cache --timeout=3600'
```

---

## 🐛 Troubleshooting

### Issue 1: "Authentication failed"

**Nguyên nhân:** Token sai hoặc hết hạn

**Giải pháp:**
- Tạo token mới: https://github.com/settings/tokens
- Đảm bảo tick `repo` scope

### Issue 2: "remote origin already exists"

**Giải pháp:**
```bash
# Xóa remote cũ
git remote remove origin

# Thêm lại
git remote add origin https://github.com/YOUR_USERNAME/humibot.git
```

### Issue 3: "Updates were rejected"

**Giải pháp:**
```bash
# Pull trước (nếu remote có thay đổi)
git pull origin main --allow-unrelated-histories

# Rồi push
git push -u origin main
```

### Issue 4: Push chậm/timeout

**Nguyên nhân:** File quá lớn hoặc mạng chậm

**Giải pháp:**
```bash
# Tăng timeout
git config --global http.postBuffer 524288000

# Push lại
git push -u origin main
```

---

## 📊 Files Được Commit

```
✓ 42 files total:

📄 Deployment configs:
  - Dockerfile
  - docker-compose.yml
  - nginx/humibot.conf
  - systemd/humibot.service
  - requirements.txt
  - packages.txt
  - env.example

📄 Source code:
  - app.py (Streamlit UI)
  - chatbot.py (CLI)
  - src/*.py (Core modules)

📄 Scripts:
  - scripts/deploy.sh
  - scripts/setup_server.sh
  - scripts/process_documents.py
  - scripts/check_prerequisites.sh

📄 Documentation:
  - README.md
  - DEPLOYMENT.md
  - DEPLOY_FREE.md
  - QUICKSTART.md
  - METHODOLOGY.md

📄 Configuration:
  - config/config.yaml
  - .streamlit/config.toml
  - .github/workflows/keep-alive.yml

📄 Sample documents:
  - data/documents/*.txt
  - data/documents/moi.pdf
```

---

## 🎯 Sau Khi Push Xong

### Option 1: Deploy Lên Streamlit Cloud (Free)

Xem file: `DEPLOY_FREE.md`

**Các bước ngắn gọn:**
1. Truy cập: https://share.streamlit.io/
2. Sign in with GitHub
3. New app → Chọn repo `humibot`
4. Main file: `app.py`
5. Add secret: `GOOGLE_API_KEY`
6. Deploy!

### Option 2: Deploy Lên VPS

Xem file: `DEPLOY_STEPS.md` hoặc `DEPLOYMENT.md`

**Clone từ GitHub trên server:**
```bash
# Trên server
cd /opt
git clone https://github.com/YOUR_USERNAME/humibot.git
cd humibot
sudo bash scripts/setup_server.sh
```

---

## 🔄 Cập Nhật Code Sau Này

Khi có thay đổi code:

```bash
# 1. Kiểm tra thay đổi
git status

# 2. Stage changes
git add .

# 3. Commit
git commit -m "Update: mô tả thay đổi"

# 4. Push
git push origin main
```

---

## 📞 Quick Commands Reference

```bash
# Xem status
git status

# Xem history
git log --oneline

# Xem remote
git remote -v

# Xem branch
git branch

# Pull latest
git pull origin main

# Push changes
git push origin main
```

---

## ✨ Next Steps

1. ✅ Push code lên GitHub (bạn đang ở đây)
2. 🚀 Deploy lên Streamlit Cloud (xem `DEPLOY_FREE.md`)
3. 🌐 Cấu hình domain `humibot.id.vn`
4. 🎉 Website live!

---

**Chúc bạn push thành công! 🚀**

*Nếu gặp vấn đề, check phần Troubleshooting ở trên.*

