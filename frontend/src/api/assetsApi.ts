// src/api/assetsApi.ts
import axios from 'axios';

const API_URL = '/api/assets';

export const fetchAssetsData = async () => {
  try {
    const response = await axios.get(`${API_URL}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching assets data:', error);
    throw error;
  }
};
