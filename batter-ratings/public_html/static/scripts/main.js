function main() {
  window.app = new Vue({
    el: 'div#app',
    data: {
      dataFetched: false,
      published: '',
      cacheKey: '',
      teams: [],
      players: [],
      sortColumn: 'pa',
      sortDirection: 'asc',
      leagueFilter: '*',
      teamFilter: '*',
      textFilter: '',
    },
    created: async function() {
      this.published = document.head.querySelector('[name=published][content]').content;
      this.cacheKey = document.querySelector('meta[name="cache-key"]').getAttribute('content');
      let data = await FanGraphs.fetchBatting('./batters.json?cache=' + this.cacheKey);
      this.teams = data.teams.filter(team => team.name != '');
      this.players = data.players;
      this.dataFetched = true;
    },
    methods: {
      sortedClass(column) {
        return this.sortColumn === column ? 'sorted' : '';
      },
      filterOutBlankTeams(teamName) {
        if (teamName === '- - -') {
          return '-';
        }
        else {
          return teamName;
        }
      },
      handleSortClick: function(s) {
        if (s === this.sortColumn) {
          this.sortDirection = this.sortDirection === 'asc' ? 'desc': 'asc';
        }
        this.sortColumn = s;
      },
      sortPlayers: function(players) {
        let sortedPlayers = players.sort((a,b) => {
          let modifier = 1;
          if (this.sortDirection === 'desc') modifier = -1;
          if (a[this.sortColumn] < b[this.sortColumn]) return -1 * modifier;
          if (a[this.sortColumn] > b[this.sortColumn]) return 1 * modifier;
          return 0;
        });

        // Declare the direction each column should sort by default
        let columnTypes = {
          name: 'asc',
          team: 'asc',
          g: 'asc',
          pa: 'asc',
          hr: 'asc',
          r: 'asc',
          rbi: 'asc',
          sb: 'asc',
          bb: 'asc',
          k: 'asc',
          iso: 'asc',
          babip: 'asc',
          avg: 'asc',
          obp: 'asc',
          slg: 'asc',
          woba: 'asc',
          xwoba: 'asc',
          wrc: 'asc',
          bsr: 'asc',
          off: 'asc',
          def: 'asc',
          war: 'asc',
          league: 'asc',
          division: 'asc',
        }

        let colType = columnTypes[this.sortColumn];

        if (this.sortDirection === 'desc') {
          if (colType === 'desc') {
            sortedPlayers.forEach(function(element, index) {
              element['mlb_rank'] = index + 1;
            });
          }
          else {
            sortedPlayers.forEach(function(element, index) {
              element['mlb_rank'] = sortedPlayers.length - index + 1;
            });
          }
        }
        else if (this.sortDirection === 'asc') {
          if (colType === 'asc') {
            sortedPlayers.forEach(function(element, index) {
              element['mlb_rank'] = index + 1;
            });
          }
          else {
            sortedPlayers.forEach(function(element, index) {
              element['mlb_rank'] = sortedPlayers.length - index + 1;
            });
          }
        }

        return sortedPlayers;
      },
      filterByLeague: function(players, leagueFilter) {
        return players.filter(player => {
          if (leagueFilter.startsWith('AL')) {
            if (leagueFilter.endsWith('*')) {
              return player.league === 'AL';
            }
            else {
              return player.division === leagueFilter;
            }
          }
          else if (leagueFilter.startsWith('NL')) {
            if (leagueFilter.endsWith('*')) {
              return player.league === 'NL';
            }
            else {
              return player.division === leagueFilter;
            }
          }
          else {
            return true;
          }
        });
      },
      filterByTeam: function(players, team) {
        return players.filter(player => {
          if (team === '*') {
            return true;
          }
          else {
            return player.team === team;
          }
        });
      },
      filterByName: function(players, textFilter) {
        if (textFilter.length == 0) return players;

        textFilter = textFilter.toLowerCase().trim();
        let tokens = textFilter.split(/[,]+/);
        return players.filter(value => {
          let playerName = value.name.toLowerCase();
          let anyMatched = false;
          tokens.forEach(token => {
            token = token.trim();
            if (token.length > 0 && playerName.includes(token)) {
              anyMatched = true;
            }
          });
          return anyMatched;
        });
      },
      teamLogoUrl: function(team) {
        return 'static/images/' + team + '.png';
      }
    },
    computed: {
      displayPlayers: function() {
        let players = this.players;
        players = this.sortPlayers(players);
        players = this.filterByName(players, this.textFilter);
        players = this.filterByLeague(players, this.leagueFilter);
        players = this.filterByTeam(players, this.teamFilter);
        return players;
      }
    },
    filters: {
      fmt_pct: function(value, precision) {
        if (value != null) {
          return (value * 100).toFixed(precision).toString() + '%';
        }
        return '';
      }
    }
  });
}
