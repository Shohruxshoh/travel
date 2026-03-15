# 🚀 Deployment Guide — silk-road-trip.com

## Server Requirements
- **OS:** Ubuntu 22.04+
- **RAM:** 2GB+
- **Docker** + **Docker Compose** installed
- **Domain:** `silk-road-trip.com` → server IP (A record)

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

## Step 3: Start All Services (One Command!)

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

✅ Site is now live at `http://silk-road-trip.com`

---

## Step 4: Enable SSL (HTTPS)

```bash
bash ssl-init.sh
```

✅ Site is now live at `https://silk-road-trip.com`

---

## Step 5: Verify

```bash
docker-compose -f docker-compose.prod.yml ps
curl -I https://silk-road-trip.com
```

---

## Architecture

```
Client → Nginx container (80/443)
           ├── /        → Frontend container (Vue SPA)
           └── /api/    → Backend container (FastAPI)

Docker internal network:
  Nginx ──→ Frontend (Nginx:80)
  Nginx ──→ Backend (Uvicorn:9000)
  Backend → PostgreSQL + Redis
  Celery Worker → Redis → PostgreSQL
```

---

## Useful Commands

```bash
# Restart all
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up --build -d

# Logs
docker-compose -f docker-compose.prod.yml logs -f nginx
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f celery-worker

# DB Backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U travel_user travel_db > backup.sql

# Update code
git pull && docker-compose -f docker-compose.prod.yml up --build -d

# Renew SSL certificate
docker-compose -f docker-compose.prod.yml run --rm certbot renew
docker-compose -f docker-compose.prod.yml restart nginx
```
