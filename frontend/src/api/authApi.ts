// src/api/authApi.ts
import axios from 'axios';

const LOGIN_API_URL = '/api/login';
const USER_API_URL = '/api/users/me';
const VERIFY_API_URL = '/api/verify';
const REGISTER_API_URL = '/api/register';

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


export const verifyTokenAndFetchUserData = async ({ verifyToken }: { verifyToken: string }) => {
  try {
    const response = await axios.get(VERIFY_API_URL, { params: { token: verifyToken } });
    const accessToken = response.data.access_token;
    const userResponse = await fetchUserData({ token: accessToken });
    return { token: accessToken, user: userResponse };
  } catch (error) {
    console.error('Error verifying token:', error);
    throw error;
  }
};


export interface RegisterParams {
  email: string;
  password: string;
  name: string;
}


export const registUser = async ({ email, password, name }: RegisterParams) => {
  try {
    const action = "sendVerificationEmail";
    const response = await axios.post(REGISTER_API_URL, { action, email, password, name });
    return response.data;
  } catch (error) {
    console.error('Error registering user:', error);
    throw error;
  }
}
