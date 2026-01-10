import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/Navigation.css';

function Navigation({ user, token, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  return (
    <nav className="navigation">
      <div className="nav-content">
        <Link to="/" className="nav-brand">
          🎄 Quantum Advent Calendar
        </Link>
        
        <div className="nav-links">
          {user && (
            <>
              <Link to="/">Challenges</Link>
              <Link to="/leaderboard">Leaderboard</Link>
              <Link to="/progress">Progress</Link>
            </>
          )}
        </div>

        <div className="nav-user">
          {user ? (
            <div className="user-info">
              <span className="username">👤 {user.username}</span>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </div>
          ) : (
            <Link to="/login" className="login-link">Login</Link>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navigation;
