// src/store/modules/assets.ts
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { AxiosError } from "axios";

import { fetchAssetsData } from "../../api/assetsApi";
import { AssetsArray } from "../../types/assetTypes";


// 非同期アクションクリエーター
export const fetchAssets = createAsyncThunk(
  'assets/fetchAssets',
  async (_, { rejectWithValue }) => {
    try {
      const data = await fetchAssetsData();
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


export interface AssetsState {
  assetsData: AssetsArray;
  loading: boolean;
  error: Error | null;
}

const assets = createSlice({
  name: 'assets',
  initialState: {
    assetsData: [],
    loading: false,
    error: null
  } as AssetsState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(fetchAssets.pending, state => {
        state.loading = true;
        state.error = null;
    })
      .addCase(fetchAssets.fulfilled, (state, action) => {
        state.loading = false;
        state.assetsData = action.payload;
    })
      .addCase(fetchAssets.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as Error;
    });
  }
});

export default assets.reducer;
