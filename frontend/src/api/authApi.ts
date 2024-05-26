// src/api/authApi.ts
import axios from 'axios';

const LOGIN_API_URL = '/api/login';
const USER_API_URL = '/api/users/me';

export interface LoginParams {
  email: string;
  password: string;
}


export const fetchUserData = async ({ token }: { token: string }) => {
  try {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    const response = await axios.get(USER_API_URL);
    return response.data;
  } catch (error) {
    console.error('Error fetching user data:', error);
    throw error;
  }

}


export const getTokenAndFetchUserData = async ({ email, password }: LoginParams) => {
  try {
    const response = await axios.post(LOGIN_API_URL, { email, password });
    const token = response.data.access_token;
    const userResponse = await fetchUserData({ token });
    return { token, user: userResponse };
  } catch (error) {
    console.error('Error fetching token:', error);
    throw error;
  }
};
