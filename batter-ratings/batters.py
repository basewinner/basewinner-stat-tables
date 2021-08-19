import argparse
import arrow
import bs4
import jinja2
import json
import pandas as pd
import pathlib
import requests

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

    def __init__(self, teams):
        self.teams = teams

    def fetch(self, start_date, end_date):
        print('Fetching Batters Data')
        contents = self._fetch_batting_stats(start_date, end_date)
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

        df = pd.read_html(str(table_el))[0]
        df = df.drop(columns=['#'])

        df['League'] = df['Team'].apply(lambda v: self.teams.get(v, {}).get('league'))
        df['Division'] = df['Team'].apply(lambda v: self.teams.get(v, {}).get('division'))

        return df

    def _fetch_batting_stats(self, start_date, end_date):
        url = 'https://www.fangraphs.com/leaders.aspx'
        params = {
            'pos': 'all',
            'stats': 'bat',
            'lg': 'all',
            'qual': '50',
            'type': '8',
            'season': start_date.format('YYYY'),
            'month': '0',
            'season1': start_date.format('YYYY'),
            'ind': '0',
            'team': '',
            'rost': '',
            'age': '',
            'filter': '',
            'players': '',
            'startdate': '',
            'enddate': '',
            'page': '1_500',
        }
        response = requests.get(url, params=params)
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


if __name__ == '__main__':

    # Configure command-line arguments
    argparser = argparse.ArgumentParser()
    argparser.add_argument('output_dir', type=valid_dir_arg)
    args = argparser.parse_args()

    # Compute the last 30 days
    end_date = arrow.now().to('US/Eastern')
    start_date = end_date.shift(days=-30)

    # Fetch the batting for the past 30 days
    manager = BatterStatsManager(TEAMS)
    df = manager.fetch(start_date, end_date)

    # Create computed fields
    df['K%'] = df['K%'].apply(manager.strip_pct_signs).astype(float).div(100).round(4)
    df['BB%'] = df['BB%'].apply(manager.strip_pct_signs).astype(float).div(100).round(4)

    # Make a unique key for vue.js to use
    df['key'] = df.index.astype('str').str.zfill(3)

    # Figure out their division
    df['Division'] = df['Team'].apply(lambda v: TEAMS[v].get('division'))

    # Set up the template engine
    template_loader = jinja2.FileSystemLoader('./templates')
    template_env = jinja2.Environment(loader=template_loader)

    # Load the template
    template = template_env.get_template('batters.html')

    # Load the data and sort by plate appearances
    batters = df.sort_values('PA', ascending=False).to_dict(orient='records')

    # Get a list of the teams
    teams =  [{'abbr':k, 'name':v['name']} for k,v in TEAMS.items()]
    teams = sorted(teams, key=lambda k: k['name'])

    # Render the template
    published = arrow.now().to('US/Eastern')
    context = {'published': published}
    output_html = template.render(context)

    output_filepath = pathlib.Path(args.output_dir / 'index.html')
    output_filepath.write_text(output_html)

    # Render the JSON
    output_dict = {
        'batters': batters,
        'teams': teams,
    }

    output_json = json.dumps(output_dict, indent=2)

    output_filepath = pathlib.Path(args.output_dir / 'batters.json')
    output_filepath.write_text(output_json)

