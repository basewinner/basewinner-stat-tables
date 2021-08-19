import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";
import Player_By_Season from "./pictures/Player_By_Season.jpg";
import player_by_week from "./pictures/player_by_week.jpg";
import expected_standings from "./pictures/expected_standings.jpg";


function Home() {
  return (
    <div className="Home">
      <h1 className="text-center">
       Choose A Table to Get Ratings
      </h1>
        <div className="list-center">
          <img src={Player_By_Season} />
            <h3 >
              <Link className="center" to={`/season`}>Season</Link>
            </h3>
        </div>
        <div className="list-center">
        <img src={player_by_week} />
          <h3 >
            <Link className="center" to={`/week`}>Week</Link>
          </h3>
      </div>
        <div className="list-center">
        <img src={expected_standings} />
          <h3 >
            <Link className="center" to={`/expected`}>Expected Standings</Link>
          </h3>
      </div>
    </div>
  );
}

export default Home;