// src/components/Dashboard/Dashboard.tsx:
import React from 'react';

import './Dashboard.scss';
import { useDashboardViewModel } from '../../viewModels/DashboardViewModel';
import ChartDisplay from '../ChartDisplay';
import ChartSelector from '../ChartSelector';
import UserProfile from '../UserProfile/UserProfile';
import TradeDatePicker from '../TradeDatePicker/TradeDatePicker';
import FuturesGraph from '../FuturesGraph/FuturesGraph';

const Dashboard: React.FC = () => {
  const {
    user,
    selectedChart,
    selectChart,
    assets,
    assetsLoading,
    assetsError,
    tradeDatesError,
    selectedGraphType,
    setSelectedGraphType,
    selectedAsset,
    setSelectedAsset,
    selectedTradeDate,
    setSelectedTradeDate,
  } = useDashboardViewModel();

  if (!user) return <div>Loading user...</div>;
  if (assetsLoading) return <div>Loading data...</div>;

  return (
    <div className='dashboard'>
      <h1>{user.name}'s Dashboard</h1>
      <div>
        <label htmlFor="graph-type-select">Select Graph Type: </label>
        <select id="graph-type-select" value={selectedGraphType} onChange={(e) => setSelectedGraphType(e.target.value)}>
          <option value="futures-data">Futures Data</option>
          {/* 他のグラフタイプもここに追加できます */}
        </select>
      </div>
      <div>
        <label htmlFor="asset-select">Select Asset: </label>
        <select id="asset-select" value={selectedAsset} onChange={(e) => setSelectedAsset(e.target.value)}>
          <option value="">--Please choose an asset--</option>
          {assets.map(asset => (
            <option key={asset.id} value={asset.name}>{asset.name}</option>
          ))}
        </select>
      </div>
      {selectedAsset && (
        <div>
          <TradeDatePicker
            graphType={selectedGraphType}
            asset={selectedAsset}
            selectedTradeDate={selectedTradeDate}
            onDateChange={setSelectedTradeDate}
          />
        </div>
      )}
      {assetsError || tradeDatesError ? (
        <div>Error: {assetsError?.message || tradeDatesError?.message}</div>
      ) : (
        <div>
          <h2>Asset: {selectedAsset}</h2>
          <h2>Trade Date: {selectedTradeDate}</h2>
        </div>
      )}
      {selectedAsset && selectedTradeDate && (
        <FuturesGraph asset={selectedAsset} tradeDate={selectedTradeDate} />
      )}
      <ChartSelector selectedChart={selectedChart} onChange={selectChart} />
      {selectedChart && <ChartDisplay chartId={selectedChart} />}
      <UserProfile />
    </div>
  );
};

export default Dashboard;
