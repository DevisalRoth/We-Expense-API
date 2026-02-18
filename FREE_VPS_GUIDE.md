# 🚀 How to Get a FREE VPS (Forever)

You chose **Cloud Free Tier**. The best options for a completely free VPS that is powerful enough to run your API are **Oracle Cloud** and **Google Cloud**.

Here is a guide to getting set up.

---

## 🏆 Option 1: Oracle Cloud "Always Free" (Recommended)
Oracle gives the most generous free tier. You get a powerful ARM server with 4 CPUs and 24GB RAM for free, forever.

### Steps:
1.  **Sign Up**: Go to [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/).
    *   *Note: You will need a credit card for identity verification, but they won't charge you unless you upgrade.*
2.  **Create a VM Instance**:
    *   **Image**: Ubuntu 22.04 or 24.04.
    *   **Shape**: Select **Ampere (ARM)** -> **VM.Standard.A1.Flex**.
    *   **OCPUs**: 4
    *   **Memory**: 24 GB
3.  **SSH Key**: Download the private key they generate for you (or upload your own).
4.  **Networking**: In the "Primary VNIC" section, make sure "Assign a public IPv4 address" is checked.
5.  **Create**: Click Create. It takes a few minutes.

### Connecting:
```bash
ssh -i /path/to/private.key ubuntu@<YOUR_PUBLIC_IP>
```

---

## 🥈 Option 2: Google Cloud Platform (GCP) Free Tier
Good alternative, but less powerful (only 1GB RAM, shared CPU).

### Steps:
1.  **Sign Up**: Go to [Google Cloud Free Tier](https://cloud.google.com/free).
2.  **Create VM**: Go to **Compute Engine** -> **VM Instances**.
3.  **Region**: Must be `us-west1`, `us-central1`, or `us-east1` (check current free tier regions).
4.  **Machine Type**: `e2-micro` (2 vCPUs, 1GB RAM).
5.  **Boot Disk**: Change to "Standard persistent disk" (30GB is free).
6.  **Firewall**: Check "Allow HTTP traffic" and "Allow HTTPS traffic".

---

## 🥉 Option 3: AWS Free Tier (12 Months Only)
Amazon gives you a free server (t2.micro or t3.micro) for **12 months only**. After that, you pay.

1.  **Sign Up**: [AWS Free Tier](https://aws.amazon.com/free/).
2.  **Launch Instance**: Select **EC2**.
3.  **AMI**: Ubuntu Server 22.04 LTS.
4.  **Instance Type**: `t2.micro` or `t3.micro` (look for the "Free tier eligible" badge).

---

## 🛠️ Next Steps (After Getting Your Server)

Once you have your server IP and SSH access:

1.  **Open the Port**: You need to allow traffic on port `8000`.
    *   **Oracle**: Go to VCN -> Security Lists -> Ingress Rules. Add Rule: Source `0.0.0.0/0`, Protocol `TCP`, Port `8000`.
    *   **GCP/AWS**: Go to Security Groups / Firewall. Add Rule: Custom TCP, Port `8000`, Source `0.0.0.0/0`.

2.  **Run the Setup Script**:
    From your local computer:
    ```bash
    # Upload setup script
    scp -i /path/to/key setup_vps.sh ubuntu@<IP>:~/setup_vps.sh
    
    # Connect
    ssh -i /path/to/key ubuntu@<IP>
    
    # Run setup
    chmod +x setup_vps.sh
    ./setup_vps.sh
    ```

3.  **Deploy App**: Follow the steps in `DEPLOY.md`!
