import React, { useState, useEffect } from 'react';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-monokai';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import '../styles/ChallengeEditor.css';

function ChallengeEditor({ user }) {
  const { day } = useParams();
  const [challenge, setChallenge] = useState(null);
  const [code, setCode] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    fetchChallenge();
  }, [day]);

  const fetchChallenge = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/challenges/${day}`);
      setChallenge(response.data);
      setCode(response.data.starter_code);
    } catch (error) {
      console.error('Error fetching challenge:', error);
    }
  };

  const handleSubmit = async () => {
    if (!user) {
      alert('Please set your username first');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/submissions/', {
        username: user,
        day: parseInt(day),
        code: code
      });
      setResults(response.data);
      setSubmitted(true);
    } catch (error) {
      console.error('Error submitting:', error);
      setResults({
        passed: false,
        results: { error: 'Submission failed' }
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
        <div className="description">
          {challenge.description}
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
