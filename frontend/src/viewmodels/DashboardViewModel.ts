
import { useState, useEffect } from 'react';
import UserService from '../services/UserService';

const useDashboardViewModel = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const fetchUsers = async () => {
            const data = await UserService.getAllUsers();
            setUsers(data);
        };

        fetchUsers();
    }, []);

    return { users };
};

export default useDashboardViewModel;
