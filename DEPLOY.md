# 🚀 How to Deploy Your Own Server (VPS)

You've chosen to run your own server! This gives you full control, better performance, and persistent database connections.

Here is a step-by-step guide to deploying your FastAPI application to a VPS (Virtual Private Server) like DigitalOcean, AWS EC2, or Linode.

## Prerequisites

1.  **A VPS Server**: Recommended specs:
    *   OS: Ubuntu 22.04 LTS (or newer)
    *   RAM: 1GB minimum (2GB recommended)
    *   CPU: 1 vCPU is fine for starting out.
2.  **SSH Access**: You should be able to connect to your server via terminal: `ssh root@your_server_ip`

## Step 1: Prepare Your Server

Connect to your server via SSH and run the provided setup script.

1.  **Copy the setup script to your server**:
    (Run this from your local computer in the `FastAPI` directory)
    ```bash
    scp setup_vps.sh root@<YOUR_SERVER_IP>:~/setup_vps.sh
    ```

2.  **Run the script on the server**:
    ```bash
    ssh root@<YOUR_SERVER_IP>
    chmod +x setup_vps.sh
    ./setup_vps.sh
    ```
    This will install Docker, Docker Compose, and configure the firewall.

## Step 2: Upload Your Code

Now, copy your project files to the server.

1.  **Copy the project folder**:
    (Run this from your local computer, one level above `FastAPI`)
    ```bash
    scp -r FastAPI root@<YOUR_SERVER_IP>:~/app
    ```

    *Alternatively, if your code is on GitHub, you can just `git clone` it on the server.*

## Step 3: Configure Environment Variables

You need to set up your `.env` file on the server.

1.  **SSH into your server**:
    ```bash
    ssh root@<YOUR_SERVER_IP>
    cd ~/app
    ```

2.  **Create/Edit .env file**:
    ```bash
    nano .env
    ```
    Paste your environment variables here (Database URL, Secret Key, etc.).
    
    **IMPORTANT:**
    - Update `DATABASE_URL` to use the **Transaction Pooler (Port 6543)** if using Supabase, or use the direct connection string if you install PostgreSQL on this server too.
    - Since you are running a persistent server, you can use connection pooling more effectively!

## Step 4: Start the Application

1.  **Run with Docker Compose**:
    ```bash
    docker compose up -d --build
    ```

2.  **Check logs**:
    ```bash
    docker compose logs -f
    ```

Your API is now running at `http://<YOUR_SERVER_IP>:8000`!

## (Optional) Step 5: Setup a Domain & HTTPS

To use a domain (e.g., `api.example.com`) and HTTPS:

1.  Buy a domain and point an `A Record` to your server's IP.
2.  Install Nginx and Certbot on the server to handle SSL termination and reverse proxy to port 8000.
