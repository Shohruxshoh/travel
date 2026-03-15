#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# SSL Certificate Setup for silk-road-trip.com
# Run this AFTER docker-compose is up and running
# ═══════════════════════════════════════════════════════════════

set -e

DOMAIN="silk-road-trip.com"
EMAIL="shohruxnasriddinov98@gmail.com"

echo "🔐 Getting SSL certificate for $DOMAIN..."

# Step 1: Get SSL certificate via certbot (without www — DNS not configured for it)
docker compose -f docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    -d $DOMAIN \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email

# Step 2: Switch to SSL nginx config
echo "📝 Switching to SSL nginx config..."
cp nginx/nginx.ssl.conf nginx/nginx.prod.conf

# Step 3: Restart nginx to apply SSL
echo "🔄 Restarting nginx..."
docker compose -f docker-compose.prod.yml restart nginx

echo "✅ SSL setup complete! Site is now available at https://$DOMAIN"
