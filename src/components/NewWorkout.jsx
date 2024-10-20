import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function NewWorkout() {
  const [type, setType] = useState('');
  const [duration, setDuration] = useState('');
  const [calories, setCalories] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/workouts', 
        { type, duration: parseInt(duration), calories: parseInt(calories) },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      navigate('/dashboard');
    } catch (error) {
      console.error('Failed to log workout:', error);
    }
  };

  return (
    <div>
      <h2>Log New Workout</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={type}
          onChange={(e) => setType(e.target.value)}
          placeholder="Workout type"
          required
        />
        <input
          type="number"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
          placeholder="Duration (minutes)"
          required
        />
        <input
          type="number"
          value={calories}
          onChange={(e) => setCalories(e.target.value)}
          placeholder="Calories burned"
          required
        />
        <button type="submit">Log Workout</button>
      </form>
    </div>
  );
}

export default NewWorkout;