#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up your VPS for the Expense API..."

# 1. Update system packages
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y git curl wget

# 2. Install Docker
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    sudo apt-get install -y ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    
    echo \
      "deb [arch=\"$(dpkg --print-architecture)\" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
      
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
    echo "✅ Docker is already installed."
fi

# 3. Setup firewall (UFW)
echo "🛡️ Configuring Firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 8000/tcp  # Allow API port
sudo ufw --force enable

echo "✅ Server setup complete! Now you can deploy your app."
echo "👉 Run: docker compose up -d --build"
