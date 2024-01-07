import React from 'react';

export const UserList = ({ users }) => (
    <ul>
        {users.map(user => (
            <li key={user.id}>{user.name}</li>
        ))}
    </ul>
);
