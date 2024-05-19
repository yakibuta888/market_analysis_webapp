// src/viewModels/FuturesGraphViewModel.ts
import { useEffect } from 'react';

import { fetchFuturesData, clearFuturesData } from '../store/modules/futuresData';
import { useAppDispatch, useAppSelector } from '@/store/hooks';


export const useFuturesChartViewModel = (params: {
  asset: string,
  tradeDate: string
}) => {
  const dispatch = useAppDispatch();
  const data = useAppSelector((state) => state.futuresData.data);
  const loading = useAppSelector((state) => state.futuresData.loading);
  const error = useAppSelector((state) => state.futuresData.error);

  useEffect(() => {
    if (params.asset || params.tradeDate) {
      dispatch(clearFuturesData());
      dispatch(fetchFuturesData(params));
    }
  }, [dispatch, params.asset, params.tradeDate]);

  return { data, loading, error };
};
