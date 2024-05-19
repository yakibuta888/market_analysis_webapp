// src/viewModels/TradeDatePickerViewModel.ts
import { useEffect } from "react";

import { FetchTradeDatesParams } from "../api/tradeDatesApi";
import { fetchTradeDates, clearTradeDates } from "../store/modules/tradeDates";
import { useAppDispatch, useAppSelector } from "@/store/hooks";


export const useTradeDatePickerViewModel = (params: FetchTradeDatesParams) => {
  const dispatch = useAppDispatch();
  const tradeDates = useAppSelector((state) => state.tradeDates.datesData);
  const loading = useAppSelector((state) => state.tradeDates.loading);
  const error = useAppSelector((state) => state.tradeDates.error);

  useEffect(() => {
    if (params.graphType && params.asset) {
      dispatch(clearTradeDates())
      dispatch(fetchTradeDates(params));
    }
  }, [dispatch, params.graphType, params.asset]);

  return { tradeDates, loading, error };
};
