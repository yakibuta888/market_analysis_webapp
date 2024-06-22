import "./Sidebar.scss";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import AddIcon from '@mui/icons-material/Add';

import { logout } from '@/store/modules/auth';
import SidebarChannel from "./SidebarChannel";
import MicIcon from '@mui/icons-material/Mic';
import HeadphonesIcon from '@mui/icons-material/Headphones';
import SettingsIcon from '@mui/icons-material/Settings';
import { useAppDispatch, useAppSelector } from "@/store/hooks";


const Sidebar = () => {
  const user = useAppSelector((state) => state.auth.user);
  const dispatch = useAppDispatch();

  const handleLogout = () => {
    dispatch(logout());
  };


  return (
    <div className="sidebar">
      <div className="sidebarLeft">
        <div className="webAppIcon">
          <img src="./phoenix.png" alt="Server Icon" />
        </div>
        <div className="serverIcon">
          <img src="./phoenix.png" alt="Server Icon" />
        </div>
      </div>
      <div className="sidebarRight">
        <div className="sidebarTop">
          <h3>Market Analysis</h3>
          <ExpandMoreIcon />
        </div>

        <div className="sidebarChannels">
          <div className="sidebarChannelsHeader">
            <div className="sidebarHeader">
              <ExpandMoreIcon />
              <h4>Channel</h4>
            </div>
            <AddIcon className="sidebarAddIcon"/>
          </div>

          <div className="sidebarChannelList">
            <SidebarChannel />
          </div>

          <div className="sidebarFooter">
            <div className="sidebarAccount">
              <img src={user?.photo ? user.photo : "./phoenix.png"} alt="" onClick={() => handleLogout()}/>
              <div className="accountName">
                <h4>{user?.name}</h4>
                <span>#{user?.id}</span>
              </div>
            </div>

            <div className="sidebarVoice">
              <MicIcon />
              <HeadphonesIcon />
              <SettingsIcon />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
