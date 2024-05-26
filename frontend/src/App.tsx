// src/App.tsx

import React, { useEffect } from 'react';

import './App.scss';
import { useAppDispatch, useAppSelector } from './store/hooks';
import { initializeAuth } from './store/modules/auth';
import Dashboard from './components/Dashboard/Dashboard';
import Sidebar from './components/Sidebar/Sidebar';
import Login from './components/login/Login';


const App: React.FC = () => {
  const isLoggedIn = useAppSelector((state) => state.auth.token !== null);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(initializeAuth());
  }, [dispatch]);

  return (
      <div className="container">
        {isLoggedIn ? (
          <>
            <Sidebar />
            <Dashboard />
          </>
        ) : (
          <>
            <Login />
          </>
        )}
      </div>
  );
};

export default App;
