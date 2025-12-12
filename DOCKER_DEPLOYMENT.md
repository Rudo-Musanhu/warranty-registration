# Docker Deployment Guide for Warranty Register

## Prerequisites

- Docker installed on your Linux server
- Docker Compose installed
- Git installed

## Directory Structure

```
warranty_register/
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
├── .dockerignore
├── .env.docker
├── manage.py
├── requirements.txt
└── ... (rest of Django project files)
```

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Rudo-Musanhu/warranty-registration.git
cd warranty_register
```

### 2. Configure Environment Variables

Edit `.env.docker` with your production settings:

```bash
# For production, change these:
DEBUG=False
SECRET_KEY=your-secret-key-here  # Generate a new secret key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database credentials (change passwords!)
POSTGRES_PASSWORD=your-secure-password

# CORS settings (add your frontend URLs)
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://app.your-domain.com
```

### 3. Build and Start Containers

```bash
# Build images
docker-compose build

# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx
```

### 4. Create Superuser (One-time setup)

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the Application

- Django Admin: http://your-server-ip/admin/
- Web App: http://your-server-ip/
- API: http://your-server-ip/api/warranty/

## Service Details

### Database (PostgreSQL)
- Container: `warranty_db`
- Port: 5432 (internal only, not exposed to host by default)
- Data persists in `postgres_data` volume

### Django Application
- Container: `warranty_django`
- Port: 8000 (internal)
- Static files served by Nginx
- Media files in `/app/media`

### Nginx Web Server
- Container: `warranty_nginx`
- Port: 80 (HTTP) and 443 (HTTPS)
- Reverse proxy to Django app
- Serves static/media files

## Common Commands

```bash
# View running containers
docker-compose ps

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes database!)
docker-compose down -v

# Restart services
docker-compose restart

# View service logs
docker-compose logs -f

# Run Django management commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Access container shell
docker-compose exec web bash
docker-compose exec db psql -U postgres -d warranty_db
```

## Production Configuration

### 1. Enable HTTPS

Uncomment the HTTPS server block in `nginx.conf` and place your SSL certificates:

```bash
mkdir -p ssl
# Add your certificate and key files
cp /path/to/cert.pem ssl/
cp /path/to/key.pem ssl/
```

### 2. Update ALLOWED_HOSTS

In `.env.docker`:
```
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

### 3. Generate New SECRET_KEY

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 4. Set DEBUG to False

```
DEBUG=False
```

### 5. Database Backups

```bash
# Backup database
docker-compose exec db pg_dump -U postgres warranty_db > backup.sql

# Restore from backup
docker-compose exec -T db psql -U postgres warranty_db < backup.sql
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs web

# Rebuild images
docker-compose build --no-cache
```

### Database connection issues

```bash
# Check if database is running
docker-compose exec db pg_isready -U postgres

# Connect to database
docker-compose exec db psql -U postgres
```

### Static files not loading

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Restart nginx
docker-compose restart nginx
```

### Permission issues

```bash
# Run with sudo if needed
sudo docker-compose up -d
```

## Performance Optimization

### Increase Gunicorn Workers

Edit `docker-compose.yml` and change the Django command:

```yaml
command: >
  sh -c "python manage.py migrate &&
         python manage.py collectstatic --noinput &&
         gunicorn warranty_backend.wsgi:application --bind 0.0.0.0:8000 --workers 4"
```

### Enable Caching in Nginx

Caching is already configured in `nginx.conf` for static and media files.

### Database Connection Pooling

For production, consider using pgBouncer. Edit `docker-compose.yml` to add:

```yaml
pgbouncer:
  image: pgbouncer/pgbouncer
  # ... configuration
```

## Monitoring

### Check disk space
```bash
df -h
```

### Monitor container resource usage
```bash
docker stats
```

### View error logs
```bash
docker-compose logs --tail=100 web
```

## Security Best Practices

1. Use strong database passwords
2. Use environment variables for sensitive data (don't commit `.env.docker`)
3. Keep Docker images updated
4. Use HTTPS in production
5. Regularly backup the database
6. Monitor logs for suspicious activity
7. Implement rate limiting in Nginx
8. Keep SECRET_KEY secure

## Support

For issues or questions, refer to:
- Docker Documentation: https://docs.docker.com/
- Django Documentation: https://docs.djangoproject.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Nginx Documentation: https://nginx.org/en/docs/
