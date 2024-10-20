import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import Groups from './components/Groups';
import NewWorkout from './components/NewWorkout';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/groups" element={<Groups />} />
          <Route path="/workouts/new" element={<NewWorkout />} />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;