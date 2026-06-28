#!/bin/bash
# Script de déploiement RTVoyage sur VPS Ubuntu 22.04+
# Usage : bash deploy.sh

set -e
APP_DIR="/var/www/rtvoyage"
REPO_URL="https://github.com/VOTRE_USER/SAE24-21_.git"

echo "==> Mise à jour des paquets"
apt-get update -qq && apt-get install -y -qq python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git

echo "==> Clonage / mise à jour du dépôt"
if [ -d "$APP_DIR/.git" ]; then
    git -C "$APP_DIR" pull
else
    git clone "$REPO_URL" "$APP_DIR"
fi

echo "==> Environnement Python"
python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install -q --upgrade pip
"$APP_DIR/venv/bin/pip" install -q -r "$APP_DIR/flask/requirements.txt"

echo "==> Variables d'environnement"
if [ ! -f "$APP_DIR/.env" ]; then
    cp "$APP_DIR/.env.example" "$APP_DIR/.env"
    echo "ATTENTION : Editez $APP_DIR/.env et relancez le script."
    exit 1
fi

echo "==> Migrations de base de données"
cd "$APP_DIR/flask"
"$APP_DIR/venv/bin/flask" db upgrade

echo "==> Service systemd"
cp "$APP_DIR/deploy/rtvoyage.service" /etc/systemd/system/rtvoyage.service
systemctl daemon-reload
systemctl enable rtvoyage
systemctl restart rtvoyage

echo "==> Configuration Nginx"
cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/sites-available/rtvoyage
ln -sf /etc/nginx/sites-available/rtvoyage /etc/nginx/sites-enabled/rtvoyage
nginx -t && systemctl reload nginx

echo "==> Certificat SSL (Let's Encrypt)"
certbot --nginx -d rtvoyage.com -d www.rtvoyage.com --non-interactive --agree-tos -m admin@rtvoyage.com || true

echo ""
echo "✓ Déploiement terminé !"
echo "  Site : https://rtvoyage.com"
echo "  Logs : journalctl -u rtvoyage -f"
