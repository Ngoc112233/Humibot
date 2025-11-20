#!/bin/bash

# ==========================================
# HumiBot Deployment Script
# ==========================================
# Tự động deploy và cập nhật HumiBot

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="humibot"
APP_DIR="/opt/humibot"
BACKUP_DIR="/opt/humibot-backups"
LOG_FILE="/var/log/humibot-deploy.log"

# Functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   error "This script must be run as root (use sudo)"
fi

log "=========================================="
log "Starting HumiBot Deployment"
log "=========================================="

# 1. Check prerequisites
log "Checking prerequisites..."
command -v docker >/dev/null 2>&1 || error "Docker is not installed"
command -v docker-compose >/dev/null 2>&1 || error "Docker Compose is not installed"
success "Prerequisites check passed"

# 2. Backup current deployment (if exists)
if [ -d "$APP_DIR" ]; then
    log "Creating backup..."
    BACKUP_NAME="${APP_NAME}-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    cp -r "$APP_DIR" "$BACKUP_DIR/$BACKUP_NAME"
    success "Backup created: $BACKUP_DIR/$BACKUP_NAME"
fi

# 3. Pull latest code (if git repo)
if [ -d "$APP_DIR/.git" ]; then
    log "Pulling latest code..."
    cd "$APP_DIR"
    git pull origin main || warning "Git pull failed, using local code"
else
    warning "Not a git repository, using existing code"
fi

# 4. Check .env file
cd "$APP_DIR"
if [ ! -f .env ]; then
    error ".env file not found. Please create it from env.example"
fi
success ".env file found"

# 5. Stop existing containers
log "Stopping existing containers..."
docker-compose down || true
success "Containers stopped"

# 6. Pull/build images
log "Building Docker images..."
docker-compose build --no-cache
success "Images built successfully"

# 7. Start containers
log "Starting containers..."
docker-compose up -d
success "Containers started"

# 8. Wait for health check
log "Waiting for application to be healthy..."
sleep 10
RETRY=0
MAX_RETRIES=30
while [ $RETRY -lt $MAX_RETRIES ]; do
    if curl -f http://localhost:8501/_stcore/health >/dev/null 2>&1; then
        success "Application is healthy!"
        break
    fi
    RETRY=$((RETRY+1))
    log "Health check attempt $RETRY/$MAX_RETRIES..."
    sleep 2
done

if [ $RETRY -eq $MAX_RETRIES ]; then
    error "Application failed to become healthy"
fi

# 9. Show container status
log "Container status:"
docker-compose ps

# 10. Show logs
log "Recent logs:"
docker-compose logs --tail=20

log "=========================================="
success "Deployment completed successfully!"
log "=========================================="
log "Access your application at: https://humibot.id.vn"
log "To view logs: docker-compose logs -f"
log "To restart: docker-compose restart"
log "To stop: docker-compose down"

