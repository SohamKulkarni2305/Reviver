import { useState, useRef, useEffect } from 'react'
import mermaid from 'mermaid'
import ReactMarkdown from 'react-markdown'
import './index.css'

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (result?.mermaid_code) {
      mermaid.initialize({ startOnLoad: true, theme: 'dark' });
      // Small timeout to ensure DOM is ready
      setTimeout(() => mermaid.contentLoaded(), 100);
    }
  }, [result]);

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
            {result.image_url && (
              <div className="glass-container" style={{ margin: '0 0 2rem 0', textAlign: 'center', padding: '1rem' }}>
                <h3 style={{ marginBottom: '1rem', color: '#c084fc' }}>Course Visual</h3>
                <img 
                  src={result.image_url} 
                  alt="Generated Course Cover" 
                  style={{ width: '100%', maxHeight: '400px', objectFit: 'cover', borderRadius: '12px' }} 
                />
              </div>
            )}
            
            <div className="glass-container" style={{ margin: '0 0 2rem 0' }}>
              <div className="markdown-body">
                {/* Simple render of markdown for prototype */}
                <ReactMarkdown>
                  {result.markdown_summary}
                </ReactMarkdown>
              </div>
            </div>
            
            {result.mermaid_code && (
              <div className="glass-container" style={{ margin: '0 0 2rem 0', textAlign: 'center' }}>
                <h3 style={{ color: '#60a5fa' }}>Concept Flowchart</h3>
                <div className="mermaid" style={{ marginTop: '1rem', background: 'rgba(255,255,255,0.05)', padding: '2rem', borderRadius: '12px' }}>
                  {result.mermaid_code}
                </div>
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
