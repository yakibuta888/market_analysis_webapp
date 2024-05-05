import axios from 'axios';

const API_URL = 'http://backend:8000/users';

export const fetchUserData = async () => {
  const response = await axios.get(`${API_URL}/1`);
  return response.data;
};
