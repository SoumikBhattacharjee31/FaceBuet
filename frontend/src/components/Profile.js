import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import ProfileCard from "../components/ProfileCard";
import Post from "../components/Post";
import axios from "axios";
import Button from "@mui/material/Button";

const drawerWidth = 240;

const Main = styled("main", { shouldForwardProp: (prop) => prop !== "open" })(
  ({ theme, open }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create("margin", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: `-${drawerWidth}px`,
    ...(open && {
      transition: theme.transitions.create("margin", {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: 0,
    }),
  })
);

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: "flex-end",
}));

export default function Profile({open, setCurrentComponent, profileId}) {
  const [data, setData] = React.useState([]);
  const [profilePosts, setProfilePosts] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);

  React.useEffect(() => {
    
    axios
      .post("http://localhost:8000/api/get_user_profile/", {user_id:profileId}, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then (response => {
        setData(response.data);
        setIsLoading(false);
      })
  }, []);

  React.useEffect(() => {
    
    axios
      .post("http://localhost:8000/api/home/", {user_id:profileId}, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then (response => {
        setProfilePosts(response.data);
        setIsLoading(false);
      })
  }, []);

  return (
    <Box sx={{ display: "flex" }}>
      <Main open={open}>
        <DrawerHeader />
        {isLoading ? (
          <></>
        ) : 
            (
              <>
              <ProfileCard postData={data} />
              {
                profilePosts.map((postData, index) => (
                  <Post key={index} postData={postData} />
                ))
              }
              </>
            
            
            )
        }
      </Main>
    </Box>
  );
};


