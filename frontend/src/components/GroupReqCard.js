import * as React from "react";
import { styled } from "@mui/material/styles";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Collapse from "@mui/material/Collapse";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import { red } from "@mui/material/colors";
import FavoriteIcon from "@mui/icons-material/Favorite";
import ShareIcon from "@mui/icons-material/Share";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import axios from "axios";
import Button from "@mui/material/Button";

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? "rotate(0deg)" : "rotate(180deg)",
  marginLeft: "auto",
  transition: theme.transitions.create("transform", {
    duration: theme.transitions.duration.shortest,
  }),
}));

export default function GroupReqCard({postData, setCurrentComponent, setProfileId, profileId, groupId}) {



  const gotoProfile = ()=>{
    setProfileId(postData.user_id)
    setCurrentComponent("Profile")
  }
  const handleAccept = ()=>{
    axios
      .post("http://localhost:8000/api/accept_req_in_group/", {user_id:postData.user_id,group_id:groupId}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
  }
  const handleReject = ()=>{
    axios
      .post("http://localhost:8000/api/reject_req_in_group/", {user_id:postData.user_id,group_id:groupId}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
  }

  return (
    <Card sx={{Width: 500, border: "2px solid #ccc", borderRadius: "10px" }}>
      <CardHeader
      onClick={gotoProfile}
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="post">
            {/* <img src={postData.media[0]} alt="R"></img> */}
            <img src={postData.media} alt="R" style={{ width: '100%', height: '100%', objectFit: 'cover' }}></img>
          </Avatar>
        }
        action={
          <IconButton aria-label="settings">
            <MoreVertIcon />
          </IconButton>
        }
        title={postData.user_name}
        // subheader={postData.init_time}
        // subheader="August 21 , 2023"
      />
      <CardActions disableSpacing>
      <Button variant="contained" onClick={handleAccept}>Accept</Button>
      <Button variant="contained" onClick={handleReject}>Reject</Button>
      </CardActions>
    </Card>
  );
}
