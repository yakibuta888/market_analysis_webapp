import { useEffect } from "react";
import { Button } from "@mui/material";

import "./Login.scss"
import { login, logout, fetchUser } from '@/store/modules/user';
import { useAppDispatch, useAppSelector } from '@/store/hooks';


const Login = () => {
  const dispatch = useAppDispatch();
  const user = useAppSelector((state) => state.user.userData);

  useEffect(() => {
    if (!user) {
      dispatch(fetchUser());
    }
  }, [dispatch, user]);

  const signIn = () => {
    useEffect(() => {
      if (user) {
        dispatch(
          login({
            id: user.id,
            name: user.name,
            email: user.email,
          })
        );
      } else {
        dispatch(logout());
      }
    }, [dispatch]);
  }

  return (
    <div className="login">
      <div className="loginLogo">
        <img src="./phoenix.png" alt="logo" />
      </div>
      <Button variant="outlined" color="primary" onClick={signIn}>Login</Button>
    </div>
  );
}

export default Login;
