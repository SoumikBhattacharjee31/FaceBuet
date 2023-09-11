import * as React from "react";
import { styled } from "@mui/material/styles";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import { red } from "@mui/material/colors";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import GroupsIcon from '@mui/icons-material/Groups';


const cardStyles = {
  display: "flex",
  flexDirection: "column",
  // maxWidth: 1000, // Set the maximum width to make it moderately larger
  border: "2px solid #ccc",
  borderRadius: "10px",
};


export default function SearchGroupCard({postData, setCurrentComponent, setGroupId}) {
  const [expanded, setExpanded] = React.useState(false);
  console.log(postData)

  const gotoProfile = ()=>{
    setGroupId(postData.group_id)
    setCurrentComponent("GroupPage")
  }

  return (
    <Card sx={cardStyles}>
      <CardHeader
      onClick={gotoProfile}
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="post">
            {postData.media ? <img
              src={postData.media}
              alt="R"
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            ></img>:<GroupsIcon/>}
          </Avatar>
        }
        title={postData.group_name}
        subheader={postData.group_type}
      />
    </Card>
  );
}
