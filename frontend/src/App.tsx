// src/App.tsx

import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';

import './App.scss';
import { useAppDispatch, useAppSelector } from './store/hooks';
import { initializeAuth } from './store/modules/auth';
import Dashboard from './components/Dashboard/Dashboard';
import Sidebar from './components/Sidebar/Sidebar';
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import Verify from './components/Verify';


const App: React.FC = () => {
  const isLoggedIn = useAppSelector((state) => state.auth.token !== null);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(initializeAuth());
  }, [dispatch]);

  return (
    <Router>
      <div className="container">
        <Routes>
          <Route path="/login" element={
            isLoggedIn ? (
              <Navigate to="/dashboard" />
            ) : (
              <Login />
            )} />
          <Route path="/register" element={
            isLoggedIn ? (
              <Navigate to="/dashboard" />
            ) : (
              <Register />
            )} />
          <Route path="/dashboard" element={
            isLoggedIn ? (
              <>
                <Sidebar />
                <Dashboard />
              </>
            ) : (
              <Navigate to="/login" />
            )} />
          <Route path="/verify" element={<Verify />} />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
