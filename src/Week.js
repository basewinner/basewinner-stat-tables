import React from "react";
import { Link, Redirect } from "react-router-dom";
import {WeekTable} from './components/WeekTable'

function Week() {
  return (
    <div>
      <h1>Player By Week</h1>
      <WeekTable />
      <h3>Chart Key</h3>
    </div>
  );
}

export default Week;
