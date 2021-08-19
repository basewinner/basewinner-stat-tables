import React from "react";
import { NavLink } from "react-router-dom";
import "./NavBar.css";

function NavBar() {
  return (
    <nav className="NavBar">
      <NavLink exact to="/">
        Home
      </NavLink>
      <NavLink exact to="/season">
        Player by Season
      </NavLink>
      <NavLink exact to="/week">
        Player By Week
      </NavLink>
      <NavLink exact to="/expected">
        X Standings
      </NavLink>
    </nav>
  );
}

export default NavBar;
