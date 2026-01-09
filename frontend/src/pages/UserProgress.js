import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/UserProgress.css';

function UserProgress({ user }) {
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) fetchProgress();
  }, [user]);

  const fetchProgress = async () => {
    try {
      const response = await axios.get(
        `http://localhost:5000/api/submissions/user/${user}/progress`
      );
      setProgress(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching progress:', error);
      setLoading(false);
    }
  };

  if (!user) return <div>Please set your username to view progress</div>;
  if (loading) return <div>Loading...</div>;
  if (!progress) return <div>No progress yet</div>;

  return (
    <div className="user-progress">
      <h1>{progress.username}'s Progress</h1>
      <div className="progress-stats">
        <div className="stat">
          <h3>{progress.completed}/{progress.total}</h3>
          <p>Challenges Completed</p>
        </div>
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ width: `${progress.percentage}%` }}
          />
          <span>{progress.percentage.toFixed(1)}%</span>
        </div>
      </div>
    </div>
  );
}

export default UserProgress;
