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
      
      // Auto-scroll to results after a short delay to allow rendering
      setTimeout(() => {
        document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
      }, 100);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const scrollToDetector = () => {
    document.getElementById('detector-section').scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="App">
      
      {/* Navbar Section */}
      <nav className="navbar">
        <div className="nav-links">
          <a href="#" className="active">Home</a>
          <a href="#detector-section">Detect</a>
          <a href="#features-section">About</a>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <p className="hero-subtitle">Advanced Vision Tech</p>
          <h1 className="hero-title">Enhance Night-Time Media Like Never Before</h1>
          <button className="btn-primary" onClick={scrollToDetector}>
            Try It Now
          </button>
        </div>
      </section>

      {/* Detector Section */}
      <section id="detector-section" className="detector-section">
        <h2 className="section-label">Object Detection Demo</h2>
        <p className="section-desc">
          Upload a dark or night-time image. Our pipeline applies Contrast Limited Adaptive Histogram Equalization (CLAHE) before running Ultralytics YOLOv8.
        </p>

        <div className="upload-area">
          <label htmlFor="fileInput" className="upload-label">
            {file ? file.name : "Click here to select an image file"}
          </label>
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleFileChange} 
            id="fileInput" 
            className="hidden-input"
          />
        </div>
        
        <button 
          className="btn-primary" 
          onClick={handleUpload} 
          disabled={!file || loading}
        >
          {loading ? <span className="spinner"></span> : "Enhance & Detect"}
        </button>
        
        {error && <div className="error-msg">{error}</div>}
      </section>

      {/* Results Section */}
      {results && (
        <section id="results-section" className="results-section">
          <div className="results-header">
            <h2>True to life analysis</h2>
            <p>See the progression from the original dark input, through structural enhancement, to the final AI object detection.</p>
          </div>
          
          <div className="results-grid">
            <div className="result-card">
              <h3>Original Input</h3>
              <div className="img-container">
                <img src={results.original} alt="Original dark input" />
              </div>
            </div>

            <div className="result-card">
              <h3>Structure-Enhanced</h3>
              <div className="img-container">
                <img src={results.enhanced} alt="Enhanced output" />
              </div>
            </div>

            <div className="result-card">
              <h3>YOLOv8 Detection</h3>
              <div className="img-container">
                <img src={results.detected} alt="Detected objects" />
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Features Section */}
      <section id="features-section" className="features-section">
        <div className="features-grid">
          <div className="feature-item">
            <h3>High-Quality Output</h3>
            <p>Our CLAHE enhancement ensures that local contrast is preserved without blowing out already bright areas.</p>
          </div>
          <div className="feature-item">
            <h3>Fast Processing</h3>
            <p>Using classical computer vision to enhance images is significantly faster than relying on massive, heavy AI models.</p>
          </div>
          <div className="feature-item">
            <h3>State of the Art AI</h3>
            <p>Powered by Ultralytics YOLOv8 Nano for incredibly fast, accurate, and lightweight object detection.</p>
          </div>
          <div className="feature-item">
            <h3>Privacy First</h3>
            <p>Your images are processed locally on your server and are temporarily stored solely for demonstrating the pipeline.</p>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <footer className="footer">
        <p>Built with React, Flask, OpenCV, and YOLO. Design inspired by Safalite.</p>
      </footer>

    </div>
  );
}

export default App;
