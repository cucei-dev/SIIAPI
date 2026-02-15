# Deployment Guide

This guide covers deploying SIIAPI to production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Database Setup](#database-setup)
- [Application Deployment](#application-deployment)
- [Docker Deployment](#docker-deployment)
- [Security Considerations](#security-considerations)
- [Monitoring](#monitoring)
- [Backup and Recovery](#backup-and-recovery)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **OS**: Linux (Ubuntu 20.04+ recommended) or similar
- **Python**: 3.10 or higher
- **Database**: PostgreSQL 13+ or MySQL 8+
- **Memory**: Minimum 2GB RAM (4GB+ recommended)
- **Storage**: Minimum 10GB available space

### Required Software

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.10 python3.10-venv python3-pip -y

# Install PostgreSQL (recommended)
sudo apt install postgresql postgresql-contrib -y

# Or install MySQL
sudo apt install mysql-server -y

# Install Nginx (for reverse proxy)
sudo apt install nginx -y

# Install supervisor (for process management)
sudo apt install supervisor -y
```

## Environment Setup

### 1. Create Application User

```bash
sudo useradd -m -s /bin/bash siiapi
sudo su - siiapi
```

### 2. Clone Repository

```bash
cd /home/siiapi
git clone <repository-url> app
cd app
```

### 3. Create Virtual Environment

```bash
python3.10 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create `.env` file:

```bash
nano .env
```

Production configuration:

```env
# Database - PostgreSQL
DB_URL=postgresql://siiapi_user:secure_password@localhost/siiapi_db

# Application
APP_NAME=SIIAPI
APP_SITE=yourdomain.com
APP_ENV=production
APP_DESCRIPTION=University Academic Information API
APP_DEBUG=false

# Security - IMPORTANT: Generate secure keys!
SECRET_KEY=<generate-secure-random-key-here>
DUMMY_HASH=<generate-bcrypt-hash-here>

# SIIAU Integration
SIIAU_URL=https://siiau.udg.mx/wco/sspseca.consulta_oferta
```

### 6. Generate Secure Keys

```python
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate DUMMY_HASH
python3 -c "from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt']).hash('dummy'))"
```

## Database Setup

### PostgreSQL Setup

#### 1. Create Database and User

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE siiapi_db;
CREATE USER siiapi_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE siiapi_db TO siiapi_user;
\q
```

#### 2. Configure PostgreSQL

Edit `/etc/postgresql/13/main/pg_hba.conf`:

```
# Add this line
local   siiapi_db   siiapi_user   md5
```

Restart PostgreSQL:

```bash
sudo systemctl restart postgresql
```

#### 3. Initialize Database

```bash
# As siiapi user
cd /home/siiapi/app
source venv/bin/activate
python -c "from app.core.database import init_db; init_db()"
```

### MySQL Setup

#### 1. Create Database and User

```bash
sudo mysql
```

```sql
CREATE DATABASE siiapi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'siiapi_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON siiapi_db.* TO 'siiapi_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 2. Update Connection String

```env
DB_URL=mysql://siiapi_user:secure_password@localhost/siiapi_db
```

## Application Deployment

### Option 1: Systemd Service

#### 1. Create Service File

```bash
sudo nano /etc/systemd/system/siiapi.service
```

```ini
[Unit]
Description=SIIAPI FastAPI Application
After=network.target postgresql.service

[Service]
Type=notify
User=siiapi
Group=siiapi
WorkingDirectory=/home/siiapi/app
Environment="PATH=/home/siiapi/app/venv/bin"
ExecStart=/home/siiapi/app/venv/bin/uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 2. Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable siiapi
sudo systemctl start siiapi
sudo systemctl status siiapi
```

### Option 2: Supervisor

#### 1. Create Supervisor Configuration

```bash
sudo nano /etc/supervisor/conf.d/siiapi.conf
```

```ini
[program:siiapi]
command=/home/siiapi/app/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/home/siiapi/app
user=siiapi
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/siiapi/app.log
environment=PATH="/home/siiapi/app/venv/bin"
```

#### 2. Create Log Directory

```bash
sudo mkdir -p /var/log/siiapi
sudo chown siiapi:siiapi /var/log/siiapi
```

#### 3. Start Application

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start siiapi
sudo supervisorctl status siiapi
```

### Nginx Reverse Proxy

#### 1. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/siiapi
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Static files (if any)
    location /static {
        alias /home/siiapi/app/static;
        expires 30d;
    }
}
```

#### 2. Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/siiapi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 3. SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Create non-root user
RUN useradd -m -u 1000 siiapi && chown -R siiapi:siiapi /app
USER siiapi

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: siiapi_db
      POSTGRES_USER: siiapi_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - siiapi_network

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DB_URL: postgresql://siiapi_user:secure_password@db/siiapi_db
      APP_NAME: SIIAPI
      APP_SITE: yourdomain.com
      APP_ENV: production
      APP_DEBUG: "false"
      SECRET_KEY: ${SECRET_KEY}
      DUMMY_HASH: ${DUMMY_HASH}
      SIIAU_URL: https://siiau.udg.mx/wco/sspseca.consulta_oferta
    depends_on:
      - db
    networks:
      - siiapi_network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    networks:
      - siiapi_network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  siiapi_network:
    driver: bridge
```

### 3. Build and Run

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Security Considerations

### 1. Firewall Configuration

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

### 2. Database Security

- Use strong passwords
- Restrict database access to localhost
- Regular security updates
- Enable SSL connections

### 3. Application Security

- Never commit `.env` file
- Use strong SECRET_KEY
- Enable HTTPS only
- Implement rate limiting
- Regular dependency updates

### 4. CORS Configuration

Add to `app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5. Rate Limiting

Install slowapi:

```bash
pip install slowapi
```

Add to `app/main.py`:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

## Monitoring

### 1. Application Logs

```bash
# Systemd
sudo journalctl -u siiapi -f

# Supervisor
tail -f /var/log/siiapi/app.log

# Docker
docker-compose logs -f api
```

### 2. System Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Monitor resources
htop
```

### 3. Database Monitoring

```bash
# PostgreSQL
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"

# MySQL
mysql -u root -p -e "SHOW PROCESSLIST;"
```

### 4. Health Check Endpoint

Add to `app/main.py`:

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

Monitor with:

```bash
curl http://localhost:8000/health
```

## Backup and Recovery

### Database Backup

#### PostgreSQL

```bash
# Backup
pg_dump -U siiapi_user siiapi_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U siiapi_user siiapi_db < backup_20240101.sql
```

#### MySQL

```bash
# Backup
mysqldump -u siiapi_user -p siiapi_db > backup_$(date +%Y%m%d).sql

# Restore
mysql -u siiapi_user -p siiapi_db < backup_20240101.sql
```

### Automated Backups

Create backup script `/home/siiapi/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/home/siiapi/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U siiapi_user siiapi_db > $BACKUP_DIR/db_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete

# Compress old backups
find $BACKUP_DIR -name "db_*.sql" -mtime +1 -exec gzip {} \;
```

Add to crontab:

```bash
crontab -e
# Add: 0 2 * * * /home/siiapi/backup.sh
```

## Troubleshooting

### Application Won't Start

```bash
# Check logs
sudo journalctl -u siiapi -n 50

# Check if port is in use
sudo netstat -tulpn | grep 8000

# Check permissions
ls -la /home/siiapi/app
```

### Database Connection Issues

```bash
# Test connection
psql -U siiapi_user -d siiapi_db -h localhost

# Check PostgreSQL status
sudo systemctl status postgresql

# Check logs
sudo tail -f /var/log/postgresql/postgresql-13-main.log
```

### High Memory Usage

```bash
# Check processes
ps aux | grep uvicorn

# Reduce workers in systemd service
# Edit: --workers 2 (instead of 4)
```

### SSL Certificate Issues

```bash
# Renew certificate
sudo certbot renew

# Check certificate
sudo certbot certificates
```

## Performance Optimization

### 1. Database Optimization

```sql
-- Add indexes
CREATE INDEX idx_seccion_nrc ON seccion(nrc);
CREATE INDEX idx_materia_clave ON materia(clave);
CREATE INDEX idx_user_email ON user(email);

-- Analyze tables
ANALYZE;
```

### 2. Application Optimization

- Use connection pooling
- Enable response caching
- Optimize database queries
- Use async operations

### 3. Nginx Optimization

```nginx
# Enable gzip compression
gzip on;
gzip_types text/plain text/css application/json application/javascript;

# Enable caching
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m;
```

## Scaling

### Horizontal Scaling

1. Deploy multiple API instances
2. Use load balancer (Nginx, HAProxy)
3. Shared database
4. Session storage in Redis

### Vertical Scaling

1. Increase server resources
2. Optimize database
3. Increase worker count
4. Enable caching

---

## Maintenance Checklist

- [ ] Regular security updates
- [ ] Database backups
- [ ] Log rotation
- [ ] SSL certificate renewal
- [ ] Dependency updates
- [ ] Performance monitoring
- [ ] Disk space monitoring
- [ ] Database optimization

---

For additional support, refer to the [README](../README.md) and [Architecture](ARCHITECTURE.md) documentation.