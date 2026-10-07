import { useState, useRef } from 'react'
import './index.css'

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setLoading(true);
    setResult(null);
    
    // Create FormData
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      // Assuming FastAPI runs on 8000
      const response = await fetch('http://localhost:8000/api/generate-recap', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error generating recap:', error);
      alert('Failed to generate recap. Make sure the backend is running!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <h1>Course Recap Generator</h1>
      
      <div className="glass-container">
        {!loading && !result && (
          <>
            <div 
              className="upload-zone"
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current.click()}
            >
              <h3>{file ? file.name : "Drag & Drop your PDF here"}</h3>
              <p>or click to browse files</p>
              <input 
                type="file" 
                ref={fileInputRef} 
                style={{ display: 'none' }} 
                accept=".pdf,.doc,.docx"
                onChange={handleFileSelect}
              />
            </div>
            <button 
              onClick={handleUpload} 
              disabled={!file}
            >
              Generate Recap & Diagram
            </button>
          </>
        )}

        {loading && (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div className="loader"></div>
            <p style={{ marginTop: '1rem' }}>Agents are processing your document...</p>
          </div>
        )}

        {result && (
          <div className="dashboard">
            <div className="glass-container" style={{ margin: 0 }}>
              <div className="markdown-body">
                {/* Simple render of markdown for prototype */}
                <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                  {result.markdown_summary}
                </pre>
              </div>
            </div>
            
            {result.image_url && (
              <div className="glass-container" style={{ margin: 0, textAlign: 'center' }}>
                <h3>Generated Canva Diagram</h3>
                <a href={result.image_url} target="_blank" rel="noreferrer" style={{ color: '#8b5cf6' }}>
                  Open Diagram in Canva
                </a>
              </div>
            )}
            
            <button onClick={() => { setFile(null); setResult(null); }}>Start Over</button>
          </div>
        )}
      </div>
    </>
  )
}

export default App
