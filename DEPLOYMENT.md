# Deployment Guide for PDF Toolkit

This guide covers various deployment options for the PDF Toolkit web application.

## Table of Contents
1. [Local Development](#local-development)
2. [Production Considerations](#production-considerations)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS EC2 Deployment](#aws-ec2-deployment)
5. [DigitalOcean Deployment](#digitalocean-deployment)
6. [Docker Deployment](#docker-deployment)
7. [Nginx Configuration](#nginx-configuration)

---

## Local Development

### Running in Development Mode
```bash
python app.py
```
The application will be available at `http://localhost:5000`

### Using Flask CLI
```bash
export FLASK_APP=app.py  # Linux/Mac
set FLASK_APP=app.py     # Windows CMD
$env:FLASK_APP="app.py"  # Windows PowerShell

flask run --host=0.0.0.0 --port=5000
```

---

## Production Considerations

### 1. Use a Production WSGI Server

**Install Gunicorn (Linux/Mac)**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Install Waitress (Windows)**
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### 2. Security Checklist
- [ ] Change `SECRET_KEY` in `.env` to a random string
- [ ] Set `DEBUG=False` in production
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Implement authentication if needed
- [ ] Use environment variables for sensitive data
- [ ] Set up proper logging
- [ ] Configure file upload size limits
- [ ] Implement input validation

### 3. Performance Optimization
- Use a CDN for static files
- Enable Gzip compression
- Set up caching headers
- Use a reverse proxy (Nginx)
- Monitor application performance
- Set up background task processing for large files

---

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Create Procfile**
```bash
echo "web: gunicorn app:app" > Procfile
```

2. **Create runtime.txt**
```bash
echo "python-3.11.7" > runtime.txt
```

3. **Login to Heroku**
```bash
heroku login
```

4. **Create Heroku App**
```bash
heroku create your-app-name
```

5. **Set Environment Variables**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
```

6. **Deploy**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

7. **Open App**
```bash
heroku open
```

### Heroku Scaling
```bash
# Scale web dynos
heroku ps:scale web=1

# View logs
heroku logs --tail
```

---

## AWS EC2 Deployment

### 1. Launch EC2 Instance
- Choose Ubuntu Server 22.04 LTS
- Select instance type (t2.micro for free tier)
- Configure security group (allow HTTP/HTTPS)
- Create and download key pair

### 2. Connect to Instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### 3. Install Dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

### 4. Setup Application
```bash
# Clone repository
git clone https://github.com/kRaghuram5/Python_Toolkit.git
cd Python_Toolkit

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

### 5. Create Systemd Service
```bash
sudo nano /etc/systemd/system/pdftoolkit.service
```

Add:
```ini
[Unit]
Description=PDF Toolkit Web Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Python_Toolkit
Environment="PATH=/home/ubuntu/Python_Toolkit/venv/bin"
ExecStart=/home/ubuntu/Python_Toolkit/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

### 6. Start Service
```bash
sudo systemctl start pdftoolkit
sudo systemctl enable pdftoolkit
sudo systemctl status pdftoolkit
```

### 7. Configure Nginx (see Nginx section below)

---

## DigitalOcean Deployment

### Using App Platform (Easiest)

1. **Connect Repository**
   - Go to DigitalOcean App Platform
   - Click "Create App"
   - Connect your GitHub repository

2. **Configure App**
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn -w 4 -b 0.0.0.0:8080 app:app`
   - Port: 8080

3. **Set Environment Variables**
   - Add `SECRET_KEY`
   - Add `FLASK_ENV=production`

4. **Deploy**
   - Click "Deploy"
   - App will be available at provided URL

### Using Droplet (Manual)
Follow similar steps as AWS EC2 deployment.

---

## Docker Deployment

### 1. Create Dockerfile
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p uploads outputs

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=production
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
    restart: unless-stopped
```

### 3. Build and Run
```bash
# Build image
docker build -t pdf-toolkit .

# Run container
docker run -d -p 5000:5000 --name pdf-toolkit pdf-toolkit

# Or use docker-compose
docker-compose up -d
```

### 4. Docker Commands
```bash
# View logs
docker logs pdf-toolkit

# Stop container
docker stop pdf-toolkit

# Restart container
docker restart pdf-toolkit

# Remove container
docker rm pdf-toolkit
```

---

## Nginx Configuration

### Basic Configuration
Create `/etc/nginx/sites-available/pdftoolkit`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for large file processing
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    location /static {
        alias /home/ubuntu/Python_Toolkit/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/pdftoolkit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## Environment Variables for Production

Create `.env` file:
```env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=generate-a-random-secret-key-here
DEBUG=False
HOST=0.0.0.0
PORT=5000
MAX_CONTENT_LENGTH=52428800
```

Generate secret key:
```python
import secrets
print(secrets.token_hex(32))
```

---

## Monitoring and Maintenance

### 1. Log Rotation
Create `/etc/logrotate.d/pdftoolkit`:
```
/home/ubuntu/Python_Toolkit/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 ubuntu ubuntu
}
```

### 2. Monitoring Tools
- **Uptime monitoring**: UptimeRobot, Pingdom
- **Application monitoring**: Sentry, New Relic
- **Server monitoring**: Datadog, Prometheus

### 3. Backup Strategy
- Backup uploaded files regularly
- Database backups (if using database)
- Configuration backups

---

## Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

**Issue: Permission Denied for uploads/outputs**
```bash
chmod 755 uploads outputs
```

**Issue: Port already in use**
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Issue: Large files timing out**
- Increase `MAX_CONTENT_LENGTH` in `.env`
- Increase nginx timeout settings
- Increase gunicorn timeout: `gunicorn -w 4 -b 0.0.0.0:5000 --timeout 300 app:app`

---

## Performance Tuning

### Gunicorn Workers
```bash
# Formula: (2 x CPU cores) + 1
gunicorn -w 9 -b 0.0.0.0:5000 app:app
```

### Redis for Caching (Optional)
```bash
pip install redis flask-caching
```

Add to `app.py`:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

---

## Support

For deployment issues, please open an issue on GitHub:
https://github.com/kRaghuram5/Python_Toolkit/issues
