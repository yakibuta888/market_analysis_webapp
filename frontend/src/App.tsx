// src/App.tsx

import React from 'react';

import './App.scss';
import { useAppDispatch, useAppSelector } from './store/hooks';
import Dashboard from './components/Dashboard/Dashboard';
import Sidebar from './components/Sidebar/Sidebar';
import Login from './components/login/Login';


const App: React.FC = () => {
  const user = useAppSelector((state) => state.user.userData);

  return (
      <div className="container">
        {user ? (
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
