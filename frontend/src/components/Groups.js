import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Post from "./Post";
import axios from "axios";
import Button from "@mui/material/Button";
import GroupCard from "./GroupCard";
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';
import Stack from '@mui/material/Stack';

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

export default function Groups({ open, setCurrentComponent }) {
  const fetched_user_id = localStorage.getItem("user_id");
  const request_data = { user_id: fetched_user_id, group_type: "group" };
  const [data, setData] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  React.useEffect(() => {
    const response = axios
      .post("http://localhost:8000/api/get_groups/", request_data, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        setData(response.data);
        setIsLoading(false);
      });
  }, []);
  const handleButtonClick = () => {
    setCurrentComponent("creategroup")
  };

  return (
    <Box sx={{ position: 'relative', display: 'flex' }}>
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
        ) : (
          data.not_in_group.map((postData, index) => (
            <GroupCard key={index} postData={postData} />
          ))
        )}
        {isLoading ? (
          <></>
        ) : (
          data.member_in_group.map((postData, index) => (
            <GroupCard key={index} postData={postData} />
          ))
        )}
        {isLoading ? (
          <></>
        ) : (
          data.owner_in_group.map((postData, index) => (
            <GroupCard key={index} postData={postData} />
          ))
        )}
      </Main>
    </Box>
  );
}
