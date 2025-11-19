import React from 'react';
import './Footer.css';
import { Github, Mail, Linkedin, Code } from 'lucide-react';

function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <div className="footer-brand">
            <Code className="footer-icon" />
            <span className="footer-brand-text">Media Downloader</span>
          </div>
          <p className="footer-description">
            Download videos and images from Instagram and Facebook posts instantly. 
            Free, fast, and secure.
          </p>
        </div>

        <div className="footer-section">
          <h3 className="footer-heading">Features</h3>
          <ul className="footer-links">
            <li>Instagram Posts</li>
            <li>Instagram Reels</li>
            <li>Facebook Videos</li>
            <li>High Quality Downloads</li>
          </ul>
        </div>

        <div className="footer-section">
          <h3 className="footer-heading">Connect</h3>
          <div className="footer-social">
            <a 
              href="https://github.com/hamzamuzamil" 
              target="_blank" 
              rel="noopener noreferrer"
              className="social-link"
              aria-label="GitHub"
              title="GitHub"
            >
              <Github className="social-icon" />
            </a>
            <a 
              href="mailto:hamzamuzamil21@gmail.com"
              className="social-link"
              aria-label="Email"
              title="Email"
            >
              <Mail className="social-icon" />
            </a>
            <a 
              href="https://www.linkedin.com/in/muhammad-hamza-bhutta/"
              target="_blank"
              rel="noopener noreferrer"
              className="social-link"
              aria-label="LinkedIn"
              title="LinkedIn"
            >
              <Linkedin className="social-icon" />
            </a>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="footer-bottom-content">
          <p className="footer-copyright">
            Built by <span className="author-name">Hamza</span> • © {currentYear}
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;

