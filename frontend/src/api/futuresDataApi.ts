import axios from 'axios';


const API_URL = '/api/futures-data/'

export const fetchFuturesDataApi = async (asset: string, tradeDate: string) => {
  try {
    const response = await axios.get(`${API_URL}/${asset}?trade_dates=${tradeDate}`);
    return response.data.data;
  } catch (error) {
    console.error('Error fetching futures data:', error);
    throw error;
  }
};
