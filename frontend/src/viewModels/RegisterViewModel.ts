// src/viewModels/RegisterViewModel.ts

import { useState } from 'react';

import { register } from '../store/modules/auth';
import { useAppDispatch, useAppSelector } from '@/store/hooks';

export const RegisterViewModel = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const dispatch = useAppDispatch();
  const authState = useAppSelector(state => state.auth);

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setName(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    dispatch(register({ email, password, name }));
  };

  return {
    email,
    password,
    name,
    handleEmailChange,
    handlePasswordChange,
    handleNameChange,
    handleSubmit,
    authState,
  };
};
