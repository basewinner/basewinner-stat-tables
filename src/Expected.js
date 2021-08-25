import React from "react";
import expected_standings from "./pictures/expected_standings.jpg";
import {ExpectedTable} from './components/ExpectedTable'
import "./Expected.css";


function Expected() {
  return (
    <div>
      <h1 className="standings">MLB Expected Standings</h1>
      <ExpectedTable />
      <h5 className="left">Published Tuesday, Agust 24th @ 7:00 AM ET</h5>
      <h3>Chart Key</h3>
    </div>
  );
}

export default Expected;