import React from 'react';
import logo from './logo.svg';
import maze from './images/maze1.jpg'
import './App.scss';

import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom';

import Home from './Components/Home/Home'
import Inventory from './Components/Inventory/Inventory';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <Inventory />
        <Router>
          <Route exact path="/" component={Home}/>
          <Route exact path="/north" component={Home}/>
          <Route exact path="/south" component={Home}/>
        </Router>
        <img className="maze-img" src={maze} alt="maze" height="100px" width="100px"/>
      </header>
    </div>
  );
}

export default App;
