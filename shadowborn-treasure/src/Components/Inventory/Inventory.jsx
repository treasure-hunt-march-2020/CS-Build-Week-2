import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

// import Button from '@material-ui/core/Button';

import axios from 'axios';

import Spinner from '../Spinner/Spinner';

import Controls from '../Controls/Controls'

function Inventory(props) {

    useEffect(() => {

        const AuthString = process.env.REACT_APP_JAMES_API_KEY

        axios.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', { headers: { Authorization: AuthString } }
        ).then(result => {
            console.log(result)
        }).catch(error => {
            console.log(error)
        })

    }, []);

    return (
        <div>
            <h6>Possible exits</h6>
            <div className="exits">
                Hello
            </div>
        </div>
    )
}

export default Inventory;