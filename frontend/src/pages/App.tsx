import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Login from './Login/Login';
import Stations from './Stations/Stations';
import Favorites from './Favorites/Favorites';
import Profile from './Profile/Profile';

export default function App() {
  return (
    <div>
      <nav>
        <Link to="/">Stations</Link> | 
        <Link to="/favorites">Favorites</Link> | 
        <Link to="/profile">Profile</Link> | 
        <Link to="/login">Login</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Stations />} />
        <Route path="/favorites" element={<Favorites />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </div>
  );
}
