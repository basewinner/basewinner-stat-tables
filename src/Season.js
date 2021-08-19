import React from "react";
import Player_By_Season from "./pictures/Player_By_Season.jpg";
import {SeasonTable} from './components/SeasonTable'
import { Link, Redirect } from "react-router-dom";

function Season() {
  return (
    <div>
      <h1>Player by Season</h1>
      <SeasonTable />
      <h3>Chart Key</h3>
    </div>
  );
}

export default Season;
