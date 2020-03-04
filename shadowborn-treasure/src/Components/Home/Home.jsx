import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

import './home.scss';

import axios from 'axios';

import Spinner from '../Spinner/Spinner';

import Controls from '../Controls/Controls'

function Home(props) {
    
//   console.log("Home Props",props)
  
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState([true])

  useEffect(() => {

    setLoading(true)
    let isSubscribed = true;

    const AuthString = process.env.REACT_APP_JAMES_API_KEY

    axios.get(
      'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/',{ headers: { Authorization: AuthString } }
    ).then(result => {
      setLoading(false)
      console.log(result.data)
      if (isSubscribed) {
        setData([result.data])
      }
    }).catch(error => {
      console.log(error)
    })

    return () => isSubscribed = false

  }, []);

  return (
    <Router>
      {((loading === true) ?
        <Spinner />
        :
        <div className="all-cards rooms">
          {data.map(item => (
            <div className="card room" key={item.room_id}>
            {/* <div className="card room" key={item.room_id} onClick={() => props.history.push(item.room_id)}> */}
              {/* <a href={item.name}>{item.name}</a> */}
              <h1 className="room-name">{item.title}</h1>
              <h6 className="room-type">You are at {item.coordinates} coordinates, the elevation is {item.elevation} and the terrain is {item.terrain}</h6>
              <p>{item.description}</p>
              <p>Items: {item.items}</p>
              <h6>Possible exits</h6>
              <div className="exit-container">
                  
                  <div className="exits"> 
                    {item.exits[0]}</div>
                    <div className="exits"> 
                    {item.exits[1]}</div>
                    <div className="exits"> 
                    {item.exits[2]}</div>
                    <div className="exits"> 
                    {item.exits[3]}</div>
              </div>
              <Controls />
            </div>
          ))}
          {console.log("Home", props)}
        </div>
      )}
    </Router>
  );
}

export default Home;