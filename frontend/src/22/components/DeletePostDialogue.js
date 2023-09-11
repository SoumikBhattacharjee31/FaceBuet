import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import axios from "axios";

export default function DeletePostDialogue({post_id}) {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };
  const handleDelete = async () => {
    setOpen(false);
    try{
        const response = await axios
          .post("http://localhost:8000/api/delete_user_post/", {post_id:post_id}, {
            headers: {
              "Content-Type": "application/json",
            },
          })
          if ('error' in response.data){console.log(response.data.error);}
        //   else {setCurrentComponent('feed')}
        } catch (error) {console.log(error);}
  };

  return (
    <div>
      <Button variant="outlined" onClick={handleClickOpen}>
        Delete Post
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {"Are you sure about deleting this post?"}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            You will not be able to recover this post once you click on the Agree button.
            Are you sure to want to continue?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>No</Button>
          <Button onClick={handleDelete} autoFocus>
            Yes
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}