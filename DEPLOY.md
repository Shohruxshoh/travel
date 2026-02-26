# 🚀 Deployment Guide — adventures-travel-time.com

## Server Requirements
- **OS:** Ubuntu 22.04+
- **RAM:** 2GB+
- **Docker** + **Docker Compose** installed
- **Nginx** installed on server (for SSL + reverse proxy)
- **Domain:** `adventures-travel-time.com` → server IP (A record)

## Ports Used
| Service | Port |
|---------|------|
| Frontend | 5173 |
| Backend API | 9001 |

---

## Step 1: Upload Project to Server

```bash
scp -r ./travel root@YOUR_SERVER_IP:/opt/travel
ssh root@YOUR_SERVER_IP
cd /opt/travel
```

---

## Step 2: Setup .env

```bash
cp backend/.env.prod backend/.env
nano backend/.env   # Change ADMIN_PASSWORD!
```

---

## Step 3: Start Services

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

---

## Step 4: Setup Server Nginx + SSL

**4a. Copy nginx config:**
```bash
cp nginx/nginx.conf /etc/nginx/sites-available/adventures-travel-time.com
ln -s /etc/nginx/sites-available/adventures-travel-time.com /etc/nginx/sites-enabled/
```

**4b. Get SSL certificate:**
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d adventures-travel-time.com -d www.adventures-travel-time.com
```

**4c. Restart nginx:**
```bash
nginx -t && systemctl restart nginx
```

---

## Step 5: Verify

```bash
docker-compose -f docker-compose.prod.yml ps
curl -I https://adventures-travel-time.com
```

---

## Useful Commands

```bash
# Restart
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up --build -d

# Logs
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f celery-worker

# DB Backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U travel_user travel_db > backup.sql

# Update
git pull && docker-compose -f docker-compose.prod.yml up --build -d
```

---

## Architecture

```
Client → Server Nginx (80/443 SSL)
           ├── / → localhost:5173 (Frontend container)
           └── /api/ → localhost:9001 (Backend container)

Docker internal:
  Frontend (Nginx:80) ──proxy──→ Backend:8000
  Celery Worker → Redis → PostgreSQL
```
