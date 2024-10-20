import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './Dashboard.module.css';

function Dashboard() {
  const [message, setMessage] = useState('');
  const [workouts, setWorkouts] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/dashboard', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setMessage(response.data.message);
        
        const workoutsResponse = await axios.get('http://localhost:5000/api/workouts', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setWorkouts(workoutsResponse.data.workouts);
      } catch (error) {
        console.error('Failed to fetch dashboard:', error);
        if (error.response && error.response.status === 401) {
          navigate('/login');
        }
      }
    };

    fetchDashboard();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Dashboard</h2>
      <p>{message}</p>
      <h3>Your Workouts</h3>
      <ul className={styles.workoutList}>
        {workouts.map((workout) => (
          <li key={workout.id} className={styles.workoutItem}>
            {workout.type} - Duration: {workout.duration} minutes, Calories: {workout.calories}
          </li>
        ))}
      </ul>
      <div className={styles.nav}>
        <Link to="/workouts/new">Log New Workout</Link>
        <Link to="/groups">View Groups</Link>
        <button onClick={handleLogout}>Logout</button>
      </div>
    </div>
  );
}

export default Dashboard;