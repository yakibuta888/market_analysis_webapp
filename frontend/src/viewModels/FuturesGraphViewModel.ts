// src/viewModels/FuturesGraphViewModel.ts
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { fetchFuturesData } from '../store/modules/futuresData';
import { RootState, AppDispatch } from '../store';

export const useFuturesChartViewModel = () => {
  const dispatch = useDispatch<AppDispatch>();
  const data = useSelector((state: RootState) => state.futuresData.data);
  const loading = useSelector((state: RootState) => state.futuresData.loading);
  const error = useSelector((state: RootState) => state.futuresData.error);

  useEffect(() => {
    dispatch(fetchFuturesData('2024-04-01'));
  }, [dispatch]);

  return { data, loading, error };
};
