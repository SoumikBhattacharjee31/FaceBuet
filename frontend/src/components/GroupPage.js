import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import GroupPageCard from "../components/GroupPageCard";
import Post from "../components/Post";
import axios from "axios";
import Button from "@mui/material/Button";
import SendIcon from '@mui/icons-material/Send';

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

export default function GroupPage({open, setCurrentComponent, groupId, setGroupId}) {
  const request_data = {group_id:groupId};
  const [data, setData] = React.useState([]);
  const [profilePosts, setProfilePosts] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);


  React.useEffect(() => {
    
    axios
      .post("http://localhost:8000/api/get_group_page/", request_data, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then (response => {
        setData(response.data);
        setIsLoading(false);
        console.log(response.data)
      })
  }, []);

  const handleButtonClick = () => {
    setGroupId(groupId)
    setCurrentComponent("creategrouppost")
  };

  return (
    <Box sx={{ display: "flex" }}>
      <Button 
      variant="contained" 
      endIcon={<SendIcon />}
      style={{
        position: 'fixed',
        bottom: '16px', // Adjust this value as needed
        right: '430px', // Adjust this value as needed
        zIndex: 100,
      }}
      onClick={handleButtonClick}
      >
        Send
      </Button>
      <Main open={open}>
        <DrawerHeader />
        {isLoading ? (
          <></>
        ) : 
            (
              <>
              <GroupPageCard postData={data.group_info} />
              { data.post_info?
                data.post_info.map((postData, index) => (
                  <Post key={index} postData={postData} />
                ))
                :<></>
              }
              </>
            
            
            )
        }
      </Main>
    </Box>
  );
};

