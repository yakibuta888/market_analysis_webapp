// src/store/modules/tradeDates.ts
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { AxiosError } from "axios";

import { fetchTradeDatesApi, FetchTradeDatesParams } from "../../api/tradeDatesApi";
import { TradeDatesArray } from "../../types/tradeDateTypes";


// 非同期アクションクリエーター
export const fetchTradeDates = createAsyncThunk(
  'tradeDates/fetchTradeDates',
  async (params: FetchTradeDatesParams, { rejectWithValue }) => {
    try {
      const data = await fetchTradeDatesApi(params);
      return data;
    } catch (error) {
      if (error && (error as AxiosError).message) {
        return rejectWithValue({
          message: (error as AxiosError).message,  // エラーメッセージ
          code: (error as AxiosError).code,        // エラーコード
          url: (error as AxiosError).config?.url   // エラーが発生したリクエストのURL
        });
      }
      return rejectWithValue(error);
    }
  }
);


// ステートの型
export interface TradeDatesState {
  datesData: TradeDatesArray;
  loading: boolean;
  error: Error | null;
}

// スライスの設定
const tradeDatesSlice = createSlice({
  name: 'tradeDates',
  initialState: {
    datesData: [],
    loading: false,
    error: null
  } as TradeDatesState,
  reducers: {
    clearTradeDates: (state) => {
      state.datesData = [];
      state.loading = false;
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTradeDates.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchTradeDates.fulfilled, (state, action) => {
        state.loading = false;
        state.datesData = action.payload;
      })
      .addCase(fetchTradeDates.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as Error;
      });
  }
});

export const { clearTradeDates } = tradeDatesSlice.actions;

export default tradeDatesSlice.reducer;
