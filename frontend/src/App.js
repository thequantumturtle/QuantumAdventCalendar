import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import ChallengeList from './pages/ChallengeList';
import ChallengeEditor from './pages/ChallengeEditor';
import Leaderboard from './pages/Leaderboard';
import UserProgress from './pages/UserProgress';
import Navigation from './components/Navigation';

function App() {
  const [user, setUser] = useState(localStorage.getItem('username') || '');

  const handleSetUser = (username) => {
    setUser(username);
    localStorage.setItem('username', username);
  };

  return (
    <Router>
      <Navigation user={user} onSetUser={handleSetUser} />
      <div className="app-container">
        <Routes>
          <Route path="/" element={<ChallengeList />} />
          <Route path="/challenge/:day" element={<ChallengeEditor user={user} />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/progress" element={<UserProgress user={user} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
