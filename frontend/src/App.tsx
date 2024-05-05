import React from 'react';
import { Provider } from 'react-redux';
import store from './store';
import Dashboard from './components/Dashboard';
import UserProfile from './components/UserProfile';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <Dashboard />
      <UserProfile />
    </Provider>
  );
};

export default App;
