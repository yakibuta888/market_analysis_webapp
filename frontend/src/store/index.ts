import { configureStore } from '@reduxjs/toolkit';

import assetsReducer from './modules/assets';
import futuresDataReducer from './modules/futuresData';
import tradeDates from './modules/tradeDates';
import userReducer from './modules/user';

const store = configureStore({
  reducer: {
    assets: assetsReducer,
    futuresData: futuresDataReducer,
    tradeDates: tradeDates,
    user: userReducer,
  }
});

export default store;
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
