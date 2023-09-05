import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import CommentCard from "../components/CommentCard";
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

export default function Comments({open, setCurrentComponent, post_id}) {
  const [data, setData] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const buttonStyle = {
    width: '400px',  // Adjust the width as needed
    height: '50px', // Adjust the height as needed
  };

  React.useEffect(() => {
    const response = axios
      .post("http://localhost:8000/api/get_comment_info/", { post_id: post_id }, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then (response => {
        setData(response.data);
        console.log(response.data)
        setIsLoading(false);
      })
  }, []);

  return (
    <Box sx={{ display: "flex" }}>
      {/* <Main open={open}> */}
        <DrawerHeader />
        {isLoading ? (
          <></>
        ) : (
          data.map((postData, index) => (
            <CommentCard key={index} postData={postData} />
          ))
        )}
      {/* </Main> */}
    </Box>
  );
};


