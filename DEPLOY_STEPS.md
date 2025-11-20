# 🚀 TRIỂN KHAI HUMIBOT LÊN humibot.id.vn

**Tóm tắt các bước đã chuẩn bị xong và bước tiếp theo**

---

## ✅ Đã Chuẩn Bị Xong

Tôi đã tạo đầy đủ các file cần thiết cho deployment:

### 📁 Deployment Files
```
✅ requirements.txt          - Python dependencies
✅ Dockerfile                - Container configuration
✅ docker-compose.yml        - Multi-container orchestration
✅ .dockerignore             - Optimize build
✅ nginx/humibot.conf        - Nginx reverse proxy config
✅ systemd/humibot.service   - Systemd service
✅ env.example               - Environment template
```

### 🔧 Automation Scripts
```
✅ scripts/setup_server.sh         - Tự động setup server (1 lần)
✅ scripts/deploy.sh               - Deploy/update application
✅ scripts/check_prerequisites.sh  - Kiểm tra server sẵn sàng
```

### 📖 Documentation
```
✅ DEPLOYMENT.md      - Hướng dẫn chi tiết đầy đủ
✅ QUICK_DEPLOY.md    - Hướng dẫn nhanh 30 phút
✅ DEPLOY_STEPS.md    - File này (tóm tắt)
```

---

## 🎯 3 BƯỚC TIẾP THEO

### BƯỚC 1: Thuê VPS/Server

**Khuyến nghị: DigitalOcean**
- Link: https://www.digitalocean.com/
- Cấu hình: Ubuntu 22.04, 4GB RAM, 2 CPU (~$24/tháng)
- Region: Singapore (gần Việt Nam)

**Alternative:**
- Vultr: https://www.vultr.com/
- Azdigi (VN): https://azdigi.com/ (200-400k/tháng)

**Sau khi tạo, bạn có:**
- IP address: `xxx.xxx.xxx.xxx`
- Root password hoặc SSH key

### BƯỚC 2: Cấu Hình DNS

Đăng nhập trang quản lý domain → DNS Settings:

| Type | Name | Value (IP server) | TTL |
|------|------|-------------------|-----|
| A    | @    | xxx.xxx.xxx.xxx   | 3600 |
| A    | www  | xxx.xxx.xxx.xxx   | 3600 |

**Đợi 10-20 phút để DNS propagate**

Kiểm tra:
```bash
ping humibot.id.vn
# Phải thấy IP của server
```

### BƯỚC 3: Deploy Code Lên Server

#### 3A. Upload Code

**Option 1: Từ máy local**
```bash
# Nén project
cd "/Volumes/ổ cứng C/DA-test"
tar -czf humibot.tar.gz \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='venv' \
    --exclude='.git' \
    --exclude='logs/*.log' \
    .

# Upload lên server
scp humibot.tar.gz root@xxx.xxx.xxx.xxx:/tmp/

# SSH vào server
ssh root@xxx.xxx.xxx.xxx

# Extract
mkdir -p /opt/humibot
cd /opt/humibot
tar -xzf /tmp/humibot.tar.gz
```

**Option 2: Qua GitHub (Khuyến nghị)**
```bash
# Push code lên GitHub trước (từ máy local)
cd "/Volumes/ổ cứng C/DA-test"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/humibot.git
git push -u origin main

# Clone trên server
ssh root@xxx.xxx.xxx.xxx
cd /opt
git clone https://github.com/your-username/humibot.git
cd humibot
```

#### 3B. Chạy Setup Script

**QUAN TRỌNG:** Sửa email trong script trước:
```bash
nano scripts/setup_server.sh
# Tìm dòng: EMAIL="admin@humibot.id.vn"
# Đổi thành email của bạn để nhận thông báo SSL
# Ctrl+X, Y, Enter
```

**Chạy setup:**
```bash
chmod +x scripts/*.sh
sudo bash scripts/setup_server.sh
```

⏱️ Thời gian: ~10 phút

Script sẽ tự động:
- ✅ Cài Docker, Docker Compose, Nginx
- ✅ Setup SSL certificate (Let's Encrypt)
- ✅ Cấu hình firewall
- ✅ Tạo systemd service

#### 3C. Cấu Hình .env

```bash
cp env.example .env
nano .env
```

**Thay đổi:**
```bash
# QUAN TRỌNG: Điền API key thật
GOOGLE_API_KEY=AIzaSy...your_real_key_here

# Các dòng khác giữ nguyên
APP_ENV=production
DOMAIN=humibot.id.vn
```

**Lấy Google API Key:**
1. https://makersuite.google.com/app/apikey
2. Đăng nhập → Create API Key
3. Copy và paste vào .env

Lưu: `Ctrl+X`, `Y`, `Enter`

#### 3D. Xử Lý Documents

```bash
# Nếu chưa có documents, upload từ local:
# (Terminal mới trên máy local)
scp -r data/documents/* root@xxx.xxx.xxx.xxx:/opt/humibot/data/documents/

# Quay lại server, xử lý
python3 scripts/process_documents.py
```

⏱️ Thời gian: ~2-5 phút

#### 3E. Deploy Application

```bash
sudo bash scripts/deploy.sh
```

⏱️ Thời gian: ~5 phút

**Nếu thành công:**
```
✅ Deployment completed successfully!
Access your application at: https://humibot.id.vn
```

---

## 🎉 Kiểm Tra

Mở browser:
- https://humibot.id.vn

**Test chat:**
- "Điều kiện tốt nghiệp USSH là gì?"
- "Quy định về điểm danh?"

**Nếu chatbot trả lời → Hoàn thành! 🚀**

---

## 📊 Quản Lý Production

### Xem Logs
```bash
docker-compose logs -f
```

### Restart Application
```bash
sudo systemctl restart humibot
# hoặc
docker-compose restart
```

### Update Code
```bash
cd /opt/humibot
git pull origin main
sudo bash scripts/deploy.sh
```

### Check Status
```bash
# Container status
docker ps

# Health check
curl http://localhost:8501/_stcore/health

# Nginx
sudo systemctl status nginx

# SSL certificate
sudo certbot certificates
```

---

## 🐛 Troubleshooting

### Website không mở?
```bash
# Check services
sudo systemctl status nginx
docker ps

# Restart
sudo systemctl restart nginx
docker-compose restart
```

### SSL Error?
```bash
sudo certbot renew --force-renewal
sudo systemctl reload nginx
```

### Application Error?
```bash
# Xem logs
docker-compose logs --tail=50

# Restart
docker-compose restart
```

---

## 📚 Tài Liệu Chi Tiết

- **Hướng dẫn nhanh:** `QUICK_DEPLOY.md`
- **Hướng dẫn đầy đủ:** `DEPLOYMENT.md`
- **Check server:** `bash scripts/check_prerequisites.sh`

---

## 📞 Checklist Deploy

- [ ] Đã thuê VPS/server
- [ ] Đã cấu hình DNS (humibot.id.vn → IP server)
- [ ] Đã upload code lên server
- [ ] Đã chạy `setup_server.sh`
- [ ] Đã tạo file `.env` với Google API key
- [ ] Đã xử lý documents (`process_documents.py`)
- [ ] Đã chạy `deploy.sh`
- [ ] Website mở được tại https://humibot.id.vn
- [ ] SSL certificate hoạt động (khóa xanh)
- [ ] Chatbot trả lời câu hỏi đúng

---

## ⏱️ Ước Tính Thời Gian

| Bước | Thời gian |
|------|-----------|
| Thuê VPS | 5-10 phút |
| Cấu hình DNS | 5 phút + 15 phút chờ |
| Upload code | 2-5 phút |
| Setup server | 10-15 phút |
| Cấu hình & deploy | 10 phút |
| **Tổng** | **~45-60 phút** |

---

## 🎯 Next Steps Sau Khi Deploy

1. **Test kỹ:** Thử nhiều loại câu hỏi
2. **Monitor:** Theo dõi logs trong vài ngày đầu
3. **Setup monitoring:** UptimeRobot (https://uptimerobot.com/)
4. **Backup:** Kiểm tra backup tự động
5. **Security:** Review firewall rules
6. **Share:** Chia sẻ với sinh viên!

---

**🚀 Chúc bạn deploy thành công!**

*Nếu gặp vấn đề, xem `DEPLOYMENT.md` hoặc kiểm tra troubleshooting section.*

