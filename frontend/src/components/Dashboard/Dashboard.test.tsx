// src/components/Dashboard/Dashboard.test.tsx
// src/components/Dashboard/Dashboard.test.tsx
import { render, screen } from '@testing-library/react';
import { Provider } from 'react-redux';
import store from '@/store';
import Dashboard from './Dashboard';
import { describe, it, expect } from 'vitest';

describe('Dashboard component', () => {
  it('renders loading state initially', () => {
    render(
      <Provider store={store}>
        <Dashboard />
      </Provider>
    );
    expect(screen.getByText('Loading user...')).toBeInTheDocument();
  });

  // Add more tests for different states and interactions
});
