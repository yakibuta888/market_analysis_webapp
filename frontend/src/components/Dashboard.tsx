// src/components/Dashboard.tsx
import React from 'react';
import { useDashboardViewModel } from '../viewModels/DashboardViewModel';
import ChartDisplay from './ChartDisplay';
import ChartSelector from './ChartSelector';

const Dashboard: React.FC = () => {
  const { user, selectedChart, selectChart } = useDashboardViewModel();

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h1>{user.name}'s Dashboard</h1>
      <ChartSelector selectedChart={selectedChart} onChange={selectChart} />
      {selectedChart && <ChartDisplay chartId={selectedChart} />}
    </div>
  );
};

export default Dashboard;
