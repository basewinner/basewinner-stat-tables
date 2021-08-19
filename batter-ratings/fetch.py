import argparse
import arrow
import bs4
import jinja2
import json
import numpy as np
import pandas as pd
import pathlib
import requests
import sys
import time
import urllib.parse

from models import Batter
from models import Team

TEAMS = {
    'ARI': {'league': 'NL', 'division': 'NLW', 'name': 'Arizona Diamondbacks'},
    'ATL': {'league': 'NL', 'division': 'NLE', 'name': 'Atlanta Braves'},
    'BAL': {'league': 'AL', 'division': 'ALE', 'name': 'Baltimore Orioles'},
    'BOS': {'league': 'AL', 'division': 'ALE', 'name': 'Boston Red Sox'},
    'CHC': {'league': 'NL', 'division': 'NLC', 'name': 'Chicago Cubs'},
    'CIN': {'league': 'NL', 'division': 'NLC', 'name': 'Cincinnati Reds'},
    'CLE': {'league': 'AL', 'division': 'ALC', 'name': 'Cleveland Indians'},
    'COL': {'league': 'NL', 'division': 'NLW', 'name': 'Colorado Rockies'},
    'CHW': {'league': 'AL', 'division': 'ALC', 'name': 'Chicago White Sox'},
    'DET': {'league': 'AL', 'division': 'ALC', 'name': 'Detroit Tigers'},
    'HOU': {'league': 'AL', 'division': 'ALW', 'name': 'Houston Astros'},
    'KCR':  {'league': 'AL', 'division': 'ALC', 'name': 'Kansas City Royals'},
    'LAA': {'league': 'AL', 'division': 'ALW', 'name': 'Los Angeles Angels'},
    'LAD': {'league': 'NL', 'division': 'NLW', 'name': 'Los Angeles Dodgers'},
    'MIA': {'league': 'NL', 'division': 'NLE', 'name': 'Miami Marlins'},
    'MIL': {'league': 'NL', 'division': 'NLC', 'name': 'Milwaukee Brewers'},
    'MIN': {'league': 'AL', 'division': 'ALC', 'name': 'Minnesota Twins'},
    'NYM': {'league': 'NL', 'division': 'NLE', 'name': 'New York Mets'},
    'NYY': {'league': 'AL', 'division': 'ALE', 'name': 'New York Yankees'},
    'OAK': {'league': 'AL', 'division': 'ALW', 'name': 'Oakland Athletics'},
    'PHI': {'league': 'NL', 'division': 'NLE', 'name': 'Philadelphia Phillies'},
    'PIT': {'league': 'NL', 'division': 'NLC', 'name': 'Pittsburg Pirates'},
    'SDP':  {'league': 'NL', 'division': 'NLW', 'name': 'San Diego Padres'},
    'SEA': {'league': 'AL', 'division': 'ALW', 'name': 'Seattle Mariners'},
    'SFG':  {'league': 'NL', 'division': 'NLW', 'name': 'San Francisco Giants'},
    'STL': {'league': 'NL', 'division': 'NLC', 'name': 'St. Louis Cardinals'},
    'TBR':  {'league': 'AL', 'division': 'ALE', 'name': 'Tampa Bay Rays'},
    'TEX': {'league': 'AL', 'division': 'ALW', 'name': 'Texas Rangers'},
    'TOR': {'league': 'AL', 'division': 'ALE', 'name': 'Toronto Blue Jays'},
    'WSN': {'league': 'NL', 'division': 'NLE', 'name': 'Washington Nationals'},
    '- - -': {'league': '', 'division': '', 'name': ''},
}

class BatterStatsManager(object):

    def __init__(self, teams, debug):
        self.teams = teams
        self.debug = debug;

    def fetch(self, game_date):
        print(f"Fetching Batters Data for {game_date.format('YYYY-MM-DD')}")
        contents = self._fetch_batting_stats(game_date)
        df = self._create_dataframe(contents)
        return df

    def strip_pct_signs(self, value):
        if value and type(value) == str:
            return value.replace(' %', '').replace('%', '')
        return value

    def _create_dataframe(self, html):
        soup = bs4.BeautifulSoup(html, 'lxml')

        table_el = soup.find('table', class_='rgMasterTable')
        table_el.find('tr', class_='rgPager').extract()
        table_el.find('colgroup').extract()
        table_el.find('tfoot').extract()

        # Make sure there is data for the given date
        if table_el.tbody.find('tr').find('td').text == 'No records to display.':
            return pd.DataFrame()

        # We need to extract the player fangraphs ID from the table
        player_ids = []

        for tr_el in table_el.tbody.find_all('tr'):
            td_els = tr_el.find_all('td')
            url = td_els[1].find('a').get('href')
            player_id = urllib.parse.parse_qs(url).get('statss.aspx?playerid')[0]
            player_name = td_els[1].text
            player_team = td_els[2].text
            player_ids.append({
                'Name': player_name,
                'FGID': player_id,
                'Team': player_team,
            })

        df = pd.read_html(str(table_el))[0]
        df = df.drop(columns=['#'])

        # Merge in the player_ids
        players_df = pd.DataFrame(player_ids)
        df = df.merge(players_df)

        df['League'] = df['Team'].apply(lambda v: self.teams.get(v, {}).get('league'))
        df['Division'] = df['Team'].apply(lambda v: self.teams.get(v, {}).get('division'))

        return df

    def _fetch_batting_stats(self, game_date):
        url = 'https://www.fangraphs.com/leaders.aspx'
        params = {
            'pos': 'all',
            'stats': 'bat',
            'lg': 'all',
            'qual': '0',
            'type': 'c,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,310,29,30,28,110,58,52',
            'season': game_date.format('YYYY'),
            'month': '1000',
            'season1': game_date.format('YYYY'),
            'ind': '0',
            'team': '0',
            'rost': '0',
            'age': '0',
            'filter': '',
            'players': '0',
            'startdate': game_date.format('YYYY-MM-DD'),
            'enddate': game_date.format('YYYY-MM-DD'),
            'page': '1_1000',
        }
        response = requests.get(url, params=params)

        if self.debug:
            print(response.url)

        assert response.ok, 'Could not fetch batting stats'
        contents = response.text
        return contents


def valid_dir_arg(arg):
    """ Used by argparse to see if a directory exists """
    path = pathlib.Path(arg)
    if not path.exists() or not path.is_dir:
        msg = f'File "{arg}" does not exist'
        raise argparse.ArgumentTypeError(msg)
    else:
        return path


def valid_date_arg(date_string):
    """ Used by argparser to validate date arguments """
    try:
        return arrow.get(date_string, 'YYYY-MM-DD')
    except arrow.parser.ParserError:
        msg = f'Not a valid date: "{date_string}"'
        raise argparse.ArgumentTypeError(msg)


def validate_and_normalize_dates(start_date, end_date):
    """ Ensures the dates passed are valid and in US/Eastern """
    start_date = start_date.replace(tzinfo='US/Eastern')

    # If no end date was passed, use the start date
    end_date = end_date.replace(tzinfo='US/Eastern') if end_date else start_date

    # Make sure the end date is not less than the start date
    assert start_date <= end_date, 'The end date cannot be less than the start date.'

    # You cannot fetch data greater than yesterday
    yesterday = arrow.now().shift(days=-1).floor('day')
    assert end_date <= yesterday, 'You cannot fetch data newer than yesterday'

    return start_date, end_date


if __name__ == '__main__':

    # Configure command-line arguments
    argparser = argparse.ArgumentParser()
    argparser.add_argument('start_date', type=valid_date_arg)
    argparser.add_argument('end_date', type=valid_date_arg, nargs='?')
    argparser.add_argument('--debug', action='store_true', default=False)
    args = argparser.parse_args()

    # Make sure we have valid dates in US/Eastern
    start_date, end_date = validate_and_normalize_dates(args.start_date, args.end_date)

    # Create an Arrow range for the dates
    date_range = list(arrow.Arrow.range('day', start_date, end_date))

    # The manager is used to fetch the data
    manager = BatterStatsManager(TEAMS, args.debug)

    # Iterate through each date in the range and fetch the data
    for index, date in enumerate(date_range):

        # Fetch the batting for the given date
        df = manager.fetch(date)

        # Make sure there is data for the date
        if df.empty:
            print('No data found for date. Skipping.')
            continue

        # Remove any records with zero plate appearances
        df = df[df['PA'] > 0]

        # If there were no pitches, fill in nans
        df['SwStr%'] = df['SwStr%'].fillna(0)
        df['HardHit'] = df['HardHit'].fillna(0)

        # Create computed fields
        df['SwStr%'] = df['SwStr%'].apply(manager.strip_pct_signs).astype(float).div(100).round(4)
        df['Swings_Misses'] = df['SwStr%'].multiply(df['Pitches']).round(0).astype(int).astype(int)
        df['Game Date'] = date.format('YYYY-MM-DD')
        df['HardHit'] = df['HardHit']

        # Turn the dataframe into a list of dictionaries
        players = df.to_dict(orient='records')

        # Keep track of how many inserts and updates we performed
        created = 0
        updated = 0

        # Iterate through the players and insert into the database
        for player in players:

            team_abbr = player.get('Team')
            team_name = TEAMS.get(team_abbr).get('name')
            team, _ = Team.get_or_create(name=team_name, abbr=team_abbr)

            # If the record already exists, we will overwrite it
            try:
                batter = Batter.get(date=player.get('Game Date'), fangraphs_id=player.get('FGID'))
                updated += 1
            except Batter.DoesNotExist:
                batter = Batter()
                batter.date = player.get('Game Date')
                created += 1

            batter.name = player.get('Name')
            batter.team = team
            batter.at_bats = player.get('AB')
            batter.fangraphs_id = player.get('FGID')
            batter.plate_appearances = player.get('PA')
            batter.hits = player.get('H')
            batter.single = player.get('1B')
            batter.doubles = player.get('2B')
            batter.triples = player.get('3B')
            batter.home_runs = player.get('HR')
            batter.runs = player.get('R')
            batter.runs_batted_in = player.get('RBI')
            batter.walks = player.get('BB')
            batter.intentional_walks = player.get('IBB')
            batter.strikeouts = player.get('SO')
            batter.hit_by_pitches = player.get('HBP')
            batter.sacrifice_flys = player.get('SF')
            batter.sacrifice_hits = player.get('SH')
            batter.grounded_double_play = player.get('GDP')
            batter.stolen_bases = player.get('SB')
            batter.caught_stealings = player.get('CS')
            batter.hard_hits = player.get('HardHit')
            batter.balls = player.get('Balls')
            batter.strikes = player.get('Strikes')
            batter.pitches = player.get('Pitches')
            batter.swinging_strike_pct = player.get('SwStr%')
            batter.swings_and_misses = player.get('Swings_Misses')
            batter.wins_above_replacement = player.get('WAR')
            batter.weighted_runs_created = player.get('wRC')

            batter.save()

        print(f"Created {created} records. Updated {updated} records. Date: {date.format('YYYY-MM-DD')}")

        # If there are more dates to fetch, pause to respect the load on their servers
        if index + 1 < len(date_range):
            time.sleep(2)
