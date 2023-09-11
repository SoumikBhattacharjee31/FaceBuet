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
import Button from "@mui/material/Button";
import { red } from "@mui/material/colors";
import FavoriteIcon from "@mui/icons-material/Favorite";
import ShareIcon from "@mui/icons-material/Share";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import axios from "axios";
import PersonIcon from '@mui/icons-material/Person';

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

export default function ProfileCard({postData}) {
  const [data, setData] = React.useState("");

  React.useEffect(() => {
    console.log(localStorage.getItem('user_id'));
    axios
      .post("http://localhost:8000/api/is_friend/", {user_id:(localStorage.getItem('user_id')),friend_id:(postData.user_id)}, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then (response => {
        setData(response.data.status);
        console.log(response.data.status)
      })
  }, []);


  const handleDeleteUser = () => {
    axios
      .post("http://localhost:8000/api/delete_user/", {user_id:localStorage.getItem('user_id')}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
  };
  const handleUnfriendUser = () => {
    axios
      .post("http://localhost:8000/api/unfriend/", {user_id:localStorage.getItem('user_id'),friend_id:postData.user_id}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
  };
  const handleRemoveRequest = () => {
    axios
      .post("http://localhost:8000/api/delete_request/", {user_id:localStorage.getItem('user_id'),friend_id:postData.user_id}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
  };
  const handleSendRequest = () => {
    axios
      .post("http://localhost:8000/api/send_request/", {user_id:localStorage.getItem('user_id'),friend_id:postData.user_id}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
  };
  const handleAcceptRequest = () => {
    axios
      .post("http://localhost:8000/api/accept_request/", {user_id:localStorage.getItem('user_id'),friend_id:postData.user_id}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
  };
  

  return (
    <Card sx={{Width: 500, border: "2px solid #ccc", borderRadius: "10px" }}>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="post">
            {/* <img src={postData.media[0]} alt="R"></img> */}
            {postData.profile_pic ? <img src={postData.profile_pic[0]} alt="R" style={{ width: '100%', height: '100%', objectFit: 'cover' }}></img>:<PersonIcon/>}
          </Avatar>
        }
        action={
          <IconButton aria-label="settings">
            <MoreVertIcon />
          </IconButton>
        }
        title={postData.user_name}
        subheader={postData.friend_count}
        // subheader="August 21 , 2023"
      />
      {postData.cover_photo && <CardMedia
        component="img"
        height="194"
        image={postData.cover_photo[0]}
        alt="Paella dish"
      />}
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {/* {postData.description} */}
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        {data === "own"  && <Button variant="contained" onClick={handleDeleteUser}>Delete Account</Button>}
        {data === "friend"  && <Button variant="contained" onClick={handleUnfriendUser}>Unfriend</Button>}
        {data === "sent"  && <Button variant="contained" onClick={handleRemoveRequest}>Unsend Request</Button>}
        {data === "received"  && <Button variant="contained" onClick={handleRemoveRequest}>Reject Request</Button>}
        {data === "received"  && <Button variant="contained" onClick={handleAcceptRequest}>Accept Request</Button>}
        {data === "none"  && <Button variant="contained" onClick={handleSendRequest}>Send Request</Button>}
      </CardActions>
    </Card>
  );
}
