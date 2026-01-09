import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/Navigation.css';

function Navigation({ user, onSetUser }) {
  const [showUserInput, setShowUserInput] = useState(false);
  const [tempUsername, setTempUsername] = useState(user);

  const handleSetUser = () => {
    if (tempUsername.trim()) {
      onSetUser(tempUsername);
      setShowUserInput(false);
    }
  };

  return (
    <nav className="navigation">
      <div className="nav-content">
        <Link to="/" className="nav-brand">
          🎄 Quantum Advent Calendar
        </Link>
        
        <div className="nav-links">
          <Link to="/">Challenges</Link>
          <Link to="/leaderboard">Leaderboard</Link>
          {user && <Link to="/progress">Progress</Link>}
        </div>

        <div className="nav-user">
          {user ? (
            <div className="user-info">
              <span>👤 {user}</span>
              <button onClick={() => {
                setTempUsername('');
                onSetUser('');
                setShowUserInput(false);
              }}>Logout</button>
            </div>
          ) : (
            <button onClick={() => setShowUserInput(true)}>Login</button>
          )}
        </div>
      </div>

      {showUserInput && (
        <div className="user-modal">
          <div className="modal-content">
            <h2>Enter Your Username</h2>
            <input
              type="text"
              placeholder="Your username"
              value={tempUsername}
              onChange={(e) => setTempUsername(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSetUser()}
            />
            <button onClick={handleSetUser}>Set Username</button>
            <button onClick={() => setShowUserInput(false)}>Cancel</button>
          </div>
        </div>
      )}
    </nav>
  );
}

export default Navigation;
