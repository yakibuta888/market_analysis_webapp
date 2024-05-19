// src/components/TradeDatePicker/TradeDatePicker.tsx:
import React from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { parseISO, format } from 'date-fns';

import { useTradeDatePickerViewModel } from '../../viewModels/TradeDatePickerViewModel';


interface Props {
  graphType: string;
  asset: string;
  startDate?: string;
  endDate?: string;
  skip?: number;
  limit?: number;
  selectedTradeDate: string | null;
  onDateChange: (date: string) => void;
}

const TradeDatePicker: React.FC<Props> = ({ graphType, asset, startDate, endDate, skip, limit, selectedTradeDate, onDateChange }) => {
  const { tradeDates, loading, error } = useTradeDatePickerViewModel({ graphType, asset, startDate, endDate, skip, limit });

  console.log(tradeDates);
  if (loading) return <div>Loading trade dates...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!Array.isArray(tradeDates)) return <div>Invalid trade dates</div>;

  return (
    <DatePicker
      selected={selectedTradeDate ? parseISO(selectedTradeDate) : null}
      onChange={(date: Date) => onDateChange(format(date, 'yyyy-MM-dd'))}
      includeDates={tradeDates.map(d => parseISO(d))}
      placeholderText='Select a trade date'
    />
  );
}

export default TradeDatePicker;
