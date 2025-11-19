import React, { useState } from 'react';
import './InputSection.css';
import { Link, Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';

function InputSection({ onSubmit, loading, error, progress, onReset, hasMedia }) {
  const [url, setUrl] = useState('');
  const [localError, setLocalError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setLocalError('');

    if (!url.trim()) {
      setLocalError('Please enter a URL');
      return;
    }

    // Basic URL validation
    try {
      new URL(url);
    } catch {
      setLocalError('Please enter a valid URL');
      return;
    }

    onSubmit(url);
  };

  const handleReset = () => {
    setUrl('');
    setLocalError('');
    onReset();
  };

  const displayError = error || localError;

  return (
    <div className="input-section">
      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-wrapper">
          <div className="input-container">
            <Link className="input-icon" />
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste Instagram or Facebook post URL here..."
              className="url-input"
              disabled={loading}
              aria-label="Post URL"
            />
            {url && !loading && (
              <button
                type="button"
                onClick={handleReset}
                className="clear-button"
                aria-label="Clear input"
              >
                ×
              </button>
            )}
          </div>
          <button
            type="submit"
            className="submit-button"
            disabled={loading || !url.trim()}
          >
            {loading ? (
              <>
                <Loader2 className="button-icon spinning" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <span>Download</span>
              </>
            )}
          </button>
        </div>

        {displayError && (
          <div className="error-message" role="alert">
            <AlertCircle className="error-icon" />
            <span>{displayError}</span>
          </div>
        )}

        {loading && progress > 0 && (
          <div className="progress-container">
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${progress}%` }}
              />
            </div>
            <span className="progress-text">{progress}%</span>
          </div>
        )}

        {!loading && !displayError && hasMedia && (
          <div className="success-message">
            <CheckCircle2 className="success-icon" />
            <span>Media loaded successfully!</span>
          </div>
        )}
      </form>

      <div className="instructions">
        <h3 className="instructions-title">How to use:</h3>
        <ol className="instructions-list">
          <li>Copy the URL of an Instagram or Facebook post</li>
          <li>Paste it in the input field above</li>
          <li>Click "Download" to fetch the media</li>
          <li>Click the download button to save the file</li>
        </ol>
      </div>
    </div>
  );
}

export default InputSection;

