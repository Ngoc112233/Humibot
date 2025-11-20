#!/bin/bash

# ==========================================
# HumiBot Prerequisites Checker
# ==========================================
# Kiểm tra xem server đã sẵn sàng deploy chưa

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
PASS=0
FAIL=0
WARN=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARN++))
}

echo -e "${BLUE}=========================================="
echo "HumiBot Prerequisites Check"
echo -e "==========================================${NC}\n"

# 1. Check OS
echo -e "${BLUE}[1] Checking Operating System...${NC}"
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    if [[ "$ID" == "ubuntu" ]] || [[ "$ID" == "debian" ]]; then
        check_pass "OS: $PRETTY_NAME"
    else
        check_warn "OS: $PRETTY_NAME (Ubuntu/Debian recommended)"
    fi
else
    check_warn "Cannot detect OS"
fi

# 2. Check if running as root
echo -e "\n${BLUE}[2] Checking privileges...${NC}"
if [[ $EUID -eq 0 ]]; then
    check_pass "Running as root"
else
    check_warn "Not running as root (some checks may fail)"
fi

# 3. Check CPU
echo -e "\n${BLUE}[3] Checking CPU...${NC}"
CPU_CORES=$(nproc)
if [[ $CPU_CORES -ge 2 ]]; then
    check_pass "CPU cores: $CPU_CORES (minimum: 2)"
else
    check_fail "CPU cores: $CPU_CORES (minimum required: 2)"
fi

# 4. Check Memory
echo -e "\n${BLUE}[4] Checking Memory...${NC}"
TOTAL_MEM=$(free -g | awk '/^Mem:/{print $2}')
if [[ $TOTAL_MEM -ge 4 ]]; then
    check_pass "RAM: ${TOTAL_MEM}GB (minimum: 4GB)"
elif [[ $TOTAL_MEM -ge 2 ]]; then
    check_warn "RAM: ${TOTAL_MEM}GB (recommended: 4GB)"
else
    check_fail "RAM: ${TOTAL_MEM}GB (minimum required: 4GB)"
fi

# 5. Check Disk Space
echo -e "\n${BLUE}[5] Checking Disk Space...${NC}"
DISK_AVAIL=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
if [[ $DISK_AVAIL -ge 20 ]]; then
    check_pass "Disk space: ${DISK_AVAIL}GB available (minimum: 20GB)"
elif [[ $DISK_AVAIL -ge 10 ]]; then
    check_warn "Disk space: ${DISK_AVAIL}GB available (recommended: 20GB)"
else
    check_fail "Disk space: ${DISK_AVAIL}GB available (minimum required: 20GB)"
fi

# 6. Check Docker
echo -e "\n${BLUE}[6] Checking Docker...${NC}"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
    check_pass "Docker installed: $DOCKER_VERSION"
    
    # Check Docker running
    if systemctl is-active --quiet docker; then
        check_pass "Docker service is running"
    else
        check_fail "Docker service is not running"
    fi
else
    check_fail "Docker is not installed"
    echo "  Install: curl -fsSL https://get.docker.com | sh"
fi

# 7. Check Docker Compose
echo -e "\n${BLUE}[7] Checking Docker Compose...${NC}"
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version | awk '{print $4}' | sed 's/,//')
    check_pass "Docker Compose installed: $COMPOSE_VERSION"
else
    check_fail "Docker Compose is not installed"
    echo "  Install: sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose"
    echo "           sudo chmod +x /usr/local/bin/docker-compose"
fi

# 8. Check Nginx
echo -e "\n${BLUE}[8] Checking Nginx...${NC}"
if command -v nginx &> /dev/null; then
    NGINX_VERSION=$(nginx -v 2>&1 | awk -F'/' '{print $2}')
    check_pass "Nginx installed: $NGINX_VERSION"
    
    if systemctl is-active --quiet nginx; then
        check_pass "Nginx service is running"
    else
        check_warn "Nginx service is not running"
    fi
else
    check_fail "Nginx is not installed"
    echo "  Install: sudo apt install nginx"
fi

# 9. Check Certbot
echo -e "\n${BLUE}[9] Checking Certbot (for SSL)...${NC}"
if command -v certbot &> /dev/null; then
    CERTBOT_VERSION=$(certbot --version 2>&1 | awk '{print $2}')
    check_pass "Certbot installed: $CERTBOT_VERSION"
else
    check_warn "Certbot is not installed (needed for SSL)"
    echo "  Install: sudo apt install certbot python3-certbot-nginx"
fi

# 10. Check Git
echo -e "\n${BLUE}[10] Checking Git...${NC}"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    check_pass "Git installed: $GIT_VERSION"
else
    check_warn "Git is not installed (optional)"
    echo "  Install: sudo apt install git"
fi

# 11. Check Python
echo -e "\n${BLUE}[11] Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    check_pass "Python3 installed: $PYTHON_VERSION"
else
    check_fail "Python3 is not installed"
    echo "  Install: sudo apt install python3 python3-pip"
fi

# 12. Check Network
echo -e "\n${BLUE}[12] Checking Network...${NC}"
if ping -c 1 google.com &> /dev/null; then
    check_pass "Internet connection: OK"
else
    check_fail "No internet connection"
fi

# 13. Check Ports
echo -e "\n${BLUE}[13] Checking Required Ports...${NC}"
check_port() {
    PORT=$1
    NAME=$2
    if netstat -tuln 2>/dev/null | grep -q ":$PORT " || ss -tuln 2>/dev/null | grep -q ":$PORT "; then
        check_warn "Port $PORT ($NAME) is already in use"
    else
        check_pass "Port $PORT ($NAME) is available"
    fi
}

if command -v netstat &> /dev/null || command -v ss &> /dev/null; then
    check_port 80 "HTTP"
    check_port 443 "HTTPS"
    check_port 8501 "Streamlit"
else
    check_warn "Cannot check ports (netstat/ss not installed)"
fi

# 14. Check Firewall
echo -e "\n${BLUE}[14] Checking Firewall...${NC}"
if command -v ufw &> /dev/null; then
    if ufw status | grep -q "Status: active"; then
        check_pass "UFW firewall is active"
        
        # Check if ports are allowed
        if ufw status | grep -q "80/tcp"; then
            check_pass "Port 80 is allowed in firewall"
        else
            check_warn "Port 80 not allowed in firewall"
        fi
        
        if ufw status | grep -q "443/tcp"; then
            check_pass "Port 443 is allowed in firewall"
        else
            check_warn "Port 443 not allowed in firewall"
        fi
    else
        check_warn "UFW firewall is not active"
    fi
else
    check_warn "UFW not installed"
fi

# 15. Check .env file
echo -e "\n${BLUE}[15] Checking Configuration...${NC}"
if [[ -f .env ]]; then
    check_pass ".env file exists"
    
    # Check if GOOGLE_API_KEY is set
    if grep -q "GOOGLE_API_KEY=.*[A-Za-z0-9]" .env; then
        check_pass "GOOGLE_API_KEY is configured"
    else
        check_fail "GOOGLE_API_KEY not configured in .env"
    fi
else
    check_fail ".env file not found"
    echo "  Create: cp env.example .env"
fi

# 16. Check Documents
echo -e "\n${BLUE}[16] Checking Documents...${NC}"
if [[ -d data/documents ]]; then
    DOC_COUNT=$(find data/documents -type f \( -name "*.pdf" -o -name "*.txt" -o -name "*.docx" \) | wc -l)
    if [[ $DOC_COUNT -gt 0 ]]; then
        check_pass "Found $DOC_COUNT document(s) in data/documents/"
    else
        check_warn "No documents found in data/documents/"
    fi
else
    check_warn "data/documents/ directory not found"
fi

# 17. Check Vectorstore
echo -e "\n${BLUE}[17] Checking Vectorstore...${NC}"
if [[ -d data/vectorstore ]]; then
    if [[ -f data/vectorstore/chroma.sqlite3 ]]; then
        check_pass "Vectorstore exists"
    else
        check_warn "Vectorstore not initialized"
        echo "  Run: python3 scripts/process_documents.py"
    fi
else
    check_warn "Vectorstore directory not found"
fi

# Summary
echo -e "\n${BLUE}=========================================="
echo "Summary"
echo -e "==========================================${NC}"
echo -e "${GREEN}✓ Passed:${NC} $PASS"
echo -e "${YELLOW}⚠ Warnings:${NC} $WARN"
echo -e "${RED}✗ Failed:${NC} $FAIL"

echo ""
if [[ $FAIL -eq 0 ]]; then
    echo -e "${GREEN}✓ System is ready for deployment!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Configure .env file (if not done)"
    echo "  2. Process documents: python3 scripts/process_documents.py"
    echo "  3. Deploy: sudo bash scripts/deploy.sh"
    exit 0
else
    echo -e "${RED}✗ System is NOT ready for deployment${NC}"
    echo ""
    echo "Please fix the failed checks before deploying."
    echo "Run this script again after fixing: bash scripts/check_prerequisites.sh"
    exit 1
fi

