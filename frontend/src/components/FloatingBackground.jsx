import React from 'react';
import { DollarSign, TrendingUp, BarChart3 } from 'lucide-react';

export default function FloatingBackground() {
  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      pointerEvents: 'none',
      zIndex: 0,
      overflow: 'hidden'
    }}>
      {/* Floating Gradient Blobs */}
      <div
        style={{
          position: 'absolute',
          top: '10%',
          left: '10%',
          width: '300px',
          height: '300px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)',
          opacity: 0.08,
          filter: 'blur(60px)',
          animation: 'blobMove 15s ease-in-out infinite'
        }}
      />
      <div
        style={{
          position: 'absolute',
          top: '50%',
          right: '5%',
          width: '250px',
          height: '250px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #22C55E 0%, #16A34A 100%)',
          opacity: 0.08,
          filter: 'blur(60px)',
          animation: 'blobMove 20s ease-in-out infinite 2s'
        }}
      />
      <div
        style={{
          position: 'absolute',
          bottom: '10%',
          left: '50%',
          width: '280px',
          height: '280px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
          opacity: 0.08,
          filter: 'blur(60px)',
          animation: 'blobMove 18s ease-in-out infinite 1s'
        }}
      />

      {/* Floating Icons */}
      <div
        style={{
          position: 'absolute',
          top: '20%',
          right: '15%',
          opacity: 0.1,
          animation: 'floating 6s ease-in-out infinite'
        }}
      >
        <DollarSign size={80} style={{ color: '#6366F1' }} />
      </div>
      <div
        style={{
          position: 'absolute',
          top: '60%',
          left: '5%',
          opacity: 0.1,
          animation: 'floating 5s ease-in-out infinite 1s'
        }}
      >
        <TrendingUp size={80} style={{ color: '#22C55E' }} />
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: '20%',
          right: '10%',
          opacity: 0.1,
          animation: 'floating 7s ease-in-out infinite 0.5s'
        }}
      >
        <BarChart3 size={80} style={{ color: '#F59E0B' }} />
      </div>

      {/* Grid Background Pattern */}
      <svg
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          opacity: 0.05,
          pointerEvents: 'none'
        }}
      >
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#6366F1" strokeWidth="0.5" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>
    </div>
  );
}
