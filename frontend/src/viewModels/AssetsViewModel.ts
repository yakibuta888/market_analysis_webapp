// src/viewModels/AssetsViewModel.ts
import { useEffect } from 'react';

import { fetchAssets } from '../store/modules/assets';
import { useAppDispatch, useAppSelector } from '@/store/hooks';


export const useAssetsViewModel = () => {
  const assetsData = useAppSelector((state) => state.assets.assetsData);
  const loading = useAppSelector((state) => state.assets.loading);
  const error = useAppSelector((state) => state.assets.error);
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (assetsData.length === 0 && !loading && !error) {
      dispatch(fetchAssets());
    }
  }, [dispatch, assetsData.length, loading, error]);

  return { assetsData, loading, error };
};
