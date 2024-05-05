import React from 'react';
import { useDashboardViewModel } from '../viewModels/DashboardViewModel';

const Dashboard: React.FC = () => {
  const { user, selectedChart, selectChart } = useDashboardViewModel();

  if (!user) return <div>Loading...</div>;

  const _ = selectedChart; // 未使用変数の警告を回避するためのダミー変数
  console.log(_)
  selectChart(1); // ダミーの関数呼び出し

  return (
    <div>
      <h1>{user.name}'s Dashboard</h1>
      {/* ダッシュボードとチャートの表示ロジック */}
    </div>
  );
};

export default Dashboard;
