#!/usr/bin/env bash
# Set up a cron job for certificate renewal
echo "0 0 * * * certbot renew --nginx --non-interactive >> /var/log/certbot.log" | crontab -

# Start Nginx
service nginx start
# Start uWSGI
uwsgi --ini uwsgi.ini