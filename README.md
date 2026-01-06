# Warranty Register

A Django-based backend for registering and managing asset warranties, with a React (Next.js) frontend. Supports PostgreSQL, Nginx, Docker Compose, and SSL via Let's Encrypt.

## Features
- User authentication (JWT, Django web login)
- Register and list asset warranties
- REST API for frontend integration
- CORS and CSRF protection for secure cross-domain requests
- SSL/TLS support with Let's Encrypt
- Production-ready with Docker Compose, Nginx, and PostgreSQL

## Project Structure
```
manage.py
requirements.txt
warranty/           # Django app
warranty_backend/   # Django project settings
nginx.conf          # Nginx reverse proxy config
Dockerfile          # Django app Dockerfile
docker-compose.yml  # Multi-container orchestration
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- (For local dev) Python 3.10+, pip

### Local Development
1. Clone the repo:
   ```
   git clone <your-repo-url>
   cd warranty_register
   ```
2. Create a `.env` file (optional, for secrets).
3. Build and run with Docker Compose:
   ```
   docker compose up --build
   ```
4. Access Django at http://localhost:8000

### Production Deployment
1. Set up your server with Docker, Docker Compose, and a domain (e.g., server6.eport.ws).
2. Obtain SSL certificates with Let's Encrypt (Certbot):
   ```
   sudo certbot certonly --standalone -d your-domain.com
   ```
3. Update `docker-compose.yml` to mount SSL certs into the nginx service.
4. Update `nginx.conf` to enable HTTPS and redirect HTTP to HTTPS.
5. Restart containers:
   ```
   docker compose down
   docker compose up -d
   ```

### API Usage
- Base URL: `https://your-domain.com/api/warranty/`
- Register warranty (POST `/register/`):
  ```json
  {
    "asset_id": "A12345",
    "asset_name": "Dell Laptop",
    "serial_number": "SN987654321",
    "purchase_date": "2025-12-01"
  }
  ```
- JWT login: POST `/login/` with username & password

### Frontend
- Example React/Next.js frontend at: https://assetwarranty.vercel.app
- CORS and CSRF configured for cross-domain requests

## Security
- CORS and CSRF settings in `settings.py`
- SSL via Let's Encrypt
- Use strong secrets in production

## License
MIT

---
For more details, see the code and comments in each file. Contributions welcome!
