import * as React from "react";
import Box from "@mui/material/Box";
import Navbar from "../components/Navbar";
import RightSidebar from "../components/RightSidebar";
import Feed from "../components/Feed";
import CreatePost from "../components/CreatePost";
import Friends from "../components/Friends";
import FriendReq from "../components/FriendReq";
import Groups from "../components/Groups";
import CreateGroup from "../components/CreateGroup";
import Pages from "../components/Pages";
import CreatePage from "../components/CreatePage";
import ChatHome from "../components/ChatHome";
import Events from "../components/Events";
import CreateEvent from "../components/CreateEvent";
import MarketPlace from "../components/MarketPlace";
import CreateMarketPlace from "../components/CreateMarketPlace";
import Profile from "../components/Profile";
import SearchPage from "../components/SearchPage";


export default function PersistentDrawerLeft() {
  const [searchData, setSearchData] = React.useState([]);
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const [currentComponent, setCurrentComponent] = React.useState("feed");

  return (
    <Box sx={{ display: "flex" }}>
      <Navbar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} setCurrentComponent = {setCurrentComponent} setSearchData = {setSearchData} />
      { currentComponent.toLowerCase() === "feed" && < Feed open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "createpost" && < CreatePost open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Groups" && < Groups open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Pages" && < Pages open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Friends" && < Friends open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Requests" && < FriendReq open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "creategroup" && < CreateGroup open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "createpage" && < CreatePage open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Messages" && < ChatHome open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Events" && < Events open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "createevent" && < CreateEvent open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "MarketPlace" && < MarketPlace open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "createmarketplace" && < CreateMarketPlace open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Profile" && < Profile open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "search" && < SearchPage open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} searchData = {searchData} />}
      <RightSidebar/>
    </Box>
  );
}
