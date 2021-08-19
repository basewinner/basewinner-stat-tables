import React from "react";
import expected_standings from "./pictures/expected_standings.jpg";
import {ExpectedTable} from './components/ExpectedTable'

function Expected() {
  return (
    <div>
      <h1 className="standings">MLB Expected Standings</h1>
      <ExpectedTable />
      <h3>Chart Key</h3>
    </div>
  );
}

export default Expected;