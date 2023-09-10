import * as React from "react";
import IconButton from "@mui/material/IconButton";
import axios from "axios";

export default function Post({
  postData
}) {
  const [anchorE2, setAnchorE2] = React.useState(null);
  const [shareMenuOpen, setShareMenuOpen] = React.useState(false);
  const [reactions, setReactions] = React.useState({
    like: "👍",
    love: "❤️",
    fire: "🔥",
  });



  const handleReaction = async (reaction) => {
    try {
      const user_id = localStorage.getItem("user_id");

    const request_data={reaction:reaction,user_id:user_id,post_id:postData.post_id}
      const response = await axios.post(
        "http://localhost:8000/api/setPostReact/",
        request_data,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log(`User reacted with ${reaction}`);
      
      // Update the reactions state based on the response
      setReactions((prevReactions) => ({
        ...prevReactions,
        [reaction]: prevReactions[reaction] + 1,
      }));
    } catch (error) {
      console.error("Error reacting to post:", error);
    }
  };

  return (
    <>
        <IconButton
          aria-label="add to favorites"
          onClick={() => handleReaction("like")}
        >
          {reactions.like}
        </IconButton>
        <IconButton
          aria-label="love"
          onClick={() => handleReaction("love")}
        >
          {reactions.love}
        </IconButton>
        <IconButton
          aria-label="fire"
          onClick={() => handleReaction("fire")}
        >
          {reactions.fire}
        </IconButton>
        </>
  );
}