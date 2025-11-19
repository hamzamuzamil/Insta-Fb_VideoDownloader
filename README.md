# Instagram & Facebook Media Downloader

A modern, full-stack web application for downloading videos and images from Instagram and Facebook posts. Built with React (frontend) and Flask (backend), featuring a beautiful, responsive UI with dark mode support.

## Features

- 🎨 **Modern UI/UX**: Clean, attractive interface with smooth animations
- 📱 **Fully Responsive**: Works flawlessly on desktop and mobile devices
- 🌙 **Dark Mode**: Toggle between light and dark themes
- ✅ **URL Validation**: Smart validation for Instagram and Facebook URLs
- 📊 **Progress Indicators**: Real-time progress feedback during media fetching
- 🎯 **Error Handling**: Graceful error handling with user-friendly messages
- 🔒 **Security**: Input sanitization and secure media fetching
- ⚡ **Performance**: Efficient media processing and download

## Tech Stack

### Frontend
- **React 18** - Modern UI library
- **CSS3** - Custom styling with CSS variables for theming
- **Lucide React** - Beautiful icon library
- **Axios** - HTTP client for API requests

### Backend
- **Python 3.8+** - Programming language
- **Flask** - Lightweight web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Requests** - HTTP library for fetching media

## 🚀 Quick Deploy

### Deploy to Vercel/Netlify (Frontend) + Railway/Render (Backend)

1. **Backend Deployment:**
   ```bash
   # On Railway/Render, set these environment variables:
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=your-secret-key-here
   ALLOWED_ORIGINS=https://your-frontend-domain.com
   PORT=5000
   ```

2. **Frontend Deployment:**
   ```bash
   # Set environment variable:
   REACT_APP_API_URL=https://your-backend-domain.com
   ```

### Deploy with Docker

```bash
# Build and run
docker-compose up -d

# Or build manually
docker build -t media-downloader .
docker run -p 5000:5000 -e SECRET_KEY=your-key media-downloader
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy example file
cp .env.example .env

# Edit .env with your configuration
```

5. Run the Flask server:
```bash
# Development
python app.py

# Production (with gunicorn)
gunicorn --config gunicorn_config.py wsgi:app
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
# Copy example file
cp .env.example .env

# For development, REACT_APP_API_URL can be empty (uses proxy)
# For production, set: REACT_APP_API_URL=https://your-api-domain.com
```

4. Start the development server:
```bash
npm start
```

5. Build for production:
```bash
npm run build
```

The frontend will run on `http://localhost:3000` and automatically proxy API requests to the backend.

## Usage

1. **Start both servers** (backend and frontend)
2. **Open your browser** and navigate to `http://localhost:3000`
3. **Paste a URL** from an Instagram or Facebook post
4. **Click "Download"** to fetch the media
5. **Click the download button** to save the file to your device

### Supported URL Formats

#### Instagram
- `https://www.instagram.com/p/[POST_ID]/`
- `https://www.instagram.com/reel/[REEL_ID]/`
- `https://www.instagram.com/tv/[TV_ID]/`

#### Facebook
- `https://www.facebook.com/[USER]/posts/[POST_ID]`
- `https://www.facebook.com/[USER]/videos/[VIDEO_ID]`
- `https://www.facebook.com/watch?v=[VIDEO_ID]`
- `https://fb.watch/[VIDEO_ID]`

## Project Structure

```
instavideodownloader/
├── backend/
│   ├── app.py              # Flask application and API endpoints
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Header.js
│   │   │   ├── InputSection.js
│   │   │   └── MediaDisplay.js
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Main styles
│   │   ├── index.js        # React entry point
│   │   └── index.css       # Global styles
│   └── package.json        # Node.js dependencies
└── README.md               # This file
```

## API Endpoints

### `POST /api/validate`
Validates a URL and determines the platform.

**Request:**
```json
{
  "url": "https://www.instagram.com/p/ABC123/"
}
```

**Response:**
```json
{
  "valid": true,
  "platform": "instagram",
  "url": "https://www.instagram.com/p/ABC123/"
}
```

### `POST /api/fetch`
Fetches media information from a validated URL.

**Request:**
```json
{
  "url": "https://www.instagram.com/p/ABC123/"
}
```

**Response:**
```json
{
  "success": true,
  "media_url": "https://...",
  "media_type": "video",
  "source": "instagram"
}
```

### `POST /api/download`
Downloads the media file.

**Request:**
```json
{
  "media_url": "https://...",
  "media_type": "video"
}
```

**Response:** Binary file download

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Instagram/Facebook Media Downloader"
}
```

## Important Notes

### Limitations

1. **Instagram & Facebook Anti-Scraping**: Both platforms have strict anti-scraping measures. This implementation uses a simplified approach that may not work for all posts, especially:
   - Private accounts
   - Posts requiring login
   - Posts with additional security measures

2. **Production Considerations**: For production use, consider:
   - Using official APIs (Instagram Graph API, Facebook Graph API)
   - Implementing proper authentication
   - Using specialized libraries like Instaloader (requires login)
   - Adding rate limiting and caching
   - Implementing proper error handling for edge cases

3. **File Size Limits**: The current implementation has a 100MB file size limit. Adjust `MAX_FILE_SIZE` in `backend/app.py` if needed.

## Development

### Running in Development Mode

1. Start the backend:
```bash
cd backend
python app.py
```

2. Start the frontend (in a new terminal):
```bash
cd frontend
npm start
```

### Building for Production

1. Build the React app:
```bash
cd frontend
npm run build
```

2. The built files will be in `frontend/build/`. You can serve them with a static file server or integrate with your Flask backend.

## Security Features

✅ **Production-Ready Security:**
- Input sanitization and validation
- Rate limiting (200/day, 50/hour per IP)
- Security headers (XSS protection, CSRF, etc.)
- CORS configuration with origin restrictions
- File size limits (100MB max)
- Temporary file cleanup
- Environment-based configuration
- Non-root Docker user
- HTTPS ready

## Production Deployment

### Environment Variables

**Backend (.env):**
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://your-frontend-domain.com
PORT=5000
```

**Frontend (.env):**
```env
REACT_APP_API_URL=https://your-backend-domain.com
```

### Deployment Options

1. **Vercel/Netlify (Frontend) + Railway/Render (Backend)**
   - Deploy frontend to Vercel/Netlify
   - Deploy backend to Railway/Render
   - Set environment variables on both platforms

2. **Docker Deployment**
   ```bash
   docker-compose up -d
   ```

3. **Traditional Server**
   - Use gunicorn for backend
   - Serve frontend build with nginx
   - Configure reverse proxy

### Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set ALLOWED_ORIGINS to your domain
- [ ] Enable HTTPS/SSL
- [ ] Set up proper logging
- [ ] Configure firewall rules
- [ ] Set up monitoring
- [ ] Regular dependency updates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is for educational purposes. Please respect the terms of service of Instagram and Facebook. Only download content that you have permission to download, and respect copyright laws.

