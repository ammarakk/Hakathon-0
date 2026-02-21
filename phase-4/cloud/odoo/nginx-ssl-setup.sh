#!/bin/bash
# Nginx Reverse Proxy + Let's Encrypt SSL for Odoo
# Phase 4 - Platinum Tier
# Purpose: Configure HTTPS access for Odoo with automatic SSL renewal

set -e

echo "=== Nginx + Let's Encrypt Setup for Odoo ==="
echo ""

# Configuration
DOMAIN="${1:-odoo.example.com}"
ODOO_PORT=8069
NGINX_CONFIG="/etc/nginx/sites-available/odoo"
EMAIL="${2:-admin@${DOMAIN}}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# Check if domain is provided
if [ "$DOMAIN" = "odoo.example.com" ]; then
    echo "Usage: $0 <domain> [email]"
    echo "Example: $0 odoo.yourdomain.com admin@yourdomain.com"
    echo ""
    echo "Using test domain: $DOMAIN (for testing only)"
    read -p "Continue with test domain? (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        echo "Aborted. Please provide your actual domain."
        exit 1
    fi
fi

# Install Nginx
log "Step 1: Installing Nginx..."
sudo apt update >> /var/log/nginx-ssl-setup.log 2>&1
sudo apt install -y nginx certbot python3-certbot-nginx >> /var/log/nginx-ssl-setup.log 2>&1

# Create Nginx configuration
log "Step 2: Configuring Nginx reverse proxy for $DOMAIN..."
sudo tee $NGINX_CONFIG > /dev/null <<EOF
# Upstream Odoo server
upstream odoo {
    server 127.0.0.1:$ODOO_PORT;
}

# HTTP Server - redirect to HTTPS
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        return 301 https://\$host\$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl;
    server_name $DOMAIN;

    # SSL configuration (managed by Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxy settings
    proxy_buffers 16 64k;
    proxy_buffer_size 128k;
    proxy_busy_buffers_size 256k;
    proxy_temp_file_write_size 256k;

    # Increase proxy timeout for long-running operations
    proxy_connect_timeout 600;
    proxy_send_timeout 600;
    proxy_read_timeout 600;
    send_timeout 600;

    # Proxy headers
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host \$host;
    proxy_set_header X-Forwarded-Proto \$scheme;

    # Redirect for longpolling
    location /longpolling {
        proxy_pass http://odoo;
    }

    # Main Odoo proxy
    location / {
        proxy_pass http://odoo;
        proxy_redirect off;
    }

    # Gzip compression
    gzip on;
    gzip_types text/css text/xml text/plain text/x-component application/json application/javascript application/xml+rss;
}
EOF

# Create symbolic link to enable site
log "Step 3: Enabling Nginx site..."
sudo ln -sf $NGINX_CONFIG /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
log "Step 4: Testing Nginx configuration..."
sudo nginx -t >> /var/log/nginx-ssl-setup.log 2>&1

if [ $? -eq 0 ]; then
    log "✓ Nginx configuration is valid"
else
    echo "ERROR: Nginx configuration test failed"
    sudo nginx -t
    exit 1
fi

# Restart Nginx to apply HTTP config
log "Step 5: Restarting Nginx..."
sudo systemctl restart nginx >> /var/log/nginx-ssl-setup.log 2>&1

# Obtain Let's Encrypt SSL certificate
log "Step 6: Obtaining Let's Encrypt SSL certificate..."
sudo certbot --nginx -d $DOMAIN --email $EMAIL --agree-tos --non-interactive >> /var/log/nginx-ssl-setup.log 2>&1

if [ $? -eq 0 ]; then
    log "✓ SSL certificate obtained successfully"
else
    log "ERROR: Failed to obtain SSL certificate"
    log "You may need to:"
    log "  1. Ensure DNS A record points $DOMAIN to this server"
    log "  2. Ensure port 80 is open (firewall)"
    log "  3. Run manually: sudo certbot --nginx -d $DOMAIN"
    exit 1
fi

# Setup auto-renewal cron job
log "Step 7: Setting up SSL auto-renewal..."
(crontab -l 2>/dev/null | grep -q "certbot renew") || \
    (crontab -l 2>/dev/null; echo "0 0,12 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'") | crontab -

# Test HTTPS access
log "Step 8: Testing HTTPS access..."
sleep 5
if curl -sk https://$DOMAIN > /dev/null; then
    log "✓ HTTPS is working on https://$DOMAIN"
else
    log "Warning: HTTPS test failed. Check:"
    log "  1. DNS A record for $DOMAIN"
    log "  2. Firewall allows port 443"
    log "  3. Nginx error logs: sudo tail -f /var/log/nginx/error.log"
fi

# Display completion message
echo ""
echo "=== Nginx + SSL Setup Complete ==="
echo ""
echo "Odoo is now accessible at:"
echo "  HTTP:  http://$DOMAIN (redirects to HTTPS)"
echo "  HTTPS: https://$DOMAIN"
echo ""
echo "SSL Certificate:"
echo "  Auto-renewal configured via cron"
echo "  Certificate location: /etc/letsencrypt/live/$DOMAIN/"
echo ""
echo "Next Steps:"
echo "  1. Access Odoo: https://$DOMAIN"
echo "  2. Create database and admin user"
echo "  3. Test SSL: curl -I https://$DOMAIN"
echo "  4. Check logs: sudo tail -f /var/log/nginx/access.log"
echo ""
echo "SSL Renewal:"
echo "  Automatic: Check crontab -l | grep certbot"
echo "  Manual: sudo certbot renew --dry-run"
echo ""
