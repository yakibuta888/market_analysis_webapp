// src/components/ChartDisplay.tsx
import React from 'react';

interface ChartDisplayProps {
  chartId: number;
}

const ChartDisplay: React.FC<ChartDisplayProps> = ({ chartId }) => {
  return (
    <div>
      <h2>Displaying data for Chart {chartId}</h2>
      {/* ここで選択されたチャートIDに基づいたデータ表示ロジックを実装 */}
    </div>
  );
};

export default ChartDisplay;
