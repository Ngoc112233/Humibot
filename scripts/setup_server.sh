#!/bin/bash

# ==========================================
# HumiBot Server Setup Script
# ==========================================
# Tự động setup server Ubuntu/Debian cho HumiBot

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
APP_NAME="humibot"
APP_DIR="/opt/humibot"
DOMAIN="humibot.id.vn"
USER="humibot"
EMAIL="admin@humibot.id.vn"  # Change this to your email

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   error "This script must be run as root (use sudo)"
fi

log "=========================================="
log "HumiBot Server Setup"
log "=========================================="

# 1. Update system
log "Updating system packages..."
apt-get update
apt-get upgrade -y
success "System updated"

# 2. Install dependencies
log "Installing dependencies..."
apt-get install -y \
    curl \
    git \
    nginx \
    certbot \
    python3-certbot-nginx \
    ufw \
    fail2ban \
    htop \
    vim
success "Dependencies installed"

# 3. Install Docker
if ! command -v docker &> /dev/null; then
    log "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    success "Docker installed"
else
    success "Docker already installed"
fi

# 4. Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    log "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    success "Docker Compose installed"
else
    success "Docker Compose already installed"
fi

# 5. Create application user
if id "$USER" &>/dev/null; then
    success "User $USER already exists"
else
    log "Creating user $USER..."
    useradd -m -s /bin/bash "$USER"
    usermod -aG docker "$USER"
    success "User $USER created"
fi

# 6. Setup firewall
log "Configuring firewall..."
ufw --force enable
ufw allow ssh
ufw allow http
ufw allow https
ufw status
success "Firewall configured"

# 7. Create application directory
log "Creating application directory..."
mkdir -p "$APP_DIR"
chown -R "$USER":"$USER" "$APP_DIR"
success "Application directory created"

# 8. Configure Nginx
log "Configuring Nginx..."
# Copy nginx config (assumes you'll upload it)
if [ -f "$APP_DIR/nginx/humibot.conf" ]; then
    cp "$APP_DIR/nginx/humibot.conf" /etc/nginx/sites-available/humibot
    ln -sf /etc/nginx/sites-available/humibot /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    nginx -t && systemctl reload nginx
    success "Nginx configured"
else
    warning "Nginx config not found, you'll need to configure it manually"
fi

# 9. Setup SSL with Let's Encrypt
log "Setting up SSL certificate..."
certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    --redirect || warning "SSL setup failed, you may need to configure it manually"

# 10. Setup systemd service
log "Setting up systemd service..."
if [ -f "$APP_DIR/systemd/humibot.service" ]; then
    cp "$APP_DIR/systemd/humibot.service" /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable humibot.service
    success "Systemd service configured"
else
    warning "Systemd service file not found"
fi

# 11. Setup automatic backups
log "Setting up backup cron job..."
mkdir -p /opt/humibot-backups
cat > /etc/cron.daily/humibot-backup << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/humibot-backups"
APP_DIR="/opt/humibot"
DATE=$(date +%Y%m%d-%H%M%S)
tar -czf "$BACKUP_DIR/humibot-backup-$DATE.tar.gz" \
    "$APP_DIR/data" \
    "$APP_DIR/.env" \
    "$APP_DIR/config"
# Keep only last 7 days of backups
find "$BACKUP_DIR" -name "humibot-backup-*.tar.gz" -mtime +7 -delete
EOF
chmod +x /etc/cron.daily/humibot-backup
success "Backup cron job configured"

# 12. Setup log rotation
log "Setting up log rotation..."
cat > /etc/logrotate.d/humibot << 'EOF'
/opt/humibot/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 humibot humibot
    sharedscripts
    postrotate
        systemctl reload humibot > /dev/null 2>&1 || true
    endscript
}
EOF
success "Log rotation configured"

# 13. Install monitoring tools (optional)
log "Installing monitoring tools..."
apt-get install -y \
    prometheus-node-exporter \
    netdata || warning "Some monitoring tools failed to install"

log "=========================================="
success "Server setup completed!"
log "=========================================="
log ""
log "Next steps:"
log "1. Upload your application code to: $APP_DIR"
log "2. Create .env file from env.example"
log "3. Process documents: python scripts/process_documents.py"
log "4. Deploy: bash scripts/deploy.sh"
log ""
log "Useful commands:"
log "  - View logs: docker-compose -f $APP_DIR/docker-compose.yml logs -f"
log "  - Restart app: systemctl restart humibot"
log "  - Check status: systemctl status humibot"
log "  - View nginx logs: tail -f /var/log/nginx/humibot_*.log"

