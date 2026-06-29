# --- Stage 1: Build & Dependency Resolution ---
FROM python:3.12-slim AS builder

WORKDIR /build

# Install compilation tools if any dependencies require binary extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and compile dependencies into a local user directory footprint
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: Final Secure Runtime Image ---
FROM python:3.12-slim AS runtime

# Set the working directory inside the container
WORKDIR /app

# Create a dedicated, unprivileged system user and group (UID/GID 10001)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /sbin/nologin appuser

# Copy only compiled packages from the builder stage into the new unprivileged user space
COPY --from=builder /root/.local /home/appuser/.local

# Copy the application source code files (copies the 'app' directory into /app/app)
COPY --chown=appuser:appgroup app/ ./app/

# Document the application network port
EXPOSE 8000

# Set environment variables for clean stream outputs and paths
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Enforce explicit unprivileged execution boundary
USER 10001:10001

# Run the server using the exact working directory path flag we tested locally
# Since our COPY command places 'app/' into '/app/app/', the current directory is '/app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]