// src/viewModels/DashboardViewModel.ts
import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { AnyAction } from 'redux';

import { fetchUser } from '../store/modules/user';
import { RootState } from '../store';


export const useDashboardViewModel = () => {
  const user = useSelector((state: RootState) => state.user.userData);
  const dispatch = useDispatch<ThunkDispatch<RootState, unknown, AnyAction>>();

  useEffect(() => {
    if (!user) {
      dispatch(fetchUser());
    }
  }, [dispatch, user]);

  // ViewModelがダッシュボード固有の状態を持つ場合の例
  const [selectedChart, setSelectedChart] = useState<number | null>(null);

  const selectChart = (chartId: number) => {
    setSelectedChart(chartId);
  };

  return { user, selectedChart, selectChart };
};
