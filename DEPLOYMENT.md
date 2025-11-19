# Deployment Guide

## 🚀 Production Deployment Checklist

### Pre-Deployment

- [x] Security headers added
- [x] Rate limiting implemented
- [x] Environment variables configured
- [x] Dependencies updated
- [x] Error handling improved
- [x] Logging configured
- [x] Docker configuration added

### Environment Variables

#### Backend (Railway/Render/Heroku)

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=generate-a-strong-secret-key-here
ALLOWED_ORIGINS=https://your-frontend-domain.com
PORT=5000
```

**Generate SECRET_KEY:**
```python
import secrets
print(secrets.token_hex(32))
```

#### Frontend (Vercel/Netlify)

```env
REACT_APP_API_URL=https://your-backend-domain.com
```

### Deployment Steps

#### Option 1: Separate Deployments (Recommended)

**Backend (Railway/Render):**
1. Connect your GitHub repository
2. Set root directory to `backend/`
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn --config gunicorn_config.py wsgi:app`
5. Add all environment variables

**Frontend (Vercel/Netlify):**
1. Connect your GitHub repository
2. Set root directory to `frontend/`
3. Set build command: `npm install && npm run build`
4. Set publish directory: `build`
5. Add `REACT_APP_API_URL` environment variable

#### Option 2: Docker Deployment

```bash
# Build
docker build -t media-downloader .

# Run
docker run -d \
  -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e ALLOWED_ORIGINS=https://your-domain.com \
  media-downloader
```

#### Option 3: Docker Compose

```bash
docker-compose up -d
```

### Security Hardening

1. **Change SECRET_KEY** - Never use default
2. **Restrict CORS** - Set ALLOWED_ORIGINS to your domain only
3. **Enable HTTPS** - Use SSL certificates
4. **Set up Firewall** - Restrict access to necessary ports
5. **Monitor Logs** - Set up logging and monitoring
6. **Regular Updates** - Keep dependencies updated

### Post-Deployment

1. Test all endpoints
2. Verify rate limiting works
3. Check security headers
4. Test CORS restrictions
5. Monitor error logs
6. Set up uptime monitoring

### Troubleshooting

**Backend not starting:**
- Check environment variables
- Verify gunicorn is installed
- Check port availability

**CORS errors:**
- Verify ALLOWED_ORIGINS includes your frontend domain
- Check for trailing slashes in URLs

**Rate limiting issues:**
- Adjust limits in `app.py` if needed
- Check if using Redis for distributed rate limiting

### Performance Tips

- Use Redis for rate limiting in production
- Enable CDN for frontend assets
- Set up caching for static files
- Use load balancer for high traffic
- Monitor and optimize database queries (if added)

