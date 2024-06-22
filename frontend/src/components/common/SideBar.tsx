// src/components/common/SideBar.tsx
import React from 'react'

import Divider from '@mui/material/Divider';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import MultilineChartIcon from '@mui/icons-material/MultilineChart';
import PersonIcon from '@mui/icons-material/Person';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import LoginIcon from '@mui/icons-material/Login';
import HowToRegIcon from '@mui/icons-material/HowToReg';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAppSelector, useAppDispatch } from '@/store/hooks';
import { logout } from '@/store/modules/auth';


interface SideBarProps {
  drawerWidth: number;
  mobileOpen: boolean;
  handleDrawerClose: () => void;
  handleDrawerTransitionEnd: () => void;
}


interface menuItem {
  text: string,
  path?: string,
  icon: React.ComponentType,
  action?: () => void,
}


const SideBar: React.FC<SideBarProps> = ({ drawerWidth, mobileOpen, handleDrawerClose, handleDrawerTransitionEnd }) => {
  const isLoggedIn = useAppSelector((state) => state.auth.token !== null);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  }

  const MenuItems: menuItem[] = [
    { text: "Home", path: "/", icon: HomeIcon },
    { text: "Dashboard", path: "/dashboard", icon: DashboardIcon },
    { text: "Assets", path: "/assets", icon: AccountBalanceIcon },
    { text: "Futures", path: "/futures", icon: MultilineChartIcon },
  ]

  const SettingItems: menuItem[] = [
    { text: "Profile", path: "/profile", icon: PersonIcon },
    { text: "Settings", path: "/settings", icon: SettingsIcon },
    { text: "Logout", icon: LogoutIcon, action: handleLogout },
  ]

  const GuestItems: menuItem[] = [
    { text: "Login", path: "/login", icon: LoginIcon },
    { text: "Sign up", path: "/register", icon: HowToRegIcon },
  ]

  const baseLinkStyle: React.CSSProperties = {
    textDecoration: "none",
    color: "inherit",
    display: "block",
  }

  const activeLinkStyle: React.CSSProperties = {
    backgroundColor: "rgba(0, 0, 0, 0.08)",
  }

  const drawer = (
    <div>
      <Toolbar />
      <Divider />
      <List>
        {MenuItems.map((item, index) => (
          <NavLink to={item.path || ''} key={item.text} style={({isActive}) => {
            return {
              ...baseLinkStyle,
              ...(isActive ? activeLinkStyle : {}),
            }
          }}>
            <ListItem key={index} disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <item.icon />
                </ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          </NavLink>
        ))}
      </List>
      <Divider />
      {isLoggedIn ?
        <List>
          {SettingItems.map((item, index) => (
            item.path ? (
              <NavLink to={item.path} key={item.text} style={({ isActive }) => {
                return {
                  ...baseLinkStyle,
                  ...(isActive ? activeLinkStyle : {}),
                }
              }}>
                <ListItem key={index} disablePadding>
                  <ListItemButton>
                    <ListItemIcon>
                      <item.icon />
                    </ListItemIcon>
                    <ListItemText primary={item.text} />
                  </ListItemButton>
                </ListItem>
              </NavLink>
            ) : (
              <ListItem key={index} disablePadding>
                <ListItemButton onClick={item.action}>
                  <ListItemIcon>
                    <item.icon />
                  </ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            )
          ))}
        </List>
        :
        <List>
          {GuestItems.map((item, index) => (
            <NavLink to={item.path || ''} key={item.text} style={({ isActive }) => {
              return {
                ...baseLinkStyle,
                ...(isActive ? activeLinkStyle : {}),
              }
            }}>
              <ListItem key={index} disablePadding>
                <ListItemButton>
                  <ListItemIcon>
                    <item.icon />
                  </ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            </NavLink>
          ))}
        </List>
      }
    </div>
  );


  return (
    <Box
      component="nav"
      sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      aria-label="mailbox folders"
    >
      {/* mobile */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onTransitionEnd={handleDrawerTransitionEnd}
        onClose={handleDrawerClose}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
        }}
      >
        {drawer}
      </Drawer>

      {/* PC */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', md: 'block' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
        }}
        open
      >
        {drawer}
      </Drawer>
    </Box>

  )
}

export default SideBar
