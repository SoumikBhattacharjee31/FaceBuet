import React, { useState } from "react";
import axios from 'axios';
export default function Register(props) {
  const [formData, setFormData] = useState({
    user_name: "",
    mobile: "",
    profile_pic: "",
    cover_photo: "",
    password: "",
    birth_date: "",
  });
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

 

  return (
    <div className="register-form" align="center">
      <h2>Registration Form</h2>
      <form >
        <input
          type="text"
          name="user_name"
          placeholder="User Name"
          value={formData.user_name}
          onChange={handleInputChange}
        />{" "}
        <br />
        <input
          type="text"
          name="mobile"
          placeholder="Mobile No"
          value={formData.mobile}
          onChange={handleInputChange}
        />
        <br />
        <input
          type="text"
          name="profile_pic"
          placeholder="profile_pic"
          value={formData.profile_pic}
          onChange={handleInputChange}
        />
        <br />
        <input
          type="text"
          name="cover_photo"
          placeholder="cover_photo"
          value={formData.cover_photo}
          onChange={handleInputChange}
        />
        <br />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleInputChange}
        />{" "}
        <br />
        <div>
          <button>Birth Date</button>{" "}
          <input
            type="date"
            name="birth_date"
            placeholder="Birth Date"
            value={formData.birth_date}
            onChange={handleInputChange}
          />
        </div>
        <br />
        <button type="submit" onSubmit={()=>{
          props.handleSubmit(formData)
        }}>Submit</button>
      </form>
    </div>
  );
}

// import React from "react";
// import App from "../App";

// export default function Register(props) {
//   return (
//     <form action="register" method="post" align="center">
//       <input type="text" name="first_name" placeholder="First Name "/>
//       <br />
//       <input type="text" name="last_name" placeholder="Last Name" /> <br />
//       <input type="text" name="user_name" placeholder="User Name" />
//       <br />
//       <input type="text" name="mobile" placeholder="Mobile No" /> <br />
//       <input type="text" name="profile_pic" placeholder="profile_pic" /> <br />
//       <input type="text" name="cover_photo" placeholder="cover_photo" /> <br />

//       <input type="password" name="password1" placeholder="Password" /> <br />
//       <input
//         type="password"
//         name="password2"
//         placeholder="Confirm Password"
//       />{" "}
//       <br />
//      <button>Birth Date </button> <input type="date" name="Birth Date" placeholder="Birth Date" /><br />
//       <input type="Submit" />
//     </form>
//   );
// }
