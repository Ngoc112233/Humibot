# 🚀 HƯỚNG DẪN DEPLOY HUMIBOT LÊN PRODUCTION

## 📋 Mục Lục
- [Tổng Quan](#tổng-quan)
- [Yêu Cầu](#yêu-cầu)
- [Phương Án Deploy](#phương-án-deploy)
- [Hướng Dẫn Chi Tiết](#hướng-dẫn-chi-tiết)
- [Cấu Hình Domain](#cấu-hình-domain)
- [SSL/HTTPS](#ssl-https)
- [Monitoring](#monitoring)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Tổng Quan

HumiBot sẽ được deploy lên domain: **humibot.id.vn**

**Kiến trúc deployment:**
```
Internet → DNS → Server → Nginx (Reverse Proxy) → Docker Container → Streamlit App
                    ↓
                  SSL/HTTPS (Let's Encrypt)
```

---

## 💻 Yêu Cầu

### Server Requirements
- **OS**: Ubuntu 20.04/22.04 LTS hoặc Debian 11/12
- **RAM**: 4GB tối thiểu (8GB khuyến nghị)
- **CPU**: 2 cores tối thiểu
- **Disk**: 20GB tối thiểu (50GB khuyến nghị)
- **Network**: Public IP address

### Software Requirements
- Docker 20.10+
- Docker Compose 2.0+
- Nginx 1.18+
- Certbot (cho SSL)

### Domain Requirements
- Domain đã mua: `humibot.id.vn` ✅
- Truy cập DNS settings

---

## 🏗️ Phương Án Deploy

### Option 1: VPS/Cloud Server (KHUYẾN NGHỊ)

**Ưu điểm:**
- ✅ Full control
- ✅ Chi phí thấp
- ✅ Hiệu suất tốt
- ✅ Dễ quản lý

**Nhà cung cấp đề xuất:**
- DigitalOcean (Droplet): $12/tháng
- AWS Lightsail: $10-20/tháng
- Vultr: $10/tháng
- Azdigi (VN): 200k-400k/tháng

### Option 2: Cloud Platform

**Platform-as-a-Service:**
- Google Cloud Run
- AWS ECS
- Azure Container Instances

**Ưu điểm:** Auto-scaling, managed
**Nhược điểm:** Chi phí cao hơn

### Option 3: Shared Hosting (KHÔNG khuyến nghị)

Shared hosting thường không hỗ trợ Docker → không phù hợp

---

## 📖 HƯỚNG DẪN CHI TIẾT

## BƯỚC 1: Chuẩn Bị Server

### 1.1. Thuê VPS

**Khuyến nghị: DigitalOcean Droplet**

```bash
# Cấu hình đề xuất:
- RAM: 4GB
- CPU: 2 cores
- Storage: 50GB SSD
- OS: Ubuntu 22.04 LTS
- Location: Singapore (gần VN)
- Giá: ~$24/tháng
```

**Tạo Droplet:**
1. Đăng ký tài khoản DigitalOcean
2. Create → Droplets
3. Chọn Ubuntu 22.04 LTS
4. Chọn gói 4GB RAM / 2 CPU
5. Chọn region Singapore
6. Add SSH key (khuyến nghị)
7. Create Droplet

Sau vài phút, bạn sẽ nhận được:
- IP address: `xxx.xxx.xxx.xxx`
- Root password (qua email)

### 1.2. Kết Nối Server

```bash
# SSH vào server
ssh root@xxx.xxx.xxx.xxx

# Hoặc nếu dùng SSH key
ssh -i ~/.ssh/id_rsa root@xxx.xxx.xxx.xxx
```

---

## BƯỚC 2: Cấu Hình DNS

### 2.1. Trỏ Domain về Server

Đăng nhập vào trang quản lý domain của bạn, thêm DNS records:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | `xxx.xxx.xxx.xxx` (IP server) | 3600 |
| A | www | `xxx.xxx.xxx.xxx` (IP server) | 3600 |

**Ví dụ với các nhà cung cấp:**

#### Tại Nhà Đăng Ký Domain (VD: GoDaddy, Namecheap)
1. Đăng nhập → My Domains
2. Chọn `humibot.id.vn` → DNS Management
3. Thêm A Record:
   - Host: `@` → Points to: `your_server_ip`
   - Host: `www` → Points to: `your_server_ip`
4. Save

#### Tại Cloudflare (nếu dùng)
1. Add Site → `humibot.id.vn`
2. DNS → Add Record
   - Type: A, Name: `@`, IPv4: `your_server_ip`
   - Type: A, Name: `www`, IPv4: `your_server_ip`
3. Proxy status: OFF (hoặc ON nếu muốn Cloudflare CDN)

**Kiểm tra DNS:**
```bash
# Đợi 5-30 phút để DNS propagate
ping humibot.id.vn
# Nên thấy IP của server bạn
```

---

## BƯỚC 3: Setup Server (Tự Động)

### 3.1. Upload Code Lên Server

**Từ máy local:**

```bash
# Zip toàn bộ project (trừ node_modules, venv, etc)
cd /path/to/DA-test
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

**Hoặc dùng Git (khuyến nghị):**

```bash
# Trên server
cd /opt
git clone https://github.com/your-username/humibot.git
cd humibot
```

### 3.2. Chạy Setup Script

```bash
# Cấp quyền thực thi
chmod +x scripts/setup_server.sh

# Chạy script (sẽ tự động setup mọi thứ)
sudo bash scripts/setup_server.sh
```

**Script sẽ tự động:**
- ✅ Cập nhật hệ thống
- ✅ Cài Docker & Docker Compose
- ✅ Cài Nginx
- ✅ Cấu hình firewall
- ✅ Tạo user `humibot`
- ✅ Setup SSL với Let's Encrypt
- ✅ Cấu hình systemd service
- ✅ Setup backup tự động

**⏱️ Thời gian:** ~10-15 phút

---

## BƯỚC 4: Cấu Hình Application

### 4.1. Tạo File .env

```bash
cd /opt/humibot
cp env.example .env
nano .env
```

**Cấu hình quan trọng:**

```bash
# Google Gemini API (bắt buộc)
GOOGLE_API_KEY=your_actual_api_key_here

# Application
APP_ENV=production
DOMAIN=humibot.id.vn

# Security
SECRET_KEY=your_random_secret_key_here
```

**Lấy Google API Key:**
1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập Google account
3. Create API Key
4. Copy và paste vào .env

**Tạo SECRET_KEY:**
```bash
openssl rand -hex 32
```

**Lưu file:**
- Nhấn `Ctrl + X`
- Nhấn `Y`
- Nhấn `Enter`

### 4.2. Xử Lý Documents

```bash
# Đảm bảo documents đã có trong data/documents/
ls -la data/documents/

# Chạy xử lý documents
python3 scripts/process_documents.py
```

**Nếu chưa có documents:**
```bash
# Upload từ local
scp -r data/documents/* root@xxx.xxx.xxx.xxx:/opt/humibot/data/documents/
```

---

## BƯỚC 5: Deploy Application

### 5.1. Deploy Lần Đầu

```bash
cd /opt/humibot
chmod +x scripts/deploy.sh
sudo bash scripts/deploy.sh
```

**Script sẽ:**
1. Kiểm tra prerequisites
2. Build Docker image
3. Start containers
4. Wait for health check
5. Hiển thị status

**⏱️ Thời gian:** ~5-10 phút (tùy tốc độ network)

### 5.2. Kiểm Tra Deployment

```bash
# Kiểm tra containers
docker ps

# Xem logs
docker-compose logs -f

# Test health check
curl http://localhost:8501/_stcore/health
```

### 5.3. Truy Cập Website

Mở browser và truy cập:
- **HTTP**: http://humibot.id.vn (sẽ redirect sang HTTPS)
- **HTTPS**: https://humibot.id.vn ✅

**Nếu thấy chatbot → Thành công! 🎉**

---

## BƯỚC 6: SSL/HTTPS (Tự Động)

Script `setup_server.sh` đã tự động cấu hình SSL với Let's Encrypt.

### Kiểm Tra SSL

```bash
# Kiểm tra certificate
sudo certbot certificates

# Test SSL configuration
curl -vI https://humibot.id.vn
```

### Renew SSL (Tự Động)

Let's Encrypt certificates tự động renew. Kiểm tra:

```bash
# Dry run renewal
sudo certbot renew --dry-run

# Cron job tự động chạy 2 lần/ngày
cat /etc/cron.d/certbot
```

### Nếu SSL Fail

```bash
# Manual setup SSL
sudo certbot --nginx -d humibot.id.vn -d www.humibot.id.vn

# Reload Nginx
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🔧 Quản Lý Production

### Start/Stop/Restart

```bash
# Sử dụng systemd
sudo systemctl start humibot
sudo systemctl stop humibot
sudo systemctl restart humibot
sudo systemctl status humibot

# Hoặc dùng docker-compose
cd /opt/humibot
docker-compose up -d        # Start
docker-compose down         # Stop
docker-compose restart      # Restart
```

### Xem Logs

```bash
# Application logs
docker-compose logs -f

# Nginx logs
tail -f /var/log/nginx/humibot_access.log
tail -f /var/log/nginx/humibot_error.log

# System logs
journalctl -u humibot -f
```

### Update Code

```bash
# Pull latest code
cd /opt/humibot
git pull origin main

# Redeploy
sudo bash scripts/deploy.sh
```

---

## 📊 Monitoring

### Health Check

```bash
# Automated health check
curl https://humibot.id.vn/health

# Container health
docker ps
docker inspect humibot | grep -A 5 Health
```

### Resource Usage

```bash
# Container stats
docker stats humibot

# System resources
htop

# Disk usage
df -h
du -sh /opt/humibot/*
```

### Setup Monitoring Tools

**Netdata (Đã cài trong setup script):**
- Truy cập: http://your-server-ip:19999
- Real-time system monitoring

**Setup Uptime Monitoring:**
1. Đăng ký UptimeRobot: https://uptimerobot.com
2. Add New Monitor:
   - Type: HTTPS
   - URL: https://humibot.id.vn
   - Interval: 5 minutes
3. Nhận alert qua email nếu down

---

## 💾 Backup & Recovery

### Backup Tự Động

Script đã setup cron job backup hàng ngày:

```bash
# Kiểm tra backups
ls -lh /opt/humibot-backups/

# Backup bao gồm:
# - data/vectorstore (vector database)
# - .env (config)
# - config/ (settings)
```

### Manual Backup

```bash
# Backup toàn bộ
cd /opt
tar -czf humibot-backup-$(date +%Y%m%d).tar.gz humibot/

# Backup chỉ data
tar -czf humibot-data-$(date +%Y%m%d).tar.gz \
    humibot/data/ \
    humibot/.env \
    humibot/config/
```

### Restore từ Backup

```bash
# Stop application
sudo systemctl stop humibot

# Extract backup
cd /opt
tar -xzf humibot-backup-20241120.tar.gz

# Restart
sudo systemctl start humibot
```

### Backup Offsite (Khuyến nghị)

```bash
# Install rclone
curl https://rclone.org/install.sh | sudo bash

# Setup Google Drive hoặc AWS S3
rclone config

# Sync backup to cloud
rclone sync /opt/humibot-backups/ remote:humibot-backups/
```

---

## 🔒 Security Best Practices

### 1. Firewall

```bash
# Đã được setup trong script
sudo ufw status

# Chỉ mở các ports cần thiết:
# - 22 (SSH)
# - 80 (HTTP)
# - 443 (HTTPS)
```

### 2. SSH Hardening

```bash
# Disable root login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
# Set: PasswordAuthentication no (chỉ dùng SSH key)

sudo systemctl restart sshd
```

### 3. Fail2Ban (Đã cài)

```bash
# Check status
sudo fail2ban-client status

# Ban IPs after failed login attempts
```

### 4. Regular Updates

```bash
# Auto security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 5. API Key Security

- ✅ Không commit .env vào Git
- ✅ Rotate API keys định kỳ
- ✅ Monitor API usage
- ✅ Set rate limits

---

## 🐛 Troubleshooting

### Issue 1: Website không truy cập được

**Kiểm tra:**
```bash
# 1. DNS đã trỏ đúng chưa?
ping humibot.id.vn

# 2. Nginx đang chạy?
sudo systemctl status nginx

# 3. Container đang chạy?
docker ps

# 4. Port 8501 có mở?
netstat -tulpn | grep 8501

# 5. Firewall?
sudo ufw status
```

**Fix:**
```bash
# Restart services
sudo systemctl restart nginx
docker-compose restart
```

### Issue 2: SSL Certificate Error

```bash
# Renew certificate
sudo certbot renew --force-renewal

# Check certificate
sudo certbot certificates

# Reload Nginx
sudo systemctl reload nginx
```

### Issue 3: Application Slow/Hanging

```bash
# Check resources
docker stats

# Check logs
docker-compose logs --tail=100

# Restart container
docker-compose restart
```

### Issue 4: Out of Memory

```bash
# Check memory
free -h

# Add swap (if needed)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Issue 5: Vectorstore Error

```bash
# Recreate vectorstore
cd /opt/humibot
docker-compose exec chatbot python scripts/process_documents.py
```

### Xem Logs Chi Tiết

```bash
# Application logs
docker-compose logs -f chatbot

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# System logs
sudo journalctl -xe
```

---

## 🚀 Performance Optimization

### 1. Nginx Caching

Thêm vào nginx config:

```nginx
# Cache static assets
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 2. Docker Resource Limits

Trong `docker-compose.yml`:

```yaml
services:
  chatbot:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          memory: 2G
```

### 3. Vectorstore Optimization

```yaml
# config/config.yaml
retrieval:
  top_k: 3  # Giảm từ 5 → nhanh hơn
```

### 4. Enable HTTP/2

Đã enabled trong nginx config:
```nginx
listen 443 ssl http2;
```

---

## 📈 Scaling (Tương Lai)

### Horizontal Scaling

```bash
# Multiple instances với load balancer
docker-compose scale chatbot=3
```

### Vertical Scaling

```bash
# Upgrade server resources
# - DigitalOcean: Resize Droplet
# - Thêm RAM/CPU
```

### CDN

```bash
# Sử dụng Cloudflare
# - Free CDN
# - DDoS protection
# - Caching
```

---

## 📞 Support & Maintenance

### Regular Tasks

**Hàng Tuần:**
- ✅ Kiểm tra logs
- ✅ Kiểm tra disk space
- ✅ Review monitoring alerts

**Hàng Tháng:**
- ✅ Update dependencies
- ✅ Review backups
- ✅ Security audit

**Hàng Quý:**
- ✅ Rotate API keys
- ✅ Review performance
- ✅ Update documentation

### Emergency Contacts

```bash
# Nếu server down khẩn cấp:
1. Reboot server: sudo reboot
2. Check logs: journalctl -xe
3. Restore from backup
4. Contact hosting support
```

---

## 🎓 Summary Checklist

Sau khi deploy xong, đảm bảo:

- [ ] ✅ Website accessible tại https://humibot.id.vn
- [ ] ✅ SSL certificate valid (xanh khóa)
- [ ] ✅ Chatbot trả lời câu hỏi đúng
- [ ] ✅ Health check pass
- [ ] ✅ Logs không có errors
- [ ] ✅ Backup tự động hoạt động
- [ ] ✅ Monitoring setup
- [ ] ✅ Firewall configured
- [ ] ✅ DNS records correct

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)

---

## 🎉 Congratulations!

Bạn đã deploy thành công HumiBot lên production!

**URL:** https://humibot.id.vn

**Next Steps:**
1. Test kỹ tất cả tính năng
2. Add thêm documents nếu cần
3. Monitor performance
4. Collect user feedback
5. Iterate and improve

**Good luck! 🚀**

