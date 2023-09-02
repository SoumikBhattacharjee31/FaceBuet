import { useState } from "react";
import * as React from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import IconButton from "@mui/material/IconButton";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import InputAdornment from "@mui/material/InputAdornment";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Copyright(props) {
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      align="center"
      {...props}
    >
      {"Copyright © "}
      <Link color="inherit" href="https://mui.com/">
        Your Website
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}

const defaultTheme = createTheme();

function SignUp() {
  const [profilePic, setProfilePic] = useState(null);
  const [coverPhoto, setCoverPhoto] = useState(null);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate(); 

  const handleProfilePicChange = (e) => {
    const file = e.target.files[0];
    setProfilePic(file);
  };
  const handleCoverPhotoChange = (e) => {
    const file = e.target.files[0];
    setCoverPhoto(file);
  };

  const [formData, setFormData] = useState({
    user_name: "",
    mobile: "",

    password: "",
    birth_date: "",
    email: "",
  });
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try{
      const request_data = new FormData();
      for (const key in formData) {
        request_data.append(key, formData[key]);
      }
      request_data.append("profile_pic", profilePic);
      request_data.append("cover_photo", coverPhoto);
      console.log(request_data);
      const response = await axios
        .post("http://localhost:8000/api/addusers/", request_data, {
          headers: {
            "Content-Type": "multipart/form-data",
            // "X-CSRFToken": csrfToken,
          },
        })
        if ('error' in response.data){console.log(response.data.error);}
        else {navigate("/routes/SignIn");}
      } catch (error) {console.log(error);}
    };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign up
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
            sx={{ mt: 3 }}
          >
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete="given-name"
                  name="user_name"
                  required
                  fullWidth
                  id="user_name"
                  label="User Name"
                  value={formData.user_name}
                  onChange={handleInputChange}
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="mobile"
                  label="Mobile No."
                  name="mobile"
                  value={formData.mobile}
                  onChange={handleInputChange}
                  autoComplete="family-name"
                />
              </Grid>
              <Grid item xs={12}>
                <label htmlFor="profile-pic-input">Profile Picture</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleProfilePicChange}
                  style={{ marginBottom: "10px" }}
                />
                {profilePic && (
                  <div>
                    <p>Selected Image: {profilePic.name}</p>
                    <img
                      src={URL.createObjectURL(profilePic)}
                      alt="Selected"
                      // {...URL.createObjectURL(profilePic)}
                      style={{ maxWidth: "100%", marginBottom: "10px" }}
                    />
                  </div>
                )}
                
              </Grid>
              <Grid item xs={12}>
                <label htmlFor="cover-photo-input">Cover Photo</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleCoverPhotoChange}
                  style={{ marginBottom: "10px" }}
                />
                {coverPhoto && (
                  <div>
                    <p>Selected Image: {coverPhoto.name}</p>
                    <img
                      src={URL.createObjectURL(coverPhoto)}
                      // {...URL.createObjectURL(coverPhoto)}
                      alt="Selected"
                      style={{ maxWidth: "100%", marginBottom: "10px" }}
                    />
                  </div>
                )}
              </Grid>

              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type={showPassword ? "text" : "password"}
                  id="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  autoComplete="new-password"
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          onClick={() => setShowPassword(!showPassword)}
                          edge="end"
                        >
                          {showPassword ? <Visibility /> : <VisibilityOff />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="birth_date"
                  label="Birth Date"
                  name="birth_date"
                  type="date"
                  value={formData.birth_date}
                  onChange={handleInputChange}
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Grid>
              <Grid>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  value={formData.email}
                  autoComplete="email"
                  onChange={handleInputChange}
                  autoFocus
                />
              </Grid>

              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Checkbox value="allowExtraEmails" color="primary" />
                  }
                  label="I want to receive inspiration, marketing promotions and updates via email."
                />
              </Grid>
            </Grid>
            {/* <div> */}
              {/* <a
                href="/routes/SignIn"
                style={{ textDecoration: "none", color: "inherit" }}
              > */}
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
                >
                    Sign Up
                </Button>
              {/* </a> */}
            {/* </div> */}
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="/routes/SignIn" variant="body2">
                  Already have an account? Sign in
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
        <Copyright sx={{ mt: 5 }} />
      </Container>
    </ThemeProvider>
  );
}

export default function Root() {
  return <SignUp />;
}
