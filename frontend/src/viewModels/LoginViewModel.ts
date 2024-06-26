// src/viewModels/LoginViewModel.ts

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { login } from '../store/modules/auth';
import { useAppDispatch, useAppSelector } from '@/store/hooks';

export const LoginViewModel = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useAppDispatch();
  const authState = useAppSelector(state => state.auth);

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    dispatch(login({ email, password }));
  };

  const navigate = useNavigate();

  const handleSignUpClick = () => {
    navigate('/register');
  };

  return {
    email,
    password,
    handleEmailChange,
    handlePasswordChange,
    handleSubmit,
    authState,
    handleSignUpClick,
  };
};
