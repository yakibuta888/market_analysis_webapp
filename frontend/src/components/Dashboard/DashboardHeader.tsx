import "./DashboardHeader.scss";
import NotificationsIcon from '@mui/icons-material/Notifications';
import PushPinIcon from '@mui/icons-material/PushPin';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import SearchIcon from '@mui/icons-material/Search';
import SendIcon from '@mui/icons-material/Send';
import HelpIcon from '@mui/icons-material/Help';


const DashboardHeader = () => {
  return (
    <div className="dashboardHeader">
      <div className="dashboardHeaderLeft">
        <h3>
          <span className="dashboardHeaderHash">#</span>
          Dashboard
        </h3>
      </div>

      <div className="dashboardHeaderRight">
        <NotificationsIcon />
        <PushPinIcon />
        <PeopleAltIcon />
        <div className="dashboardHeaderSearch">
          <input type="text" placeholder="検索" />
          <SearchIcon />
        </div>
        <SendIcon />
        <HelpIcon />
      </div>
    </div>
  );
}

export default DashboardHeader;
