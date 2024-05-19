// src/store/modules/futuresData.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { AxiosError } from 'axios';

import { fetchFuturesDataApi } from '../../api/futuresDataApi';
import { FuturesDataArray } from '../../types/futuresDataTypes';


export const fetchFuturesData = createAsyncThunk(
  'futuresData/fetchFuturesData',
  async ({ asset, tradeDate }: { asset: string, tradeDate: string }, { rejectWithValue }) => {
    try {
      const data = await fetchFuturesDataApi(asset, tradeDate);
      return data;
    } catch (error) {
      if (error && (error as AxiosError).message) {
        return rejectWithValue({
          message: (error as AxiosError).message,
          code: (error as AxiosError).code,
          url: (error as AxiosError).config?.url
        });
      }
      return rejectWithValue(error);
    }
  }
);

// ステートの型
export interface futuresDataState {
  data: FuturesDataArray;
  loading: boolean;
  error: Error | null;
}

// スライスの設定
const futuresDataSlice = createSlice({
  name: 'futuresData',
  initialState: {
    data: [],
    loading: false,
    error: null
  } as futuresDataState,
  reducers: {
    clearFuturesData: (state) => {
      state.data = [];
      state.loading = false;
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchFuturesData.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchFuturesData.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(fetchFuturesData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as Error;
      });
  }
});

export const { clearFuturesData } = futuresDataSlice.actions;

export default futuresDataSlice.reducer;
