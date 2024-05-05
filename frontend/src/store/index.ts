import { configureStore } from '@reduxjs/toolkit';
import userReducer from './modules/user';
import futuresDataReducer from './modules/futuresData';

const store = configureStore({
  reducer: {
    user: userReducer,
    futuresData: futuresDataReducer
  }
});

export default store;
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
