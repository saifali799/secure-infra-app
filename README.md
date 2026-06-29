 Secure Multi-Tier System Infrastructure Monitor

A hardened, production-ready 3-tier web application architecture designed to monitor system health and resource metrics in real-time. Built with a focus on container security, strict access control, and robust network segmentation.



 🛡️ Core Infrastructure & Hardening Features
Multi-Stage Frontend Build:** Optimized via an Alpine-Nginx base image. The container drops root privileges (`USER nginx`) at runtime and implements custom Content-Security-Policy (CSP) headers to neutralize Cross-Site Scripting (XSS).
Isolated Backend API:** A lightweight FastAPI server running under an explicitly declared unprivileged user ID (`10001`), ensuring that runtime container escape attacks are completely blocked.
* **Network Segmentation:** Orchestrated with Docker Compose into isolated network layers:
    * `frontend-network` (DMZ bridge for user-facing traffic)
    * `backend-network` (Internal zone, keeping the API layer completely hidden from public access)
* **Real-Time Data Collection:** Leverages native Linux utilities via Python `psutil` to dynamically fetch live VM health statistics on request, entirely eliminating the attack surface of an open local database.



Deployment Instructions

Prerequisites
* Docker & Docker Compose installed
* Linux Environment (Ubuntu/Debian preferred)

 Running the Infrastructure
1. Clone this repository to your environment.
2. Spin up the segmented architecture using Docker Compose:
   ```bash
   docker compose up -d
