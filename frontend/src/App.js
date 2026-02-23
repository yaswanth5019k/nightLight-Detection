import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResults(null);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select an image first.");
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5001/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process image.");
      }

      const data = await response.json();
      setResults({
        original: `http://localhost:5001${data.original_url}`,
        enhanced: `http://localhost:5001${data.enhanced_url}`,
        detected: `http://localhost:5001${data.detected_url}`
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App dark-theme">
      <header className="header">
        <h1>NightVision AI</h1>
        <p>Low-Light & Night-Time Object Detection</p>
      </header>

      <main className="main-content">
        <section className="upload-section glass-panel">
          <div className="upload-area">
            <input 
              type="file" 
              accept="image/*" 
              onChange={handleFileChange} 
              id="fileInput" 
              className="hidden-input"
            />
            <label htmlFor="fileInput" className="upload-label">
              {file ? file.name : "Click or Drag to Upload Image"}
            </label>
          </div>
          
          <button 
            className="magic-btn" 
            onClick={handleUpload} 
            disabled={!file || loading}
          >
            {loading ? <span className="spinner"></span> : "Enhance & Detect"}
          </button>
          
          {error && <div className="error-msg">{error}</div>}
        </section>

        {results && (
          <section className="results-section">
            <h2 className="section-title">Analysis Results</h2>
            <div className="results-grid">
              
              <div className="result-card glass-panel">
                <h3>1. Original Input</h3>
                <div className="img-container">
                  <img src={results.original} alt="Original dark input" />
                </div>
              </div>

              <div className="result-card glass-panel accent-border">
                <h3>2. Structure-Enhanced (CLAHE)</h3>
                <div className="img-container">
                  <img src={results.enhanced} alt="Enhanced output" />
                </div>
              </div>

              <div className="result-card glass-panel highlight-border">
                <h3>3. Object Detection (YOLOv8)</h3>
                <div className="img-container">
                  <img src={results.detected} alt="Detected objects" />
                </div>
              </div>

            </div>
          </section>
        )}
      </main>
      
      <footer>
        <p>Powered by OpenCV & Ultralytics YOLOv8</p>
      </footer>
    </div>
  );
}

export default App;
