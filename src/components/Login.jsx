import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import styles from './Login.module.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/api/login', { email, password });
      localStorage.setItem('token', response.data.token);
      navigate('/dashboard');
    } catch (error) {
      setError('Invalid email or password');
      console.error('Login failed:', error);
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Login</h2>
      {error && <p className={styles.error}>{error}</p>}
      <form onSubmit={handleSubmit} className={styles.form}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
          required
        />
        <button type="submit">Login</button>
      </form>
      <p>Don't have an account? <Link to="/register">Register</Link></p>
    </div>
  );
}

export default Login;