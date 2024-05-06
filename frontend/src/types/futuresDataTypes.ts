// src/types/futuresDataTypes.ts
export interface FuturesData {
  trade_date: string;
  month: string;
  settle: number;
  volume: number;
  open_interest: number;
  settle_spread: number;
}

export type FuturesDataArray = FuturesData[];
