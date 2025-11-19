"""
Instagram and Facebook Media Downloader - Backend API
Handles URL validation, media fetching, and download operations
"""

from flask import Flask, request, jsonify, send_file, after_this_request, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import re
import requests
import json
from urllib.parse import urlparse, parse_qs
import tempfile
import mimetypes
from werkzeug.utils import secure_filename
import logging
import yt_dlp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.getenv('FLASK_ENV') != 'production' else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app with static folder for React build
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
# Create static folder if it doesn't exist
if not os.path.exists(static_folder):
    os.makedirs(static_folder, exist_ok=True)
app = Flask(__name__, static_folder=static_folder, static_url_path='')

# Security configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(32).hex())
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

# CORS configuration - restrict in production
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*').split(',')
CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Configuration
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB max file size
TEMP_DIR = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'mp4', 'jpg', 'jpeg', 'png', 'webp', 'gif'}

# User-Agent header to mimic browser requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0'
}


def validate_instagram_url(url):
    """Validate Instagram post URL format - supports posts, reels, stories, etc."""
    patterns = [
        r'https?://(www\.)?instagram\.com/(p|reel|tv)/([A-Za-z0-9_-]+)',
        r'https?://(www\.)?instagram\.com/([A-Za-z0-9_.]+)/(p|reel|tv)/([A-Za-z0-9_-]+)',
        r'https?://(www\.)?instagram\.com/(p|reel|tv)/([A-Za-z0-9_-]+)/?',
        r'https?://(www\.)?instagram\.com/(p|reel|tv)/([A-Za-z0-9_-]+)\?.*',
    ]
    for pattern in patterns:
        if re.search(pattern, url):
            return True
    return False


def validate_facebook_url(url):
    """Validate Facebook post URL format"""
    patterns = [
        r'https?://(www\.)?facebook\.com/.+/posts/[0-9]+',
        r'https?://(www\.)?facebook\.com/.+/videos/[0-9]+',
        r'https?://(www\.)?facebook\.com/watch/\?v=[0-9]+',
        r'https?://(www\.)?fb\.watch/[A-Za-z0-9_-]+',
    ]
    for pattern in patterns:
        if re.match(pattern, url):
            return True
    return False


def sanitize_url(url):
    """Sanitize and validate URL input"""
    if not url or not isinstance(url, str):
        return None
    
    url = url.strip()
    
    # Basic URL format validation
    if not url.startswith(('http://', 'https://')):
        return None
    
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return None
        return url
    except Exception:
        return None


def fetch_instagram_media(url):
    """
    Fetch media from Instagram URL using yt-dlp (professional method)
    This is the most reliable way to extract Instagram media
    """
    try:
        # Clean URL - remove query parameters
        clean_url = url.split('?')[0] if '?' in url else url
        
        # Use yt-dlp to extract media information
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'no_check_certificate': True,
            'ignoreerrors': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(clean_url, download=False)
                
                if not info:
                    raise Exception("No media information found")
                
                # Get the best quality video or image
                media_url = None
                media_type = None
                
                # Check if it's a video
                if info.get('url') and ('video' in info.get('format', '').lower() or 
                                       info.get('ext') in ['mp4', 'webm', 'mkv']):
                    media_url = info.get('url')
                    media_type = 'video'
                # Check for video formats
                elif 'formats' in info:
                    # Find the best video format
                    video_formats = [f for f in info['formats'] if f.get('vcodec') != 'none']
                    if video_formats:
                        # Get the best quality video
                        best_video = max(video_formats, key=lambda x: x.get('height', 0) or x.get('width', 0))
                        media_url = best_video.get('url')
                        media_type = 'video'
                    else:
                        # No video, try image
                        image_formats = [f for f in info['formats'] if f.get('vcodec') == 'none']
                        if image_formats:
                            best_image = image_formats[0]
                            media_url = best_image.get('url')
                            media_type = 'image'
                
                # Fallback: use thumbnail or direct URL
                if not media_url:
                    if info.get('thumbnail'):
                        media_url = info['thumbnail']
                        media_type = 'image'
                    elif info.get('url'):
                        media_url = info['url']
                        # Determine type from extension or format
                        if info.get('ext') in ['mp4', 'webm', 'mkv'] or 'video' in str(info.get('format', '')).lower():
                            media_type = 'video'
                        else:
                            media_type = 'image'
                
                if not media_url:
                    raise Exception("Could not extract media URL from Instagram post")
                
                return {
                    'media_url': media_url,
                    'media_type': media_type,
                    'source': 'instagram'
                }
                
            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e)
                if 'Private' in error_msg or 'private' in error_msg:
                    raise Exception("This post is private or requires login")
                elif 'Not Found' in error_msg or 'not found' in error_msg:
                    raise Exception("Post not found. It may have been deleted.")
                else:
                    raise Exception(f"Failed to extract media: {error_msg}")
            except Exception as e:
                logger.error(f"yt-dlp extraction error: {str(e)}")
                raise Exception(f"Failed to extract media: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error fetching Instagram media: {str(e)}")
        raise Exception(f"Failed to extract media from Instagram post: {str(e)}")


def fetch_facebook_media(url):
    """
    Fetch media from Facebook URL using yt-dlp (professional method)
    This is the most reliable way to extract Facebook media
    """
    try:
        # Clean URL
        clean_url = url.split('?')[0] if '?' in url else url
        
        # Use yt-dlp to extract media information
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'no_check_certificate': True,
            'ignoreerrors': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(clean_url, download=False)
                
                if not info:
                    raise Exception("No media information found")
                
                # Get the best quality video or image
                media_url = None
                media_type = None
                
                # Check if it's a video
                if info.get('url') and ('video' in info.get('format', '').lower() or 
                                       info.get('ext') in ['mp4', 'webm', 'mkv']):
                    media_url = info.get('url')
                    media_type = 'video'
                # Check for video formats
                elif 'formats' in info:
                    # Find the best video format
                    video_formats = [f for f in info['formats'] if f.get('vcodec') != 'none']
                    if video_formats:
                        # Get the best quality video
                        best_video = max(video_formats, key=lambda x: x.get('height', 0) or x.get('width', 0))
                        media_url = best_video.get('url')
                        media_type = 'video'
                    else:
                        # No video, try image
                        image_formats = [f for f in info['formats'] if f.get('vcodec') == 'none']
                        if image_formats:
                            best_image = image_formats[0]
                            media_url = best_image.get('url')
                            media_type = 'image'
                
                # Fallback: use thumbnail or direct URL
                if not media_url:
                    if info.get('thumbnail'):
                        media_url = info['thumbnail']
                        media_type = 'image'
                    elif info.get('url'):
                        media_url = info['url']
                        # Determine type from extension or format
                        if info.get('ext') in ['mp4', 'webm', 'mkv'] or 'video' in str(info.get('format', '')).lower():
                            media_type = 'video'
                        else:
                            media_type = 'image'
                
                if not media_url:
                    raise Exception("Could not extract media URL from Facebook post")
                
                return {
                    'media_url': media_url,
                    'media_type': media_type,
                    'source': 'facebook'
                }
                
            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e)
                if 'Private' in error_msg or 'private' in error_msg:
                    raise Exception("This post is private or requires login")
                elif 'Not Found' in error_msg or 'not found' in error_msg:
                    raise Exception("Post not found. It may have been deleted.")
                else:
                    raise Exception(f"Failed to extract media: {error_msg}")
            except Exception as e:
                logger.error(f"yt-dlp extraction error: {str(e)}")
                raise Exception(f"Failed to extract media: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error fetching Facebook media: {str(e)}")
        raise Exception(f"Failed to extract media from Facebook post: {str(e)}")


def download_media(media_url, media_type):
    """Download media file from URL and save to temporary location"""
    try:
        response = requests.get(media_url, headers=HEADERS, stream=True, timeout=60)
        response.raise_for_status()
        
        # Determine file extension
        content_type = response.headers.get('content-type', '')
        if 'video' in content_type or media_type == 'video':
            ext = 'mp4'
        elif 'image' in content_type or media_type == 'image':
            ext = 'jpg'
        else:
            ext = mimetypes.guess_extension(content_type) or 'bin'
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}')
        
        # Download with size limit
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                downloaded += len(chunk)
                if downloaded > MAX_FILE_SIZE:
                    os.unlink(temp_file.name)
                    raise Exception("File size exceeds maximum allowed size")
                temp_file.write(chunk)
        
        temp_file.close()
        return temp_file.name
        
    except requests.RequestException as e:
        logger.error(f"Error downloading media: {str(e)}")
        raise Exception(f"Failed to download media: {str(e)}")
    except Exception as e:
        logger.error(f"Error saving media: {str(e)}")
        raise Exception(f"Failed to save media: {str(e)}")


@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


@app.route('/api/validate', methods=['POST'])
@limiter.limit("10 per minute")
def validate_url():
    """Validate URL format and determine platform"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'valid': False,
                'error': 'URL is required'
            }), 400
        
        sanitized_url = sanitize_url(url)
        if not sanitized_url:
            return jsonify({
                'valid': False,
                'error': 'Invalid URL format'
            }), 400
        
        platform = None
        if validate_instagram_url(sanitized_url):
            platform = 'instagram'
        elif validate_facebook_url(sanitized_url):
            platform = 'facebook'
        else:
            return jsonify({
                'valid': False,
                'error': 'Unsupported URL. Please provide an Instagram or Facebook post URL.'
            }), 400
        
        return jsonify({
            'valid': True,
            'platform': platform,
            'url': sanitized_url
        })
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({
            'valid': False,
            'error': 'An error occurred during validation'
        }), 500


@app.route('/api/fetch', methods=['POST'])
@limiter.limit("20 per hour")
def fetch_media():
    """Fetch media information from URL"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        sanitized_url = sanitize_url(url)
        if not sanitized_url:
            return jsonify({
                'success': False,
                'error': 'Invalid URL format'
            }), 400
        
        # Determine platform and fetch media
        if validate_instagram_url(sanitized_url):
            media_info = fetch_instagram_media(sanitized_url)
        elif validate_facebook_url(sanitized_url):
            media_info = fetch_facebook_media(sanitized_url)
        else:
            return jsonify({
                'success': False,
                'error': 'Unsupported URL. Please provide an Instagram or Facebook post URL.'
            }), 400
        
        return jsonify({
            'success': True,
            'media_url': media_info['media_url'],
            'media_type': media_info['media_type'],
            'source': media_info['source']
        })
        
    except Exception as e:
        logger.error(f"Fetch error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download', methods=['POST'])
@limiter.limit("10 per hour")
def download():
    """Download media file and return it"""
    temp_file_path = None
    try:
        data = request.get_json()
        media_url = data.get('media_url')
        media_type = data.get('media_type', 'image')
        
        if not media_url:
            return jsonify({
                'success': False,
                'error': 'Media URL is required'
            }), 400
        
        # Download media to temporary file
        temp_file_path = download_media(media_url, media_type)
        
        # Determine filename
        filename = f"download.{'mp4' if media_type == 'video' else 'jpg'}"
        
        # Clean up temp file after response is sent
        @after_this_request
        def cleanup(response):
            try:
                if temp_file_path and os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
            except Exception as e:
                logger.error(f"Error cleaning up temp file: {str(e)}")
            return response
        
        return send_file(
            temp_file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        # Clean up on error
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass
        logger.error(f"Download error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Instagram/Facebook Media Downloader'
    })


# Serve React app for all non-API routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    """Serve React app for all non-API routes - optimized for performance"""
    # Don't serve React app for API routes
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    
    # Check if static folder exists
    if not app.static_folder or not os.path.exists(app.static_folder):
        return jsonify({'error': 'Frontend not built. Please rebuild the application.'}), 503
    
    # Handle static assets (JS, CSS, images, etc.)
    if path and '.' in path:
        # It's a file request (has extension)
        file_path = os.path.join(app.static_folder, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_from_directory(app.static_folder, path)
    
    # For all other routes, serve index.html (React Router handles routing)
    index_path = os.path.join(app.static_folder, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(app.static_folder, 'index.html')
    else:
        return jsonify({
            'error': 'Frontend not found',
            'message': 'Please ensure the React app is built and copied to the static folder'
        }), 503


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Create temp directory if it doesn't exist
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Get configuration from environment
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    # Run Flask app
    app.run(debug=debug_mode, host=host, port=port)

