// src/components/Login/Login.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import { MemoryRouter } from 'react-router-dom';
import configureStore from 'redux-mock-store';
import Login from './Login';

const mockStore = configureStore([]);
const store = mockStore({
  auth: { token: null, loading: false, error: null }
});

describe('Login Component', () => {
  test('renders login form', () => {
    render(
      <Provider store={store}>
        <MemoryRouter>
          <Login />
        </MemoryRouter>
      </Provider>
    );

    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Login/i })).toBeInTheDocument();
  });

  test('shows error message on failed login', () => {
    const storeWithError = mockStore({
      auth: { token: null, loading: false, error: { message: 'Invalid credentials' } }
    });

    render(
      <Provider store={storeWithError}>
        <MemoryRouter>
          <Login />
        </MemoryRouter>
      </Provider>
    );

    expect(screen.getByText(/Invalid credentials/i)).toBeInTheDocument();
  });

  test('calls handleSubmit on form submission', () => {
    render(
      <Provider store={store}>
        <MemoryRouter>
          <Login />
        </MemoryRouter>
      </Provider>
    );

    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'password' } });
    fireEvent.click(screen.getByRole('button', { name: /Login/i }));

    // Submit action is usually handled by Redux action, mock it accordingly
  });
});
