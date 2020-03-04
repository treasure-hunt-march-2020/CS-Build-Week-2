import React, { useState, useEffect } from 'react';

import './inventory.scss';

import axios from 'axios';

function Inventory(props) {
    const [inventory, setInventory] = useState([]);

    const inv = []
    
    useEffect(() => {

        const AuthString = process.env.REACT_APP_JAMES_API_KEY

        axios.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', inv, {
                headers: { Authorization: AuthString}
            }
        ).then(result => {
            console.log('Moved North', result)
            setInventory([result.data])
            console.log("Inventory result",result.data)
        }).catch(error => {
            console.log(error)
        })

    }, []);

    return (
        <div className="inventory-container">
            
            {inventory.map(item => (
            <div className="inventory-card" key={item.name}>
              <h6>NAME: {item.name}</h6>
              <h6>ENCUMBRANCE: {item.encumbrance}</h6>
              <h6>STRENGTH: {item.strength}</h6>
              <h6>SPEED: {item.speed}</h6>
              <h6>GOLD: {item.gold}</h6>
              {console.log("Inventory items I've collected",item.inventory)}

            <div className="stuff">
            <h6>Treasures:</h6>
            {((item.inventory === []) ?
                <h6>No items in inventory!</h6>
                
                :
                
                item.inventory.map(treasure => (
                <h6 key={treasure}>{treasure}, </h6>
                ))
              )}

            <h6>Abilities:</h6>
            {((item.abilities === []) ?
                <h6>No abilities!</h6>
                
                :

                item.abilities.map(abilities => (
                    
                    <h6 key={abilities}>{abilities}</h6>
                    ))
                   
              )}
               {console.log("Abilities",item.abilities)}
            <h6>Status:</h6>
            {((item.status === []) ?
                <h6>No status active!</h6>
                
                :

                item.status.map(stats => (
                    <h6 key={stats}>{stats}</h6>
                    ))
                
              )}
              </div>
            </div>
          ))}
        </div>
    )
}

export default Inventory;