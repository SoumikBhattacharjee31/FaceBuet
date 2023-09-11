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
import Replies from "./Replies";


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
  // maxWidth: 500, // Set the maximum width to make it moderately larger
  border: "2px solid #ccc",
  borderRadius: "10px",
};

const mediaStyles = {
  flex: "1",
  objectFit: "cover",
};

export default function CommentCard({commentData, open, setCurrentComponent}) {
  const [expanded, setExpanded] = React.useState(false);

  const handleExpandClick = async () => {
    setExpanded(!expanded);
  };

  return (
    <Card sx={cardStyles}>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="post">
            {commentData.profile_pic && <img
              src={commentData.profile_pic}
              alt="R"
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            ></img>}
          </Avatar>
        }
        title={commentData.user_name}
        subheader={commentData.init_time}
      />
      {commentData.media[0] && <CardMedia
        component="img"
        image={commentData.media[0]}
        alt="Paella dish"
        sx={mediaStyles}
      />}
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {commentData.description}
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <ExpandMore
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <ExpandMoreIcon />
          Replies
        </ExpandMore>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          {/* <Typography paragraph></Typography> */}
          <Replies comment_id={commentData.comment_id} open = {open} setCurrentComponent={setCurrentComponent}/>
        </CardContent>
      </Collapse>
    </Card>
  );
}
