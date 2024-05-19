// src/api/tradeDatesApi.ts
import axios from 'axios';

const API_URL = '/api/trade-dates';

export interface FetchTradeDatesParams {
  graphType: string;
  asset: string;
  startDate?: string;
  endDate?: string;
  skip?: number;
  limit?: number;
}

export const fetchTradeDatesApi = async (params: FetchTradeDatesParams) => {
  try {
    const { graphType, asset, startDate, endDate, skip, limit } = params;
    const response = await axios.get(`${API_URL}/`, { params: {
      graph_type: graphType,
      asset_name: asset,
      start_date: startDate,
      end_date: endDate,
      skip,
      limit
    }});
    return response.data.trade_dates;
  } catch (error) {
    console.error('Error fetching trade dates:', error);
    throw error;
  }
};
