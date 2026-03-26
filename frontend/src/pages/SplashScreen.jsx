import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SplashScreen.css';

export default function SplashScreen() {
  const navigate = useNavigate();
  const [progress, setProgress] = useState(0);
  const [phase, setPhase] = useState(0);
  const [canSkip, setCanSkip] = useState(false);

  // Allow skipping after 3 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      setCanSkip(true);
    }, 3000);
    return () => clearTimeout(timer);
  }, []);

  // Auto-navigate to language selection after 10 seconds
  // STRICT: Users ALWAYS see language selection, even returning users
  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/language', { replace: true });
    }, 10000);
    return () => clearTimeout(timer);
  }, [navigate]);

  // Progress bar animation
  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 1;
      });
    }, 100);
    return () => clearInterval(interval);
  }, []);

  // Phase animation timeline
  useEffect(() => {
    const t1 = setTimeout(() => setPhase(1), 2000);
    const t2 = setTimeout(() => setPhase(2), 5000);
    const t3 = setTimeout(() => setPhase(3), 8000);
    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
    };
  }, []);

  const handleSkip = () => {
    navigate('/language', { replace: true });
  };

  return (
    <div className="splash-container">
      <div className="splash-bg" />
      <div className="splash-glow splash-glow-1" />
      <div className="splash-glow splash-glow-2" />

      {/* Logo - Phase 0 (Center, Prominent) */}
      <div className={`splash-logo ${phase >= 0 ? 'fade-in' : ''}`}>
        <img
          src="/mahilalogo.jpeg"
          alt="Mahila Udyam Logo"
          className="splash-logo-img"
        />
      </div>

      {/* Text - Phase 2 */}
      {phase >= 2 && (
        <div className="splash-text slide-up">
          <h1 className="splash-appname">MAHILA UDYAM</h1>
          <p className="splash-tagline">Speak. Learn. Earn.</p>
          <p className="splash-subtitle">
            AI Business Assistant for Women Entrepreneurs
          </p>
        </div>
      )}

      {/* Progress Bar */}
      <div className="splash-bottom">
        <div className="splash-progress-track">
          <div
            className="splash-progress-bar"
            style={{ width: `${progress}%` }}
          />
        </div>
        <p className="splash-progress-text">
          {progress < 100 ? 'Loading...' : 'Ready!'}
        </p>
        
        {/* Skip Button - visible after 3 seconds */}
        {canSkip && (
          <button 
            onClick={handleSkip} 
            className="splash-skip-btn"
            style={{
              marginTop: '16px',
              padding: '10px 24px',
              background: 'rgba(255,255,255,0.2)',
              border: '1px solid rgba(255,255,255,0.4)',
              color: '#fff',
              borderRadius: '24px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '600',
              fontFamily: 'inherit',
              backdropFilter: 'blur(10px)',
              transition: 'all 0.3s ease',
            }}
            onMouseEnter={(e) => {
              e.target.style.background = 'rgba(255,255,255,0.3)';
              e.target.style.borderColor = 'rgba(255,255,255,0.6)';
            }}
            onMouseLeave={(e) => {
              e.target.style.background = 'rgba(255,255,255,0.2)';
              e.target.style.borderColor = 'rgba(255,255,255,0.4)';
            }}
          >
            Skip →
          </button>
        )}
      </div>
    </div>
  );
}
