import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

// import Button from '@material-ui/core/Button';

import axios from 'axios';

import Spinner from '../Spinner/Spinner';

function Home(props) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState([true])

  useEffect(() => {

    setLoading(true)
    let isSubscribed = true;

    const AuthString = 'Token e8b177670f8c40271da9db9ca11736808cf614c5'
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
            <div className="card room" key={item.room_id} onClick={() => props.history.push(item.room_id)}>
              {/* <a href={item.name}>{item.name}</a> */}
              <h1 className="room-name">{item.title}</h1>
              <h4 className="room-type">You are at {item.coordinates} coordinates, the elevation is {item.elevation} and the terrain is {item.terrain}</h4>
              <p>{item.description}</p>
            </div>
          ))}
        </div>
      )}
    </Router>
  );
}

export default Home;