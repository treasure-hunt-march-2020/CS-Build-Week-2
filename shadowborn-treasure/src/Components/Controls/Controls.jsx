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
    const [praying, setPraying] = useState([]);
    const [examine, setExamine] = useState([]);
    const [loading, setLoading] = useState([true])

    const AuthString = process.env.REACT_APP_JAMES_API_KEY

    const north = '{"direction":"n"}'
    const south = '{"direction":"s"}'
    const east = '{"direction":"e"}'
    const west = '{"direction":"w"}'
    const get_treasure = '{"name":"treasure"}'
    const confirm = '{"name":"treasure", "confirm":"yes"}'
    const prayer = '{"confirm":"yes"}'
    const examine_it = '{"name":"well"}'

    // const timeout = () => {
    //     setTimeout(() => {
    //         setLoading(false)
    //         window.location.reload(true);
    //     }, 17000);
    // }

    const moveNorth = () => {

        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/fly/', north, {
                headers: { Authorization: AuthString}
            }
        ).then((res) => {
            console.log('Moved North', res)
            setDirection([res.data.description])
            setTimeout((moveNorth) => {
                setLoading(false)
                window.location.reload(true);
            }, 17000);
            // timeout(moveNorth)
            
        }).catch((err) => console.log(err));
    };
    const moveSouth = () => {

        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/fly/', south, {
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
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/fly/', east, {
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
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/fly/', west, {
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
            setTimeout((confirm_sell) => {
                setLoading(false)
                window.location.reload(true);
            }, 17000);
        }).catch((err) => console.log(err));
    };
    
    
    const pray = () => {

        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/', prayer, {
                headers: { Authorization: AuthString}
            }
        ).then((res) => {
            console.log('Praying...', res)
            setPraying([res.data])
            setTimeout((pray) => {
                setLoading(false)
                window.location.reload(true);
            }, 17000);
        }).catch((err) => console.log(err));
    };


    const examining = () => {

        setLoading(true)
        axios
            .post('https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/', examine_it, {
                headers: { Authorization: AuthString}
            }
        ).then((res) => {
            setExamine([res.data])
            setTimeout((examining) => {
                setLoading(false)
                window.location.reload(true);
            }, 17000);
            console.log('Examination', res.data.description)
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
                <div><h2>{sellTreasure.messages}</h2></div>
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
                <div className="buttons">
                    <button className="button-direction pray" onClick={pray}>Pray</button>
                </div>
                <div className="buttons">
                    <button className="button-direction examine" onClick={examining}>Examine</button>
                </div>
            </div>
            )}
        </Router>
    );
}

export default withRouter(Controls);