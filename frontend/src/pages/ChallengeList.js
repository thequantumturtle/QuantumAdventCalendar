import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import '../styles/ChallengeList.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function ChallengeList() {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchChallenges();
  }, []);

  const fetchChallenges = async () => {
    try {
      const response = await axios.get(`${API_URL}/challenges/`);
      setChallenges(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching challenges:', error);
      setLoading(false);
    }
  };

  if (loading) return <div>Loading challenges...</div>;

  return (
    <div className="challenge-list">
      <h1>Quantum Advent Calendar</h1>
      <p>25 days of quantum computing challenges</p>
      
      <div className="challenges-grid">
        {challenges.map((challenge) => (
          <Link 
            key={challenge.day} 
            to={`/challenge/${challenge.day}`}
            className="challenge-card"
          >
            <div className="day-number">Day {challenge.day}</div>
            <h3>{challenge.title}</h3>
            <div className="difficulty">
              {'★'.repeat(challenge.difficulty)}
              {'☆'.repeat(5 - challenge.difficulty)}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default ChallengeList;
