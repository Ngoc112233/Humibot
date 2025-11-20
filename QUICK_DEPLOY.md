# ⚡ QUICK DEPLOY GUIDE - HUMIBOT

**Triển khai HumiBot lên humibot.id.vn trong 30 phút!**

---

## 🎯 TÓM TẮT

```bash
1. Thuê VPS (DigitalOcean, Vultr, etc.)
2. Trỏ DNS: humibot.id.vn → IP server
3. Chạy 3 lệnh trên server
4. Done! ✅
```

---

## BƯỚC 1: Thuê VPS (5 phút)

### Khuyến nghị: DigitalOcean

**Link:** https://www.digitalocean.com/

**Cấu hình:**
- **Image:** Ubuntu 22.04 LTS
- **Plan:** Basic - 4GB RAM / 2 CPU ($24/tháng)
- **Region:** Singapore (gần VN)
- **Authentication:** SSH Key (hoặc Password)

**Sau khi tạo, bạn nhận được:**
```
IP: xxx.xxx.xxx.xxx
Password: your_password (qua email)
```

**Alternative:**
- Vultr: https://www.vultr.com/ (tương tự giá)
- Azdigi (VN): https://azdigi.com/ (200-400k/tháng)

---

## BƯỚC 2: Cấu Hình DNS (10 phút)

### Trỏ Domain về Server

Đăng nhập trang quản lý domain → DNS Settings:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | `xxx.xxx.xxx.xxx` | 3600 |
| A | www | `xxx.xxx.xxx.xxx` | 3600 |

**Đợi 5-15 phút để DNS propagate.**

**Kiểm tra:**
```bash
ping humibot.id.vn
# Phải thấy IP của server
```

---

## BƯỚC 3: Deploy (15 phút)

### 3.1. SSH vào Server

```bash
ssh root@xxx.xxx.xxx.xxx
# Nhập password (nếu không dùng SSH key)
```

### 3.2. Upload Code

**Cách 1: Upload từ máy local (nếu chưa có Git)**

```bash
# Trên máy local (Terminal mới)
cd /Volumes/ổ\ cứng\ C/DA-test
tar -czf humibot.tar.gz --exclude='__pycache__' --exclude='*.pyc' --exclude='venv' .
scp humibot.tar.gz root@xxx.xxx.xxx.xxx:/tmp/

# Trên server
mkdir -p /opt/humibot
cd /opt/humibot
tar -xzf /tmp/humibot.tar.gz
```

**Cách 2: Clone từ GitHub (khuyến nghị)**

```bash
# Push code lên GitHub trước
cd /opt
git clone https://github.com/your-username/humibot.git
cd humibot
```

### 3.3. Chạy Setup (Tự Động)

```bash
# Cấp quyền
chmod +x scripts/*.sh

# QUAN TRỌNG: Sửa email trong script trước
nano scripts/setup_server.sh
# Tìm dòng: EMAIL="admin@humibot.id.vn"
# Đổi thành email của bạn
# Ctrl+X, Y, Enter để lưu

# Chạy setup (sẽ tự động setup mọi thứ)
sudo bash scripts/setup_server.sh
```

**Script sẽ:**
- ✅ Cài Docker, Nginx
- ✅ Setup SSL (Let's Encrypt)
- ✅ Cấu hình firewall
- ✅ Setup systemd service
- ⏱️ Thời gian: ~10 phút

### 3.4. Cấu Hình .env

```bash
# Copy template
cp env.example .env
nano .env
```

**Sửa các dòng sau:**

```bash
# QUAN TRỌNG: Thay your_google_api_key_here bằng API key thật
GOOGLE_API_KEY=AIzaSy...your_actual_key_here

# Các dòng khác giữ nguyên
APP_ENV=production
DOMAIN=humibot.id.vn
```

**Lấy Google API Key:**
1. Mở: https://makersuite.google.com/app/apikey
2. Đăng nhập Google
3. Create API Key
4. Copy và paste vào .env

**Lưu file:** `Ctrl+X`, `Y`, `Enter`

### 3.5. Xử Lý Documents

```bash
# Kiểm tra documents đã có chưa
ls -la data/documents/

# Nếu chưa có, upload từ local:
# (Mở terminal mới trên máy local)
scp -r data/documents/* root@xxx.xxx.xxx.xxx:/opt/humibot/data/documents/

# Quay lại server, chạy xử lý
python3 scripts/process_documents.py
# Nhấn 1 (Create new) hoặc 2 (Update) nếu hỏi
```

### 3.6. Deploy!

```bash
# Chạy deploy script
sudo bash scripts/deploy.sh
```

**Script sẽ:**
1. Build Docker image
2. Start container
3. Wait for health check
4. ⏱️ Thời gian: ~5 phút

**Nếu thành công, sẽ thấy:**
```
✅ Deployment completed successfully!
Access your application at: https://humibot.id.vn
```

---

## BƯỚC 4: Kiểm Tra (2 phút)

### 4.1. Test Website

Mở browser:
- https://humibot.id.vn

**Nếu thấy giao diện chatbot → Thành công! 🎉**

### 4.2. Test Chat

Đặt câu hỏi:
- "Điều kiện tốt nghiệp USSH là gì?"
- "Quy định về điểm danh?"

**Nếu chatbot trả lời được → Hoàn hảo! 🚀**

---

## 🔧 Lệnh Hữu Ích

### Xem Logs

```bash
# Application logs
docker-compose logs -f

# Nginx logs
tail -f /var/log/nginx/humibot_access.log
tail -f /var/log/nginx/humibot_error.log
```

### Restart Application

```bash
# Cách 1: Systemd
sudo systemctl restart humibot

# Cách 2: Docker Compose
cd /opt/humibot
docker-compose restart
```

### Check Status

```bash
# Container status
docker ps

# Application health
curl http://localhost:8501/_stcore/health

# Nginx status
sudo systemctl status nginx

# SSL certificate
sudo certbot certificates
```

### Update Code

```bash
cd /opt/humibot
git pull origin main
sudo bash scripts/deploy.sh
```

---

## 🐛 Troubleshooting Nhanh

### Website không mở được?

```bash
# 1. Check DNS
ping humibot.id.vn

# 2. Check Nginx
sudo systemctl status nginx
sudo systemctl restart nginx

# 3. Check Container
docker ps
docker-compose restart

# 4. Check Firewall
sudo ufw status
```

### SSL Error?

```bash
# Renew SSL
sudo certbot renew --force-renewal
sudo systemctl reload nginx
```

### Application lỗi?

```bash
# Xem logs
docker-compose logs --tail=50

# Restart
docker-compose restart

# Recreate
docker-compose down
docker-compose up -d
```

### Out of Memory?

```bash
# Check memory
free -h

# Restart container
docker-compose restart
```

---

## 📞 Need Help?

### Common Issues

1. **DNS chưa trỏ đúng**
   - Đợi 15-30 phút để DNS propagate
   - Check với: `ping humibot.id.vn`

2. **Google API Key sai**
   - Xem logs: `docker-compose logs | grep API`
   - Check .env file: `cat .env | grep GOOGLE`

3. **Vectorstore chưa có**
   - Chạy: `python3 scripts/process_documents.py`

4. **Port 80/443 bị block**
   - Check firewall: `sudo ufw status`
   - Allow: `sudo ufw allow 80` và `sudo ufw allow 443`

### Xem Full Documentation

Nếu gặp vấn đề phức tạp:
```bash
cat DEPLOYMENT.md
```

---

## ✅ Checklist Cuối Cùng

Sau khi deploy, đảm bảo:

- [ ] Website mở được tại https://humibot.id.vn
- [ ] SSL certificate valid (khóa xanh)
- [ ] Chatbot trả lời câu hỏi
- [ ] Không có error trong logs
- [ ] Health check pass: `curl https://humibot.id.vn/health`

---

## 🎉 Hoàn Thành!

**Xin chúc mừng! HumiBot đã online tại:**

🌐 **https://humibot.id.vn**

### Next Steps:

1. **Test kỹ:** Thử nhiều câu hỏi khác nhau
2. **Monitor:** Theo dõi logs trong vài ngày đầu
3. **Backup:** Đảm bảo backup tự động hoạt động
4. **Share:** Chia sẻ với sinh viên USSH!

### Monitoring

Setup uptime monitoring (free):
- UptimeRobot: https://uptimerobot.com/
- Pingdom: https://www.pingdom.com/

### Maintenance

```bash
# Mỗi tuần, check:
sudo bash scripts/deploy.sh  # Update nếu có code mới
docker system prune -a       # Dọn dẹp Docker images cũ
```

---

**🚀 Happy Deploying!**

*Nếu cần hỗ trợ chi tiết hơn, xem `DEPLOYMENT.md`*

