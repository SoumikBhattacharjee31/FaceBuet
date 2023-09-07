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
  const fetched_user_id = profileId
  const request_data = {user_id:fetched_user_id};
  const [data, setData] = React.useState([]);
  const [profilePosts, setProfilePosts] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const buttonStyle = {
    width: '400px',  // Adjust the width as needed
    height: '50px', // Adjust the height as needed
  };

  React.useEffect(() => {
    
    axios
      .post("http://localhost:8000/api/get_user_profile/", request_data, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then (response => {
        setData(response.data);
        setIsLoading(false);
        console.log(response.data)
      })
  }, []);

  React.useEffect(() => {
    
    axios
      .post("http://localhost:8000/api/home/", request_data, {
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


