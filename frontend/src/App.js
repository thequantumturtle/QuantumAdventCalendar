import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import ChallengeList from './pages/ChallengeList';
import ChallengeEditor from './pages/ChallengeEditor';
import Leaderboard from './pages/Leaderboard';
import UserProgress from './pages/UserProgress';
import Navigation from './components/Navigation';
import Login from './pages/Login';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access_token') || '');
  const [loading, setLoading] = useState(true);

  // Check if user is authenticated on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('access_token');
    if (storedToken) {
      // Verify token is still valid by fetching user info
      verifyToken(storedToken);
    } else {
      setLoading(false);
    }
  }, []);

  const verifyToken = async (token) => {
    try {
      const response = await fetch(`${API_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        setToken(token);
      } else {
        // Token invalid, clear it
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setToken('');
      }
    } catch (error) {
      console.error('Token verification failed:', error);
      setToken('');
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = (userData, accessToken, refreshToken) => {
    setUser(userData);
    setToken(accessToken);
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  };

  const handleLogout = () => {
    setUser(null);
    setToken('');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <Navigation user={user} token={token} onLogout={handleLogout} />
      <div className="app-container">
        <Routes>
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/" element={user ? <ChallengeList /> : <Navigate to="/login" />} />
          <Route path="/challenge/:day" element={user ? <ChallengeEditor user={user} token={token} /> : <Navigate to="/login" />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/progress" element={user ? <UserProgress user={user} token={token} /> : <Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
