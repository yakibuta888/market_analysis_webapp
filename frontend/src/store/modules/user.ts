// src/store/modules/user.ts
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { AxiosError } from "axios";

import { fetchUserData } from "../../api/userApi";
import { User } from "../../types/userTypes";


// 非同期アクションクリエーター
export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (_, { rejectWithValue }) => {
    try {
      const data = await fetchUserData();
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

export interface UserState {
  userData: User | null;
  loading: boolean;
  error: Error | null;
}

const user = createSlice({
  name: 'user',
  initialState: {
    userData: null,
    loading: false,
    error: null
  } as UserState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(fetchUser.pending, state => {
        state.loading = true;
        state.error = null;
    })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = false;
        state.userData = action.payload;
    })
      .addCase(fetchUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as Error;
    });
  }
});

export default user.reducer;
