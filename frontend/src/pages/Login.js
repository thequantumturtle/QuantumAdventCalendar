import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Login.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function Login({ onLogin }) {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isLogin) {
        // Login
        const response = await fetch(`${API_URL}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: formData.username,
            password: formData.password
          })
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.error || 'Login failed');
        }

        const data = await response.json();
        onLogin(data.user, data.access_token, data.refresh_token);
        navigate('/');
      } else {
        // Register
        if (formData.password !== formData.confirmPassword) {
          throw new Error('Passwords do not match');
        }

        const response = await fetch(`${API_URL}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: formData.username,
            email: formData.email,
            password: formData.password
          })
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.error || 'Registration failed');
        }

        // Auto-login after registration
        const loginResponse = await fetch(`${API_URL}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: formData.username,
            password: formData.password
          })
        });

        if (!loginResponse.ok) {
          throw new Error('Auto-login failed after registration');
        }

        const loginData = await loginResponse.json();
        onLogin(loginData.user, loginData.access_token, loginData.refresh_token);
        navigate('/');
      }
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setFormData({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    });
    setError('');
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>⚛️ Quantum Advent Calendar</h1>
        
        <div className="login-form">
          <h2>{isLogin ? 'Login' : 'Sign Up'}</h2>
          
          {error && <div className="error-message">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="3-20 characters, alphanumeric + underscore"
                required
              />
            </div>

            {!isLogin && (
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="your@email.com"
                  required
                />
              </div>
            )}

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder={isLogin ? 'Enter password' : 'Minimum 8 characters'}
                required
              />
            </div>

            {!isLogin && (
              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="Re-enter password"
                  required
                />
              </div>
            )}

            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? 'Loading...' : isLogin ? 'Login' : 'Create Account'}
            </button>
          </form>

          <div className="toggle-mode">
            <p>
              {isLogin ? "Don't have an account? " : 'Already have an account? '}
              <button type="button" onClick={toggleMode} className="toggle-btn">
                {isLogin ? 'Sign Up' : 'Login'}
              </button>
            </p>
          </div>
        </div>

        <div className="login-info">
          <h3>About Quantum Advent Calendar</h3>
          <p>A daily quantum computing challenge from Dec 1-25.</p>
          <p>Learn quantum circuits, gates, and algorithms through hands-on coding.</p>
          <p>All submissions are graded automatically using Qiskit.</p>
        </div>
      </div>
    </div>
  );
}

export default Login;
