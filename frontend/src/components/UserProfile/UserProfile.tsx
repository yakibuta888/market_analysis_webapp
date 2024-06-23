// src/components/UserProfile.tsx
import React from 'react';
import { useUserViewModel } from '../../viewModels/UserViewModel';

const UserProfile: React.FC = () => {
  const { user, loading, error } = useUserViewModel();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>No user data</div>

  return (
    <div>
      <h1>User Profile</h1>
      <div>Name: {user.name}</div>
      <div>Email: {user.email}</div>
    </div>
  );
};

export default UserProfile;
