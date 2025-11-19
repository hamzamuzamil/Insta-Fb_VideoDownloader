import React, { useState } from 'react';
import './MediaDisplay.css';
import { Download, X, Instagram, Facebook, Video, Image as ImageIcon } from 'lucide-react';

function MediaDisplay({ mediaData, onDownload, onReset }) {
  const [imageError, setImageError] = useState(false);

  const handleImageError = () => {
    setImageError(true);
  };

  const getSourceIcon = () => {
    return mediaData.source === 'instagram' ? (
      <Instagram className="source-icon" />
    ) : (
      <Facebook className="source-icon" />
    );
  };

  const getMediaIcon = () => {
    return mediaData.mediaType === 'video' ? (
      <Video className="media-type-icon" />
    ) : (
      <ImageIcon className="media-type-icon" />
    );
  };

  return (
    <div className="media-display">
      <div className="media-header">
        <div className="media-info">
          {getSourceIcon()}
          <div className="media-details">
            <span className="media-source">
              {mediaData.source === 'instagram' ? 'Instagram' : 'Facebook'}
            </span>
            <span className="media-type">
              {getMediaIcon()}
              {mediaData.mediaType === 'video' ? 'Video' : 'Image'}
            </span>
          </div>
        </div>
        <button
          className="close-button"
          onClick={onReset}
          aria-label="Close media display"
        >
          <X />
        </button>
      </div>

      <div className="media-content">
        {mediaData.mediaType === 'video' ? (
          <video
            src={mediaData.mediaUrl}
            controls
            className="media-video"
            preload="metadata"
          >
            Your browser does not support the video tag.
          </video>
        ) : (
          <div className="media-image-container">
            {imageError ? (
              <div className="media-error">
                <ImageIcon className="error-placeholder-icon" />
                <p>Failed to load image preview</p>
                <p className="error-hint">You can still download the file</p>
              </div>
            ) : (
              <img
                src={mediaData.mediaUrl}
                alt="Downloaded media"
                className="media-image"
                onError={handleImageError}
              />
            )}
          </div>
        )}
      </div>

      <div className="media-actions">
        <button
          className="download-button"
          onClick={onDownload}
        >
          <Download className="download-icon" />
          <span>Download {mediaData.mediaType === 'video' ? 'Video' : 'Image'}</span>
        </button>
      </div>

      <div className="media-footer">
        <a
          href={mediaData.originalUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="original-link"
        >
          View original post
        </a>
      </div>
    </div>
  );
}

export default MediaDisplay;

