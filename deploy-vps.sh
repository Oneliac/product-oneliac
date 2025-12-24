#!/bin/bash

# Healthcare Agents - VPS Deployment Script
# For Ubuntu/Debian servers

echo "🏥 Healthcare Agents - VPS Deployment"
echo "====================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip
echo "🐍 Installing Python..."
sudo apt install python3 python3-pip python3-venv nginx -y

# Create application directory
echo "📁 Setting up application..."
sudo mkdir -p /var/www/healthcare-agents
sudo chown $USER:$USER /var/www/healthcare-agents
cd /var/www/healthcare-agents

# Clone repository (replace with your repo)
echo "📥 Cloning repository..."
git clone https://github.com/yourusername/healthcare-agents.git .

# Create virtual environment
echo "🔧 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r agents/requirements.txt
pip install gunicorn

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/healthcare-agents.service > /dev/null <<EOF
[Unit]
Description=Healthcare Agents API
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=/var/www/healthcare-agents
Environment="PATH=/var/www/healthcare-agents/venv/bin"
Environment="PYTHONPATH=/var/www/healthcare-agents"
ExecStart=/var/www/healthcare-agents/venv/bin/gunicorn --workers 3 --bind unix:healthcare-agents.sock -m 007 agents.api:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/healthcare-agents > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/healthcare-agents/healthcare-agents.sock;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/healthcare-agents /etc/nginx/sites-enabled
sudo nginx -t

# Start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl start healthcare-agents
sudo systemctl enable healthcare-agents
sudo systemctl restart nginx

# Setup firewall
echo "🔒 Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Point your domain to this server's IP"
echo "2. Install SSL certificate: sudo certbot --nginx"
echo "3. Test your API: curl http://your-domain.com/health"
echo ""
echo "📊 Service management:"
echo "• Status: sudo systemctl status healthcare-agents"
echo "• Logs: sudo journalctl -u healthcare-agents -f"
echo "• Restart: sudo systemctl restart healthcare-agents"