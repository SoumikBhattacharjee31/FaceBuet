import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import CssBaseline from "@mui/material/CssBaseline";
import MuiAppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import InboxIcon from "@mui/icons-material/MoveToInbox";
import MailIcon from "@mui/icons-material/Mail";
import InputBase from "@mui/material/InputBase";
import SearchIcon from "@mui/icons-material/Search";
import GroupIcon from "@mui/icons-material/Group";
import Diversity3Icon from "@mui/icons-material/Diversity3";
import { Link } from "react-router-dom";
import MessageIcon from '@mui/icons-material/Message';
import EmojiFlagsIcon from '@mui/icons-material/EmojiFlags';
import EventIcon from '@mui/icons-material/Event';
import OndemandVideoIcon from '@mui/icons-material/OndemandVideo';
import StorefrontIcon from '@mui/icons-material/Storefront';
import { alpha } from '@mui/material/styles';
import axios from "axios";

//start
const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginRight: theme.spacing(2),
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(3),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('md')]: {
      width: '20ch',
    },
  },
}));
//end







const drawerWidth = 240;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  transition: theme.transitions.create(["margin", "width"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: `${drawerWidth}px`,
    transition: theme.transitions.create(["margin", "width"], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: "flex-end",
}));

export default function Navbar({ isOpen, toggleSidebar, setCurrentComponent }) {

  const theme = useTheme();


  
  const linksLeft = {
    // Profile: "/",
    Feed: "/",
    Friends: "/", // Define the URL for Friends
    Requests: "/",
    Groups: "/", // Define the URL for Groups
    Messages:"/",
    Pages:"/",
    Events:"/",
    Videos:"/",
    MarketPlace:"/",
  };

  return (
    <Box sx={{ display: "flex" }}>
      {/* Navbar Start */}
      <CssBaseline />
      <AppBar position="fixed" open={isOpen}  sx={{ backgroundColor: 'lightblue', boxShadow: 'none' }}>
        <Toolbar >
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={toggleSidebar}
            edge="start"
            sx={{ mr: 2, ...(isOpen && { display: "none" }) }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            FaceBuet
          </Typography>
          <Search>
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder="Search…"
              inputProps={{ 'aria-label': 'search' }}
            />
          </Search>
        </Toolbar>
      </AppBar>
      {/* Navbar end */}
      {/* Left Sidebar Start */}
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
        variant="persistent"
        anchor="left"
        open={isOpen}
      >
        <DrawerHeader >
          <IconButton onClick={toggleSidebar}>
            {theme.direction === "ltr" ? (
              <ChevronLeftIcon />
            ) : (
              <ChevronRightIcon />
            )}
          </IconButton>
        </DrawerHeader>
        <Divider />
        <List>
          {Object.entries(linksLeft).map(([text, url]) => {
            let iconComponent = null;

            if (text === "Feed") {
              iconComponent = <GroupIcon />;
            } else if (text === "Friends") {
              iconComponent = <GroupIcon />;
            } else if (text === "Requests") {
              iconComponent = <Diversity3Icon />;
            } else if (text === "Groups") {
              iconComponent = <Diversity3Icon />;
            }
            else if(text=="Messages"){
              iconComponent=<MessageIcon/>
            }
            else if(text=="Pages"){
              iconComponent=<EmojiFlagsIcon/>
            }
            else if(text=="Events"){
              iconComponent=<EventIcon/>
            }
            else if(text=="Videos"){
              iconComponent=<OndemandVideoIcon/>
            }
            else if(text=="MarketPlace"){
              iconComponent=<StorefrontIcon/>
            }


            // Wrap ListItemButton with Link
            return (
              <ListItem key={text} disablePadding>
                <Link
                  // to={url}
                  style={{ textDecoration: "none", color: "inherit" }}
                  onClick={() => setCurrentComponent(text)}
                >
                  {" "}
                  {/* Use the URL associated with each text */}
                  <ListItemButton>
                    <ListItemIcon>{iconComponent}</ListItemIcon>
                    <ListItemText primary={text} />
                  </ListItemButton>
                </Link>
              </ListItem>
            );
          })}
        </List>

        <Divider />
        <List>
          {["All mail", "Trash", "Spam"].map((text, index) => (
            <ListItem key={text} disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Drawer>
      {/* Left Sidebar End */}
    </Box>
  );
}
