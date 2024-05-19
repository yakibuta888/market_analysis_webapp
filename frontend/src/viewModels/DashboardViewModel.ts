// src/viewModels/DashboardViewModel.ts
import { useEffect, useState } from 'react';

import { fetchAssets } from '../store/modules/assets';
import { fetchTradeDates } from '../store/modules/tradeDates';
import { useAppDispatch, useAppSelector } from '@/store/hooks';


export const useDashboardViewModel = () => {
  const dispatch = useAppDispatch();
  const user = useAppSelector((state) => state.user.userData);

  const assets = useAppSelector((state) => state.assets.assetsData);
  const assetsLoading = useAppSelector((state) => state.assets.loading);
  const assetsError = useAppSelector((state) => state.assets.error);

  const tradeDates = useAppSelector((state) => state.tradeDates.datesData);
  const tradeDatesLoading = useAppSelector((state) => state.tradeDates.loading);
  const tradeDatesError = useAppSelector((state) => state.tradeDates.error);

  const [selectedGraphType, setSelectedGraphType] = useState<string>('futures-data');
  const [selectedAsset, setSelectedAsset] = useState<string>('');
  const [selectedTradeDate, setSelectedTradeDate] = useState<string>('');

  useEffect(() => {
    dispatch(fetchAssets());
  }, [dispatch]);

  useEffect(() => {
    if (selectedAsset) {
      dispatch(fetchTradeDates({ graphType: selectedGraphType, asset: selectedAsset }));
    }
  }, [dispatch, selectedGraphType, selectedAsset]);

  // ViewModelがダッシュボード固有の状態を持つ場合の例
  const [selectedChart, setSelectedChart] = useState<number | null>(null);

  const selectChart = (chartId: number) => {
    setSelectedChart(chartId);
  };

  return {
    user,
    selectedChart,
    selectChart,
    assets,
    assetsLoading,
    assetsError,
    tradeDates,
    tradeDatesLoading,
    tradeDatesError,
    selectedGraphType,
    setSelectedGraphType,
    selectedAsset,
    setSelectedAsset,
    selectedTradeDate,
    setSelectedTradeDate
  };
};
