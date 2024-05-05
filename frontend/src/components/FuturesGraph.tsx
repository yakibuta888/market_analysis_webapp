// src/components/FuturesGraph.tsx
import React from 'react';
import Plot from 'react-plotly.js';
import { useFuturesChartViewModel } from '../viewModels/FuturesGraphViewModel';

const FuturesChart: React.FC = () => {
  const { data, loading, error } = useFuturesChartViewModel();

  if (loading) return <div>Loading data...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!Array.isArray(data)) return <div>Invalid data format</div>;

  console.log(data);
  return (
    <Plot
      data={[
        {
          x: data.map(d => d.month),
          y: data.map(d => d.settle),
          type: 'scatter',
          mode: 'lines+markers',
          marker: { color: 'red' },
        },
      ]}
      layout={{ width: 920, height: 440, title: 'Gold Futures' }}
    />
  );
};

export default FuturesChart;
