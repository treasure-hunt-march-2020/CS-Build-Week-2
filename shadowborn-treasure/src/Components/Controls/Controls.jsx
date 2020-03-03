import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Link, withRouter } from "react-router-dom";

import Spinner from '../Spinner/Spinner';

// import Button from '@material-ui/core/Button';

import axios from 'axios';

const initalState = {
    
};

const Controls = (props) => {
    console.log("Controls Props",props)
    const [direction, setDirection] = useState({ initalState });
    const [loading, setLoading] = useState([true])

    const AuthString = process.env.REACT_APP_JAMES_API_KEY

    const north = '{"direction":"n"}'
    const south = '{"direction":"s"}'
    const east = '{"direction":"e"}'
    const west = '{"direction":"w"}'

    const moveNorth = () => {

        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', north, {
                headers: { Authorization: AuthString}
            }
        ).then((res) => {
            console.log('Moved North', res)
            console.log(props)
            setDirection([res.direction])
            console.log("Direction",direction)
            setTimeout((moveNorth) => {
                setLoading(false)
                props.history.push('/north')
            }, 17000);
            
        }).catch((err) => console.log(err));
    };
    const moveSouth = () => {

        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', south, {
                headers: { Authorization: AuthString}
            }
        ).then((res) => {
            console.log('Moved South', res)
            setDirection([res.direction])
            console.log("Direction",direction)
            setTimeout((moveSouth) => {
                setLoading(false)
                props.history.push("/south")
            }, 17000);
        }).catch((err) => console.log(err));
    };
    
    return (
        <Router>
            {((loading === true) ?
                <Spinner />
                        :
            <div className="all-cards rooms">
                <div><h2>{direction.messages}</h2></div>
                <div>
                    <button className="button-direction" onClick={moveNorth}>North</button>
                    <button className="button-direction">East</button>
                    <button className="button-direction" onClick={moveSouth}>South</button>
                    <button className="button-direction">West</button>
                </div>
            </div>
            )}
        </Router>
    );
}

export default withRouter(Controls);