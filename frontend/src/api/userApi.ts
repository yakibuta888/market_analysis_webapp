import axios from 'axios';

const API_URL = '/api/users';

export const fetchUserData = async () => {
  try {
    const response = await axios.get(`${API_URL}/1`);
    return response.data;
  } catch (error) {
    // エラー処理: エラーログを出力する、エラーメッセージを返す、など
    console.error('Error fetching user data:', error);
    throw error; // エラーを再スローして、呼び出し元でさらに処理を行う
  }
};
