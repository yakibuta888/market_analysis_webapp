// src/App.tsx

import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';

import './App.scss';
import { theme } from '@/theme/theme';
import { useAppDispatch, useAppSelector } from './store/hooks';
import { initializeAuth } from './store/modules/auth';
import Dashboard from './components/Dashboard/Dashboard';
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import Verify from './components/Verify';
import AppLayout from './components/Layout/AppLayout';
import NoMatch from './components/NoMatch';
import { ThemeProvider } from '@emotion/react';
import { CssBaseline } from '@mui/material';


const App: React.FC = () => {
  const isLoggedIn = useAppSelector((state) => state.auth.token !== null);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(initializeAuth());
  }, [dispatch]);

  return (
    <ThemeProvider theme={theme}>
    <CssBaseline />
    <Router>
      <div className="container">
        <Routes>
          <Route path="/" element={<AppLayout />} >
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
                  <Dashboard />
                </>
              ) : (
                <Navigate to="/login" />
              )} />
            <Route path="/verify" element={<Verify />} />
            <Route index element={<Navigate to="/login" />} />
            <Route path='*' element={<NoMatch />} />
          </Route>
        </Routes>
      </div>
    </Router>
    </ThemeProvider>
  );
};

export default App;
