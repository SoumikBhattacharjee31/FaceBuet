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

export default function SearchCard({postData, setCurrentComponent, setProfileId}) {
  const [expanded, setExpanded] = React.useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const gotoProfile = ()=>{
    setProfileId(postData.user_id)
    console.log('hello')
    console.log(postData.user_id)
    setCurrentComponent("Profile")
  }

  return (
    <Card sx={cardStyles}>
      <CardHeader
      onClick={gotoProfile}
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="post">
            {postData.profile_pic ? <img
              src={postData.profile_pic}
              alt="R"
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            ></img> : <PersonIcon/>}
          </Avatar>
        }
        title={postData.user_name}
        subheader='User'
      />
      {/* <CardMedia
        component="img"
        image={postData.profile_pic[0]}
        alt="Paella dish"
        sx={mediaStyles}
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {postData.description}
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <IconButton aria-label="add to favorites">
          <FavoriteIcon />
        </IconButton>
        <IconButton aria-label="share">
          <ShareIcon />
        </IconButton>
        <ExpandMore
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <ExpandMoreIcon />
        </ExpandMore>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          <Typography paragraph></Typography>
        </CardContent>
      </Collapse> */}
    </Card>
  );
}