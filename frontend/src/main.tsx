import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css'; // グローバルスタイルをインポート

const rootElement = document.getElementById('app');
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <App />
      <div>test</div>
    </React.StrictMode>
  );
} else {
  console.error('root element not found');
}
