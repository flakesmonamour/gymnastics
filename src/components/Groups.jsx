import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

function Groups() {
  const [groups, setGroups] = useState([]);
  const [newGroupName, setNewGroupName] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/groups', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setGroups(response.data.groups);
      } catch (error) {
        console.error('Failed to fetch groups:', error);
        if (error.response && error.response.status === 401) {
          navigate('/login');
        }
      }
    };

    fetchGroups();
  }, [navigate]);

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/api/groups', 
        { name: newGroupName },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      setGroups([...groups, response.data.group]);
      setNewGroupName('');
    } catch (error) {
      console.error('Failed to create group:', error);
    }
  };

  return (
    <div>
      <h2>Groups</h2>
      <ul>
        {groups.map((group) => (
          <li key={group.id}>{group.name}</li>
        ))}
      </ul>
      <form onSubmit={handleCreateGroup}>
        <input
          type="text"
          value={newGroupName}
          onChange={(e) => setNewGroupName(e.target.value)}
          placeholder="Enter new group name"
          required
        />
        <button type="submit">Create Group</button>
      </form>
      <Link to="/dashboard">Back to Dashboard</Link>
    </div>
  );
}

export default Groups;