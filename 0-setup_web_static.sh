#!/usr/bin/env bash
# sets up web static for airbnb project

apt update
apt install -y nginx
ufw allow 'Nginx HTTP'

mkdir  -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

echo "Web Static" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data
chgrp -R ubuntu /data

echo "server {
        listen 80 default_server;
        listen [::]:80 default_server;
        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;
        add_header X-Served-By $HOSTNAME;

        location /hbnb_static/ {
            alias /data/web_static/current/;
            index index.html;
        }
}" > /etc/nginx/sites-available/default

service nginx restart
