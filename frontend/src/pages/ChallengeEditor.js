import React, { useState, useEffect } from 'react';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-monokai';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import '../styles/ChallengeEditor.css';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function ChallengeEditor({ user, token }) {
  const { day } = useParams();
  const [challenge, setChallenge] = useState(null);
  const [code, setCode] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const fetchChallenge = async () => {
    try {
      const response = await axios.get(`${API_URL}/challenges/${day}`);
      setChallenge(response.data);
      setCode(response.data.starter_code);
    } catch (error) {
      console.error('Error fetching challenge:', error);
    }
  };

  useEffect(() => {
    fetchChallenge();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [day]);

  const handleSubmit = async () => {
    if (!user || !token) {
      alert('Please log in first');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${API_URL}/submissions/`,
        {
          day: parseInt(day),
          code: code
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      setResults(response.data);
      setSubmitted(true);
    } catch (error) {
      console.error('Error submitting:', error);
      setResults({
        passed: false,
        results: { error: error.response?.data?.error || 'Submission failed' }
      });
    } finally {
      setLoading(false);
    }
  };

  if (!challenge) return <div>Loading...</div>;

  return (
    <div className="challenge-editor">
      <div className="challenge-panel">
        <h1>Day {challenge.day}: {challenge.title}</h1>
        <div className="difficulty">
          {'★'.repeat(challenge.difficulty)}{'☆'.repeat(5 - challenge.difficulty)}
        </div>
        {challenge.tags && challenge.tags.length > 0 && (
          <div className="tags">
            {challenge.tags.map((t) => (
              <span key={t} className="tag">{t}</span>
            ))}
          </div>
        )}
        <div className="description markdown-body">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{challenge.description}</ReactMarkdown>
        </div>
      </div>

      <div className="editor-panel">
        <h2>Solution</h2>
        <AceEditor
          mode="python"
          theme="monokai"
          value={code}
          onChange={(value) => setCode(value)}
          width="100%"
          height="400px"
          fontSize={14}
          setOptions={{ useWorker: false }}
        />
        <button 
          onClick={handleSubmit} 
          disabled={loading}
          className="submit-btn"
        >
          {loading ? 'Grading...' : 'Submit Solution'}
        </button>
      </div>

      {submitted && results && (
        <div className={`results-panel ${results.passed ? 'passed' : 'failed'}`}>
          <h2>{results.passed ? '✓ Passed!' : '✗ Failed'}</h2>
          {results.results.error && (
            <div className="error">
              <pre>{results.results.error}</pre>
            </div>
          )}
          {results.results.output && (
            <div className="output">
              <h3>Output:</h3>
              <pre>{results.results.output}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ChallengeEditor;
