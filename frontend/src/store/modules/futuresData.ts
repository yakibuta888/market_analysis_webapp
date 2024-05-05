// src/store/modules/futuresData.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios, { AxiosError } from 'axios';

// APIからデータを取得する非同期アクション
export const fetchFuturesData = createAsyncThunk(
  'futuresData/fetchFuturesData',
  async (tradeDate: string, { rejectWithValue }) => {
    try {
      const response = await axios.get(`/api/futures-data/gold?trade_dates=${tradeDate}`);
      // 応答が配列でない場合の加工
      return response.data.data;
    } catch (error) {
      return rejectWithValue((error as AxiosError).response?.data);
    }
  }
);

// ステートの型
export interface futuresDataState {
  data: any[];
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
  reducers: {},
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

export default futuresDataSlice.reducer;
