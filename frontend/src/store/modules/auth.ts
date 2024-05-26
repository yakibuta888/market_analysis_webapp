// src/store/modules/auth.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios, { AxiosError } from 'axios';

import { fetchUserData, getTokenAndFetchUserData, LoginParams } from '@/api/authApi';
import { User } from '@/types/userTypes';


export const login = createAsyncThunk(
  'auth/login',
  async ({ email, password }: LoginParams, { rejectWithValue }) => {
    try {
      const authData = await getTokenAndFetchUserData({ email, password });
      localStorage.setItem('token', authData.token);
      return authData;
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


export const initializeAuth = createAsyncThunk(
  'auth/initializeAuth',
  async (_, { rejectWithValue }) => {
    const token = localStorage.getItem('token');
    if (!token) {
      return rejectWithValue('No token found');
    }
    try {
      const user = await fetchUserData({ token });
      return { token, user };
    } catch (error) {
      localStorage.removeItem('token');
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


export interface AuthState {
  token: string | null;
  user: User | null;
  loading: boolean;
  error: Error | null;
}

const initialState: AuthState = {
  token: null,
  user: null,
  loading: false,
  error: null,
};


const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.token = null;
      state.user = null;
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.token = action.payload.token;
        state.user = action.payload.user;
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as Error;
      })
      .addCase(initializeAuth.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(initializeAuth.fulfilled, (state, action) => {
        state.loading = false;
        state.token = action.payload.token;
        state.user = action.payload.user;
      })
      .addCase(initializeAuth.rejected, (state, action) => {
        state.loading = false;
        state.token = null;
        state.user = null;
        state.error = action.payload as Error;
      });
  }
});

export const { logout } = authSlice.actions;

export default authSlice.reducer;
