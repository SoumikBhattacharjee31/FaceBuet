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

export default function PageCard({postData, setCurrentComponent, setGroupId}) {
  const [expanded, setExpanded] = React.useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const gotoGroup = ()=>{
    setGroupId(postData.group_id)
    setCurrentComponent("GroupPage")
  }

  return (
    <Card sx={{Width: 500, border: "2px solid #ccc", borderRadius: "10px" }}>
      <CardHeader
        onClick={gotoGroup}
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="post">
            {/* <img src={postData.media[0]} alt="R"></img> */}
            <img src={postData.media[0]} alt="R" style={{ width: '100%', height: '100%', objectFit: 'cover' }}></img>
          </Avatar>
        }
        title={postData.group_name}
        subheader={postData.init_time}
        // subheader="August 21 , 2023"
      />
      <CardMedia
      onClick={gotoGroup}
        component="img"
        height="194"
        image={postData.media[0]}
        alt="Paella dish"
      />
      <CardContent onClick={gotoGroup}>
        <Typography variant="body2" color="text.secondary">
          {postData.description}
        </Typography>
      </CardContent>
    </Card>
  );
}