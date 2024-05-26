import React from "react";
import { Button, TextField, CircularProgress, Typography, Box } from "@mui/material";

import "./Login.scss"
import { LoginViewModel } from "@/viewModels/LoginViewModel";


const Login: React.FC = () => {
  const {
    email,
    password,
    handleEmailChange,
    handlePasswordChange,
    handleSubmit,
    authState,
  } = LoginViewModel();

  return (
    <div className="login">
      <Box component="div" sx={{ maxWidth: 400, margin: 'auto', padding: 2, boxShadow: 3, borderRadius: 2 }}>
        <div className="loginLogo">
          <img src="./phoenix.png" alt="logo" />
        </div>
        <Typography variant="h4" component="h2" gutterBottom>
          Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <Box mb={2}>
            <TextField
              label="Email"
              type="email"
              value={email}
              onChange={handleEmailChange}
              required
              fullWidth
            />
          </Box>
          <Box mb={2}>
            <TextField
              label="Password"
              type="password"
              value={password}
              onChange={handlePasswordChange}
              required
              fullWidth
            />
          </Box>
          {authState.error && (
            <Box mb={2} color="error.main">
              <Typography>{authState.error.message}</Typography>
            </Box>
          )}
          <Button
            type="submit"
            variant="outlined"
            color="primary"
            disabled={authState.loading}
            fullWidth
          >
            {authState.loading ? <CircularProgress size={24} /> : 'Login'}
          </Button>
        </form>
      </Box>
    </div>
  );
}

export default Login;
