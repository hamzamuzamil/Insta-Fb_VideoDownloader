import React from 'react';
import './Header.css';
import { Moon, Sun } from 'lucide-react';

function Header({ darkMode, toggleDarkMode }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-logo">
          <span className="logo-text">Media Downloader</span>
        </div>
        <button
          className="theme-toggle"
          onClick={toggleDarkMode}
          aria-label="Toggle dark mode"
          title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {darkMode ? (
            <Sun className="theme-icon" />
          ) : (
            <Moon className="theme-icon" />
          )}
        </button>
      </div>
    </header>
  );
}

export default Header;

