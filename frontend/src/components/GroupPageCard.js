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
import Comments from "./Comments";
import PostMenu from "./PostMenu";
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

const cardStyles = {
  display: "flex",
  flexDirection: "column",
  // maxWidth: 1000, // Set the maximum width to make it moderately larger
  border: "2px solid #ccc",
  borderRadius: "10px",
};

const mediaStyles = {
  flex: "1",
  objectFit: "cover",
};

export default function Post({open, setCurrentComponent, postData, setUpdatePostId}) {
  // const postData = props.postData;
  const [data, setData] = React.useState("");

  React.useEffect(() => {
    
    axios
      .post("http://localhost:8000/api/is_in_group/", {user_id:localStorage.getItem('user_id'),group_id:postData.group_id}, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then (response => {
        setData(response.data.status);
      })
  }, []);

  // const handleDiswon = () => {
  //   axios
  //     .post("http://localhost:8000/api/delete_user/", {user_id:localStorage.getItem('user_id')}, {
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //     })
  // };

  const handleDelete = () => {
    axios
      .post("http://localhost:8000/api/delete_group/", {group_id:postData.group_id}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
  };

  const handleLeave = () => {
    axios
      .post("http://localhost:8000/api/leave_from_group/", {user_id:localStorage.getItem('user_id'),group_id:postData.group_id}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
  };

  const handleUnsend = () => {
    axios
      .post("http://localhost:8000/api/reject_req_in_group/", {user_id:localStorage.getItem('user_id'),group_id:postData.group_id}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
  };

  const handleJoin = () => {
    axios
      .post("http://localhost:8000/api/send_req_in_group/", {user_id:localStorage.getItem('user_id'), group_id:postData.group_id}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
  };
  const showRequestList = () => {
    setCurrentComponent("groupreq")
  };

  return (
    <Card sx={cardStyles}>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="post">
            <img
              src={postData.media}
              alt="R"
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            ></img>
          </Avatar>
        }
        action={
          <IconButton aria-label="settings">
            <MoreVertIcon />
          </IconButton>
        //   <PostMenu setCurrentComponent={setCurrentComponent} setUpdatePostId={setUpdatePostId} post_id={postData.post_id}/>
        }
        title={postData.group_name}
        subheader={postData.member_count}
      />
      <CardMedia
        component="img"
        image={postData.media?postData.media[0]:""}
        alt="Paella dish"
        sx={mediaStyles}
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {postData.description}
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        {/* {data === "owner"  && <Button variant="contained" onClick={handleDiswon}>Disown Group</Button>} */}
        {data === "owner"  && <Button variant="contained" onClick={handleDelete}>Delete Group</Button>}
        {data === "owner"  && <Button variant="contained" onClick={showRequestList}>Requests</Button>}
        {data === "member"  && <Button variant="contained" onClick={handleLeave}>Leave Group</Button>}
        {data === "requested"  && <Button variant="contained" onClick={handleUnsend}>Unsend Request</Button>}
        {data === "none"  && <Button variant="contained" onClick={handleJoin}>Join Group</Button>}

      </CardActions>
    </Card>
  );
}
