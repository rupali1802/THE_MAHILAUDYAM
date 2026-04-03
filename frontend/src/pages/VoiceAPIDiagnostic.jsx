import React, { useState } from 'react';
import { predictIntent } from '../services/api';

/**
 * Voice API Diagnostic Component
 * Test the frontend → backend API connection
 * Usage: Add this to your routes and navigate to /diagnostic
 */
export default function VoiceAPIDiagnostic() {
  const [testText, setTestText] = useState('income 500');
  const [language, setLanguage] = useState('en');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState([]);

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = `[${timestamp}] ${type.toUpperCase()}: ${message}`;
    console.log(logEntry);
    setLogs((prev) => [...prev, logEntry]);
  };

  const testAPI = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    setLogs([]);

    addLog('Starting API test...', 'info');
    addLog(`Text: "${testText}"`, 'info');
    addLog(`Language: ${language}`, 'info');
    addLog('Sending request to backend...', 'info');

    try {
      const response = await predictIntent(testText, language);
      
      addLog('✅ API Response received successfully!', 'success');
      addLog(`Status: ${response.status}`, 'success');
      addLog(`Response data: ${JSON.stringify(response.data, null, 2)}`, 'success');
      
      setResult(response.data);
    } catch (err) {
      addLog(`❌ API Error: ${err.message}`, 'error');
      
      if (err.response) {
        addLog(`Status Code: ${err.response.status}`, 'error');
        addLog(`Response: ${JSON.stringify(err.response.data)}`, 'error');
      } else if (err instanceof TypeError) {
        addLog('Network Error - Cannot reach backend', 'error');
        addLog('Possible causes:', 'error');
        addLog('  1. Backend is not running', 'error');
        addLog('  2. Backend URL is incorrect', 'error');
        addLog('  3. CORS is not configured', 'error');
        addLog('  4. Firewall is blocking the connection', 'error');
      }
      
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20, maxWidth: 800, margin: '0 auto', fontFamily: 'monospace' }}>
      <h1>🔍 Voice API Diagnostic</h1>
      
      <div style={{ background: '#f0f0f0', padding: 15, borderRadius: 8, marginBottom: 20 }}>
        <h3>Configuration</h3>
        <p><strong>Frontend URL:</strong> {window.location.origin}</p>
        <p><strong>Backend URL:</strong> {process.env.REACT_APP_API_URL || 'http://localhost:8000/api'}</p>
        <p><strong>Endpoint:</strong> {process.env.REACT_APP_API_URL || 'http://localhost:8000/api'}/predict-intent/</p>
      </div>

      <div style={{ marginBottom: 20 }}>
        <label>
          Test Text:
          <input
            type="text"
            value={testText}
            onChange={(e) => setTestText(e.target.value)}
            style={{ width: '100%', padding: 8, marginTop: 5 }}
            placeholder="e.g., income 500"
          />
        </label>
      </div>

      <div style={{ marginBottom: 20 }}>
        <label>
          Language:
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            style={{ width: '100%', padding: 8, marginTop: 5 }}
          >
            <option value="en">English (en)</option>
            <option value="hi">Hindi (hi)</option>
            <option value="ta">Tamil (ta)</option>
          </select>
        </label>
      </div>

      <button
        onClick={testAPI}
        disabled={loading}
        style={{
          padding: '10px 20px',
          background: loading ? '#ccc' : '#007bff',
          color: '#fff',
          border: 'none',
          borderRadius: 5,
          cursor: loading ? 'not-allowed' : 'pointer',
          fontSize: 14,
          fontWeight: 'bold',
        }}
      >
        {loading ? 'Testing...' : 'Test API'}
      </button>

      {/* Logs */}
      <div
        style={{
          background: '#1e1e1e',
          color: '#00ff00',
          padding: 15,
          borderRadius: 8,
          marginTop: 20,
          maxHeight: 300,
          overflow: 'auto',
          fontSize: 12,
          lineHeight: 1.5,
        }}
      >
        <strong>Logs:</strong>
        <div>
          {logs.length === 0 ? (
            <p style={{ color: '#666' }}>No logs yet. Click "Test API" to start.</p>
          ) : (
            logs.map((log, idx) => (
              <div
                key={idx}
                style={{
                  color: log.includes('SUCCESS') ? '#00ff00' : log.includes('ERROR') ? '#ff0000' : '#00ff00',
                }}
              >
                {log}
              </div>
            ))
          )}
        </div>
      </div>

      {/* Result */}
      {result && (
        <div style={{ background: '#e8f5e9', padding: 15, borderRadius: 8, marginTop: 20 }}>
          <h3>✅ API Response:</h3>
          <pre style={{ background: '#fff', padding: 10, borderRadius: 4, overflow: 'auto' }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}

      {/* Error */}
      {error && (
        <div style={{ background: '#ffebee', padding: 15, borderRadius: 8, marginTop: 20 }}>
          <h3>❌ Error Details:</h3>
          <pre style={{ background: '#fff', padding: 10, borderRadius: 4, overflow: 'auto', color: '#d32f2f' }}>
            {error.message}
            {'\n\n'}
            {error.response ? JSON.stringify(error.response.data, null, 2) : 'Network Error'}
          </pre>
          
          <div style={{ marginTop: 15, fontSize: 14 }}>
            <strong>Troubleshooting:</strong>
            <ul>
              <li>Is the backend running? <code>python manage.py runserver 0.0.0.0:8000</code></li>
              <li>Is port 8000 accessible from your browser?</li>
              <li>Check browser console (F12) for CORS errors</li>
              <li>Check backend terminal for error messages</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
