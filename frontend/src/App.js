import { useEffect, useState } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import Register from "./components/Register";
import Profile from "./components/Profile"

// import {
//   BrowserRouter as Router,
//   Route
// } from "react-router-dom"

function App() {
  const [data, setData] = useState([]);

let [userList, setUserList] = useState();

  useEffect(() => {
    getUsers();
  },[]);

  let getUsers = async () => {
    try {
      const response = await fetch('/api/users/');
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const jsonData = await response.json();
      // console.log(jsonData)
      setData(jsonData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
   
  
  
  const addUser = (user_name,mobile_number,profile_pic,cover_photo,birth_date) => {
    let newUserList = [...userList];
    //  let NewTotalQuantity=totalQuantity;
    newUserList.push({
     user_id:0,
     user_name:user_name,
     mobile_number:mobile_number,
     profile_pic:profile_pic,
     cover_photo:cover_photo,
     birth_date:birth_date,
});
   
    setUserList(newUserList);
  };
  // console.log(data)

  return (
    // <Router>
      <div className="App">
        <Navbar />
        <Register /*props={handleSubmit}*//>
        <div className="userdata">
          {
            data.map((datum,index)=>
              // <h3 key={index}>{datum.birth_date}</h3>
              <Profile key={index} data={datum}/>
              // <Route path="/" exact component={<Profile key={index} data={datum}/>}/>
            )
          }
        </div>
      </div>
    // </Router>
  );
}

export default App;
