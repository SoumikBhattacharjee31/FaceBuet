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
import PostReactionMenu from "./PostReactionMenu";

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
  console.log(postData);
  // const postData = props.postData;
  const [expanded, setExpanded] = React.useState(false);
  const [commentInfo, setCommentInfo] = React.useState([]);

  const handleExpandClick = async () => {
    setExpanded(!expanded);
  };

  return (
    <Card sx={cardStyles}>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="post">
            {postData.profile_pic && <img
              src={postData.profile_pic}
              alt="R"
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            ></img>}
          </Avatar>
        }
        action={
          localStorage.getItem('user_id')==postData.user_id && <PostMenu setCurrentComponent={setCurrentComponent} setUpdatePostId={setUpdatePostId} post_id={postData.post_id}/>
        }
        title={postData.user_name}
        // subheader={`${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}:${String(date.getSeconds()).padStart(2, '0')}`}
        // subheader={Date(postData.init_time).toLocaleString()}
        subheader={Date(postData.init_time)}
        // subheader={postData.init_time}
      />
      {postData.media[0] && <CardMedia
        component="img"
        image={postData.media[0]}
        alt="Paella dish"
        sx={mediaStyles}
      />}
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {postData.description}
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <PostReactionMenu postData={postData}/>
        <ExpandMore
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <ExpandMoreIcon />
          Comments
        </ExpandMore>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          {/* <Typography paragraph> */}
            <Comments post_id={postData.post_id} open = {open} setCurrentComponent={setCurrentComponent}/>
          {/* </Typography> */}
        </CardContent>
      </Collapse>
    </Card>
  );
}
