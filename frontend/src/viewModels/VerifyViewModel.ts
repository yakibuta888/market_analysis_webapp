// src/viewModels/VerifyViewModel.ts
import { useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useAppDispatch } from '../store/hooks';
import { verifyUser } from '../store/modules/auth';

export const VerifyViewModel = () => {
  const [searchParams] = useSearchParams();
  const verifyToken = searchParams.get('token');
  const dispatch = useAppDispatch();

  const handleVerify = useCallback((verifyToken: string) => {
    dispatch(verifyUser({ verifyToken }));
  }, [dispatch]);

  return {
    verifyToken,
    handleVerify,
  };
};
