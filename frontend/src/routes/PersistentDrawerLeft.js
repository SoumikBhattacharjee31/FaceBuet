import * as React from "react";
import Box from "@mui/material/Box";
import Navbar from "../components/Navbar";
import RightSidebar from "../components/RightSidebar";
import Feed from "../components/Feed";
import CreatePost from "../components/CreatePost";


export default function PersistentDrawerLeft() {
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const [currentComponent, setCurrentComponent] = React.useState("feed");

  return (
    <Box sx={{ display: "flex" }}>
      <Navbar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} setCurrentComponent = {setCurrentComponent} />
      <RightSidebar/>
      { currentComponent === "feed" && < Feed open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "createpost" && < CreatePost open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
    </Box>
  );
}
