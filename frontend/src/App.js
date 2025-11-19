import React, { useState, useEffect } from 'react';
import './App.css';
import InputSection from './components/InputSection';
import MediaDisplay from './components/MediaDisplay';
import Header from './components/Header';
import Footer from './components/Footer';
import { Instagram, Facebook } from 'lucide-react';

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    // Check localStorage for saved theme preference
    const saved = localStorage.getItem('darkMode');
    return saved ? JSON.parse(saved) : false;
  });
  const [mediaData, setMediaData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);

  // Apply dark mode theme
  useEffect(() => {
    const root = document.documentElement;
    if (darkMode) {
      root.setAttribute('data-theme', 'dark');
    } else {
      root.removeAttribute('data-theme');
    }
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const handleUrlSubmit = async (url) => {
    setError(null);
    setMediaData(null);
    setProgress(0);
    setLoading(true);

    try {
      // Step 1: Validate URL
      setProgress(20);
      const apiUrl = process.env.REACT_APP_API_URL || '';
      const validateResponse = await fetch(`${apiUrl}/api/validate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      const validateData = await validateResponse.json();

      if (!validateData.valid) {
        throw new Error(validateData.error || 'Invalid URL');
      }

      // Step 2: Fetch media
      setProgress(50);
      const fetchResponse = await fetch(`${apiUrl}/api/fetch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: validateData.url }),
      });

      const fetchData = await fetchResponse.json();

      if (!fetchData.success) {
        throw new Error(fetchData.error || 'Failed to fetch media');
      }

      setProgress(100);
      setMediaData({
        mediaUrl: fetchData.media_url,
        mediaType: fetchData.media_type,
        source: fetchData.source,
        originalUrl: url,
      });
    } catch (err) {
      setError(err.message || 'An error occurred. Please try again.');
      setProgress(0);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!mediaData) return;

    try {
      const apiUrl = process.env.REACT_APP_API_URL || '';
      const response = await fetch(`${apiUrl}/api/download`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          media_url: mediaData.mediaUrl,
          media_type: mediaData.mediaType,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Download failed');
      }

      // Get filename from response or create one
      const contentType = response.headers.get('content-type');
      const extension = mediaData.mediaType === 'video' ? 'mp4' : 'jpg';
      const filename = `download_${Date.now()}.${extension}`;

      // Create blob and download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err.message || 'Download failed. Please try again.');
    }
  };

  const handleReset = () => {
    setMediaData(null);
    setError(null);
    setProgress(0);
  };

  return (
    <div className="app">
      <Header darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      
      <main className="main-content">
        <div className="container">
          <div className="hero-section">
            <h1 className="hero-title">
              <Instagram className="icon-instagram" />
              <Facebook className="icon-facebook" />
              Media Downloader
            </h1>
            <p className="hero-subtitle">
              Download videos and images from Instagram and Facebook posts instantly
            </p>
          </div>

          <InputSection
            onSubmit={handleUrlSubmit}
            loading={loading}
            error={error}
            progress={progress}
            onReset={handleReset}
            hasMedia={!!mediaData}
          />

          {mediaData && (
            <MediaDisplay
              mediaData={mediaData}
              onDownload={handleDownload}
              onReset={handleReset}
            />
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;

