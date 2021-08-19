class FanGraphs {

  static safeRound(value, precision) {
    if (value !== '' && value !== null && value !== undefined) {
      const factorOfTen = Math.pow(10, precision);
      return Math.round(value * factorOfTen) / factorOfTen;
    }
    return value;
  }

  static safeInteger(value) {
    if (value !== '' && value !== null && value !== undefined) {
      return parseInt(value);
    }
    return value;
  }

  static parsePlayers(data) {
    let players = [];

    data.forEach(value => {
      players.push({
        key: value['key'],
        name: value['Name'],
        team: value['Team'],
        league: value['League'],
        division: value['Division'],
        g: value['G'],
        pa: value['PA'],
        hr: value['HR'],
        r: value['R'],
        rbi: value['RBI'],
        sb: value['SB'],
        bb: this.safeRound(value['BB%'], 3),
        k: this.safeRound(value['K%'], 3),
        iso: this.safeRound(value['ISO'], 3),
        babip: this.safeRound(value['BABIP'], 3),
        avg: this.safeRound(value['AVG'], 3),
        obp: this.safeRound(value['OBP'], 3),
        slg: this.safeRound(value['SLG'], 3),
        woba: this.safeRound(value['wOBA'], 3),
        xwoba: this.safeRound(value['xwOBA'], 3),
        wrc: this.safeInteger(value['wRC+']),
        bsr: this.safeRound(value['BsR'], 1),
        off: this.safeRound(value['Off'], 1),
        def: this.safeRound(value['Def'], 1),
        war: this.safeRound(value['WAR'], 1)
      });
    });

    return players;
  }

  static fetchBatting(url) {
    return new Promise((resolve, reject) => {
      fetch(url)
        .then(response => response.json())
        .then(data => {
          let teams = data.teams.filter(team => team.name != '');
          let players = this.parsePlayers(data.batters);
          resolve({
            teams: teams,
            players: players
          });
      });
    });
  }
}