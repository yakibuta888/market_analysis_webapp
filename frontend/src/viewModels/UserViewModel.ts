// src/viewModels/UserViewModel.ts
import { useEffect } from 'react';

import { fetchUser } from '../store/modules/user';
import { useAppDispatch, useAppSelector } from '@/store/hooks';


export const useUserViewModel = () => {
  const user = useAppSelector((state) => state.auth.user);
  const loading = useAppSelector((state) => state.auth.loading);
  const error = useAppSelector((state) => state.auth.error);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(fetchUser());
  }, [dispatch]);

  return { user, loading, error };
};
