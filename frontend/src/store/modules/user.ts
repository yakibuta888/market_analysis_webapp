import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { fetchUserData } from "../../api/userApi";
import { Axios, AxiosError } from "axios";

export interface User {
  id: number;
  email: string;
  name: string;
}

export interface UserState {
  userData: User | null;
  loading: boolean;
  error: Error | null;
}

// 非同期アクションクリエーター
export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (_, { rejectWithValue }) => {
    try {
      const data = await fetchUserData();
      return data;
    } catch (error) {
      if (error && (error as AxiosError).response) {
        return rejectWithValue((error as AxiosError).response?.data);
      }
      return rejectWithValue(error);
    }
  }
);

const user = createSlice({
  name: 'user',
  initialState: {
    userData: null,
    loading: false,
    error: null
  } as UserState,
  reducers: {
    // fetchUserRequest(state) {
    //   state.loading = true;
    // },
    // fetchUserSuccess(state, action) {
    //   state.loading = false;
    //   state.userData = action.payload;
    // },
    // fetchUserFailure(state, action) {
    //   state.loading = false;
    //   state.error = action.payload;
    // }
  },
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

// const { fetchUserRequest, fetchUserSuccess, fetchUserFailure } = user.actions;

// export { fetchUserRequest, fetchUserSuccess, fetchUserFailure }
export default user.reducer;
