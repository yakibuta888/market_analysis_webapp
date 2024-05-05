// src/components/ChartSelector.tsx
import React from 'react';

interface ChartSelectorProps {
  selectedChart: number | null;
  onChange: (chartId: number) => void;
}

const ChartSelector: React.FC<ChartSelectorProps> = ({ selectedChart, onChange }) => {
  return (
    <select value={selectedChart ?? ''} onChange={(e) => onChange(Number(e.target.value))}>
      <option value="">Select a chart</option>
      <option value="1">Chart 1</option>
      <option value="2">Chart 2</option>
      <option value="3">Chart 3</option>
    </select>
  );
};

export default ChartSelector;
