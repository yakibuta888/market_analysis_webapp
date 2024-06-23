// src/components/Verify/Verify.tsx
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAppSelector } from '@/store/hooks';
import { VerifyViewModel } from '@/viewModels/VerifyViewModel';


const Verify: React.FC = () => {
  const { verifyToken, handleVerify } = VerifyViewModel();
  const navigate = useNavigate();
  const isLoggedIn = useAppSelector((state) => state.auth.token !== null);
  const loading = useAppSelector((state) => state.auth.loading);

  useEffect(() => {
    if (verifyToken) {
      handleVerify(verifyToken);
    }
  }, [verifyToken, handleVerify]);

  useEffect(() => {
    if (!loading && isLoggedIn) {
      navigate('/dashboard');
    }
  }, [loading, isLoggedIn, navigate]);

  return loading ? <div>Verifying...</div> : !isLoggedIn ? <div>Verification failed.</div> : null;
};

export default Verify;
