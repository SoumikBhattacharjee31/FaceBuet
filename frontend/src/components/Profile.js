import React from "react";
import styled from "styled-components";

const Card = styled.div`
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  margin: 20px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  background-color: white;
`;

const UserInfo = styled.div`
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #ccc;
`;

function Profile (userdata) {
  return (
    <Card>
      <h3>User Profile</h3>
      <UserInfo>
        <p>ID: {userdata.data.user_id}</p>
        <p>Birth Date: {userdata.data.birth_date}</p>
        <p>Username: {userdata.data.user_name}</p>
        <p>Password: {userdata.data.password}</p>
        <p>Mobile Number: {userdata.data.mobile_number}</p>
        <p>Profile Picture: {userdata.data.profile_pic}</p>
        <p>Cover Photo: {userdata.data.cover_photo}</p>
      </UserInfo>
    </Card>
  );
};

export default Profile;








// import React from 'react'
// export default function Profile(userdata){
//     return (
//         <div>
//             <h3>{userdata.data.user_id}</h3>
//             <h3>{userdata.data.birth_date}</h3>
//             <h3>{userdata.data.user_name}</h3>
//             <h3>{userdata.data.password}</h3>
//             <h3>{userdata.data.mobile_number}</h3>
//             <h3>{userdata.data.profile_pic}</h3>
//             <h3>{userdata.data.cover_photo}</h3>
//             <h3>{userdata.data.birth_date}</h3>
//         </div>
//     )
// }
