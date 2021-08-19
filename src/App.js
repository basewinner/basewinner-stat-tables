import React from "react";

import Home from "./Home";
import Season from "./Season";
import Drink from "./Week";
import NavBar from "./NavBar";
import Expected from "./Expected";

import { BrowserRouter, Route } from "react-router-dom";

function App() {
  return (
    <div className="container">
      <div className="App">
        <BrowserRouter>
          <NavBar />
          <Route exact path="/week">
            <Drink />
          </Route>
          <Route exact path="/season">
            <Season />
          </Route>
          <Route exact path="/expected">
            <Expected />
          </Route>
        
          <Route exact path="/">
            <Home />
          </Route>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
