# Single-stage build using Debian Slim
FROM python:3.12-slim-bookworm

# Install only essential runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    tesseract-ocr-eng \
    tesseract-ocr-fra \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip\
    && pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y pip setuptools wheel \
    && find /usr/local/lib -name '__pycache__' -type d -exec rm -r {} + \
    && find /usr/local/lib -name '*.pyc' -delete

# Copy application code
COPY . .

# Environment configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run the application
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]