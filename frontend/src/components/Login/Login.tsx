// src/components/Login/Login.tsx
import React from "react";
import {
  Button,
  TextField,
  CircularProgress,
  Typography,
  Container,
} from "@mui/material";

import "./Login.scss";
import { LoginViewModel } from "@/viewModels/LoginViewModel";

const Login: React.FC = () => {
  const {
    email,
    password,
    handleEmailChange,
    handlePasswordChange,
    handleSubmit,
    authState,
    handleSignUpClick,
  } = LoginViewModel();

  return (
    <Container component="main" maxWidth="xs">
      <div className="login">
        <div className="loginLogo">
          <img src="./phoenix.png" alt="logo" />
        </div>
        <Typography variant="h4" component="h1" gutterBottom>
          Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Email"
            type="email"
            value={email}
            onChange={handleEmailChange}
            margin="normal"
            required
            fullWidth
          />
          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={handlePasswordChange}
            margin="normal"
            required
            fullWidth
          />
          {authState.error && (
            <Typography color="error">{authState.error.message}</Typography>
          )}
          <Button
            type="submit"
            variant="outlined"
            color="primary"
            disabled={authState.loading}
            fullWidth
          >
            {authState.loading ? <CircularProgress size={24} /> : "Login"}
          </Button>
        </form>
        <Button
          variant="contained"
          color="secondary"
          fullWidth
          onClick={handleSignUpClick}
        >
          Sign Up
        </Button>
      </div>
    </Container>
  );
};

export default Login;
