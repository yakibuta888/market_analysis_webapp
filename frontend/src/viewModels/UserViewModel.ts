// src/viewModels/UserViewModel.ts
import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { fetchUser } from '../store/modules/user';
import { RootState, AppDispatch } from '../store';


export const useUserViewModel = () => {
  const user = useSelector((state: RootState) => state.user.userData);
  const loading = useSelector((state: RootState) => state.user.loading);
  const error = useSelector((state: RootState) => state.user.error);
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(fetchUser());
  }, [dispatch]);

  return { user, loading, error };
};
