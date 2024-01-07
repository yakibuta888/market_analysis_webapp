import { useState, useEffect } from 'react';
import UserService from '../services/UserService';

export const useUserViewModel = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        UserService.getAllUsers().then(setUsers);
    }, []);

    return { users };
};
