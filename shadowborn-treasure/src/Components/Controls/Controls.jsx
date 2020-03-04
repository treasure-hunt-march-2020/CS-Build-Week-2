import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Link, withRouter } from "react-router-dom";

import Spinner from '../Spinner/Spinner';

import './controls.scss';

import axios from 'axios';

const Controls = (props) => {
    console.log("Controls Props",props)
    const [direction, setDirection] = useState([]);
    const [treasure, setTreasure] = useState([]);
    const [sellTreasure, setSellTreasure] = useState([]);
    const [loading, setLoading] = useState([true])

    const AuthString = process.env.REACT_APP_JAMES_API_KEY

    const north = '{"direction":"n"}'
    const south = '{"direction":"s"}'
    const east = '{"direction":"e"}'
    const west = '{"direction":"w"}'
    const get_treasure = '{"name":"treasure"}'
    const confirm = '{"name":"treasure", "confirm":"yes"}'

    const moveNorth = () => {

        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', north, {
                headers: { Authorization: AuthString}
            }
        ).then((res) => {
            console.log('Moved North', res)
            setDirection([res.data.description])
            setTimeout((moveNorth) => {
                setLoading(false)
                window.location.reload(true);
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
            setDirection([res.data.description])
            console.log('Direction',direction)
            setTimeout((moveSouth) => {
                setLoading(false)
                window.location.reload(true);
            }, 17000);
        }).catch((err) => console.log(err));
    };
    const moveEast = () => {

        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', east, {
                headers: { Authorization: AuthString}
            }
        ).then((res) => {
            console.log('Moved East', res)
            setDirection([res.data.description])
            console.log('Direction',direction)
            setTimeout((moveEast) => {
                setLoading(false)
                window.location.reload(true);
            }, 17000);
        }).catch((err) => console.log(err));
    };
    const moveWest = () => {

        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', west, {
                headers: { Authorization: AuthString}
            }
        ).then((res) => {
            console.log('Moved West', res)
            setDirection([res.data.description])
            console.log('Direction',direction)
            setTimeout((moveWest) => {
                setLoading(false)
                window.location.reload(true);
            }, 17000);
        }).catch((err) => console.log(err));
    };


    const pickup_treasure = () => {
        
        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', get_treasure, {
                headers: { Authorization: AuthString}
            }
        ).then((res) => {
            console.log('Picked up Treasure', res)
            setTreasure([res.data])
            setTimeout((pickup_treasure) => {
                setLoading(false)
                window.location.reload(true);
            }, 17000);
        }).catch((err) => console.log(err));
    };

    const sell_treasure = () => {

        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', get_treasure, {
                headers: { Authorization: AuthString}
            }
        ).then((res) => {
            console.log('Sell Treasure', res)
            setSellTreasure([res.data])
            setTimeout((sell_treasure) => {
                setLoading(false)
                window.location.reload(true);
            }, 17000);
        }).catch((err) => console.log(err));
    };

    const confirm_sell = () => {

        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', confirm, {
                headers: { Authorization: AuthString}
            }
        ).then((res) => {
            console.log('Confirm Sell', res)
            setSellTreasure([res.data])
            setTimeout((pickup_treasure) => {
                setLoading(false)
                window.location.reload(true);
            }, 17000);
        }).catch((err) => console.log(err));
    };
    
    return (
        <Router>
            {console.log('Direction',direction)}
            {((loading === true) ?
                <Spinner />
                        :
            <div className="all-cards rooms">
                <div><h2>{direction.messages}</h2></div>
                <div className="buttons">
                    <button className="button-direction" onClick={moveNorth}>North</button>
                    <button className="button-direction"onClick={moveEast}>East</button>
                    <button className="button-direction" onClick={moveSouth}>South</button>
                    <button className="button-direction"onClick={moveWest}>West</button>
                </div>
                <div className="buttons">
                    <button className="button-direction treasure" onClick={pickup_treasure}>Pickup Treasure</button>
                </div>
                <div className="buttons">
                    <button className="button-direction treasure" onClick={sell_treasure}>Sell Treasure</button>
                </div>
                <div className="buttons">
                    <button className="button-direction treasure" onClick={confirm_sell}>Confirm</button>
                </div>
            </div>
            )}
        </Router>
    );
}

export default withRouter(Controls);