#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# SSL Certificate Setup for adventures-travel-time.com
# Run this AFTER docker-compose is up and running:
#   bash ssl-init.sh
# ═══════════════════════════════════════════════════════════════

set -e

DOMAIN="adventures-travel-time.com"
EMAIL="shohruxnasriddinov98@gmail.com"

echo "🔐 Getting SSL certificate for $DOMAIN..."

# Step 1: Get SSL certificate via certbot
docker-compose -f docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    -d $DOMAIN \
    -d www.$DOMAIN \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email

# Step 2: Switch to SSL nginx config
echo "📝 Switching to SSL nginx config..."
cp nginx/nginx.ssl.conf nginx/nginx.prod.conf

# Step 3: Restart nginx to apply SSL
echo "🔄 Restarting nginx..."
docker-compose -f docker-compose.prod.yml restart nginx

echo "✅ SSL setup complete! Site is now available at https://$DOMAIN"
echo ""
echo "To auto-renew certificates, add this cron job:"
echo "  0 0 1 * * cd $(pwd) && docker-compose -f docker-compose.prod.yml run --rm certbot renew && docker-compose -f docker-compose.prod.yml restart nginx"
