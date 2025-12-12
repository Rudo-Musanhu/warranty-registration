FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project
COPY . /app/

# Create static and media directories
RUN mkdir -p /app/warranty_backend/static /app/media

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "warranty_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
