#!/bin/bash

echo "Starting Grabify deployment..."

# Update system packages
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required system packages
echo "Installing required packages..."
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib

# Create PostgreSQL database and user
echo "Setting up PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE grabify;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE grabify TO $DB_USER;"

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set up Django
echo "Setting up Django..."
python manage.py collectstatic --noinput
python manage.py migrate --settings=blog_project.settings_prod

# Set up Nginx
echo "Setting up Nginx..."
sudo rm -f /etc/nginx/sites-enabled/default
sudo tee /etc/nginx/sites-available/grabify << EOF
server {
    listen 80;
    server_name $DOMAIN_NAME;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/grabify;
    }
    
    location /media/ {
        root /home/ubuntu/grabify;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/grabify /etc/nginx/sites-enabled

# Set up Gunicorn service
echo "Setting up Gunicorn..."
sudo tee /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=Gunicorn daemon for Grabify
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/grabify
Environment="PATH=/home/ubuntu/grabify/venv/bin"
ExecStart=/home/ubuntu/grabify/venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    blog_project.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Create log directory
sudo mkdir -p /var/log/django
sudo chown -R ubuntu:ubuntu /var/log/django

# Start services
echo "Starting services..."
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart nginx

# Set up SSL with Certbot
echo "Setting up SSL..."
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d $DOMAIN_NAME --non-interactive --agree-tos --email $EMAIL

echo "Deployment complete! Your site should be available at https://$DOMAIN_NAME" 