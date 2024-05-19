// src/viewModels/UserViewModel.ts
import { useEffect } from 'react';

import { fetchUser } from '../store/modules/user';
import { useAppDispatch, useAppSelector } from '@/store/hooks';


export const useUserViewModel = () => {
  const user = useAppSelector((state) => state.user.userData);
  const loading = useAppSelector((state) => state.user.loading);
  const error = useAppSelector((state) => state.user.error);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(fetchUser());
  }, [dispatch]);

  return { user, loading, error };
};
