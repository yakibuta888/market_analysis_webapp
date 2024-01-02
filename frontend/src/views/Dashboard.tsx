
import React from 'react';
import useDashboardViewModel from '../viewmodels/DashboardViewModel';
import UserList from '../components/UserList';

const Dashboard = () => {
    const { users } = useDashboardViewModel();

    return (
        <div>
            <h1>Dashboard</h1>
            <UserList users={users} />
        </div>
    );
};

export default Dashboard;
