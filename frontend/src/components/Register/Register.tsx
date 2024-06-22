// src/components/Register/Register.tsx
import React from "react";
import { TextField, Button, Container, Typography } from "@mui/material";

import "./Register.scss";
import { RegisterViewModel } from "../../viewModels/RegisterViewModel";

const Register: React.FC = () => {
  const {
    email,
    password,
    name,
    handleEmailChange,
    handlePasswordChange,
    handleNameChange,
    handleSubmit,
    authState,
  } = RegisterViewModel();

  return (
    <Container component="main" maxWidth="xs">
      <div className="register-container">
        <Typography component="h1" variant="h5">
          Sign up
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email Address"
            name="email"
            autoComplete="email"
            autoFocus
            value={email}
            onChange={handleEmailChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="name"
            label="Name"
            id="name"
            autoComplete="name"
            value={name}
            onChange={handleNameChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={handlePasswordChange}
          />
          {authState.error && (
            <Typography color="error">{authState.error.message}</Typography>
          )}
          {authState.message && (
            <Typography color={authState.error ? "error" : "primary"}>
              {authState.message}
            </Typography>
          )}
          <Button
            type="submit"
            fullWidth
            variant="outlined"
            color="primary"
            className="submit"
            disabled={authState.loading || authState.message !== ""}
          >
            Sign Up
          </Button>
        </form>
      </div>
    </Container>
  );
};

export default Register;
