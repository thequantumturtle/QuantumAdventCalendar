import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Leaderboard.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const response = await axios.get(`${API_URL}/leaderboard/`);
      setLeaderboard(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
      setLoading(false);
    }
  };

  if (loading) return <div>Loading leaderboard...</div>;

  return (
    <div className="leaderboard">
      <h1>Global Leaderboard</h1>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Username</th>
            <th>Challenges Completed</th>
            <th>Total Submissions</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((entry) => (
            <tr key={entry.rank}>
              <td className="rank">#{entry.rank}</td>
              <td>{entry.username}</td>
              <td>{entry.completed}/25</td>
              <td>{entry.total_submissions}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;
