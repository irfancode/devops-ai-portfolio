#!/bin/bash
set -e

# Update system
yum update -y

# Install Python 3 and dependencies
yum install -y python3 python3-pip git

# Create app directory
mkdir -p /opt/app
cd /opt/app

# Copy application files (assumes they're bundled or pulled from repo)
# git clone <repo-url> /opt/app

# Install Python dependencies
pip3 install flask gunicorn psycopg2-binary boto3 prometheus-client

# Create systemd service
cat > /etc/systemd/system/api.service << 'EOF'
[Unit]
Description=AI DevOps API
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/app
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 main:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable api
systemctl start api

# Install node_exporter for Prometheus metrics
NODE_EXPORTER_VERSION="1.6.1"
wget -q "https://github.com/prometheus/node_exporter/releases/download/v${NODE_EXPORTER_VERSION}/node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz"
tar xzf "node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz"
mv "node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64/node_exporter" /usr/local/bin/

cat > /etc/systemd/system/node_exporter.service << EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
Type=simple
User=node_exporter
ExecStart=/usr/local/bin/node_exporter
Restart=always

[Install]
WantedBy=multi-user.target
EOF

useradd --no-create-home --shell /bin/false node_exporter
systemctl daemon-reload
systemctl enable node_exporter
systemctl start node_exporter

echo "Setup complete. API running on port 5000."
