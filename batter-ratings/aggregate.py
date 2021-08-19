import argparse
import json
import pandas as pd
import pathlib
import peewee
import sqlite3
import tqdm

from models import Batter
from models import Team

PA_PER_9 = 37.3
BB_SLOPE = 0.795
BB_INTERCEPT = 0.204

# The column names from the dictionary are very long and result in huge JSON file
# so we will replace them with short names
COLUMN_NAMES = {
    'date': 'week',
    'team_id': 'tid',
    'at_bats': 'ab',
    'plate_appearances': 'pa',
    'hits': 'h',
    'single': '1b',
    'doubles': '2b',
    'triples': '3b',
    'home_runs': 'hr',
    'runs': 'r',
    'runs_batted_in': 'rbi',
    'walks': 'bb',
    'intentional_walks': 'ibb',
    'strikeouts': 'so',
    'hit_by_pitches': 'hbp',
    'sacrifice_flys': 'sf',
    'sacrifice_hits': 'sh',
    'grounded_double_play': 'gdp',
    'stolen_bases': 'sb',
    'caught_stealings': 'cs',
    'hard_hits': 'hh',
    'balls': 'b',
    'strikes': 's',
    'pitches': 'p',
    'swinging_strike_pct': 'ssp',
    'swings_and_misses': 'sam',
    'wins_above_replacement': 'war',
    'weighted_runs_created': 'wrc',
    'hard_hit_per_nine': 'hh9',
    'expected_walk_rate': 'xwr',
    'fgid': 'fgid',
}


def load_dataframe_from_sqlite(filepath):
    """ Loads a dataframe with all the records from the batters table """
    conn = sqlite3.connect('batters.db')
    sql = 'SELECT batter.*, team.name AS team_name FROM batter INNER JOIN team ON batter.team_id=team.id'
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


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

    # Load the database records into a dataframe
    df = load_dataframe_from_sqlite('batters.db')

    # Convert the date string into a datetime, then make it the dataframe's index
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    # Create a dict of all the teams with the team id as the dictionary key
    teams = {}

    for index, row in df.reset_index()[['team_id', 'team_name']].drop_duplicates().iterrows():
        team_name = row.get('team_name')
        team_id = row.get('team_id')
        teams[team_id] = team_name

    # We'll store a dictionary of all the players using their fangraphs id as the dictionary key
    players = {}

    for index, row in df.reset_index()[['fangraphs_id', 'name']].drop_duplicates().iterrows():
        player_name = row.get('name')
        fgid = row.get('fangraphs_id')
        players[fgid] = player_name

    # We'll store a list of each player's weekly dataframes, then after we will concatenate them into one dataframe
    weekly_player_dfs = []

    grouped = df.groupby(['fangraphs_id', 'team_id'])

    # Group the dataframe by the fangraphs ID so we have a dataframe for each individual player
    for (fgid, team_id), player_df in tqdm.tqdm(grouped):

        # We need to resample all the daily data by week
        wkdf = player_df.resample('W').agg('sum')

        # Take the date index and make it a column
        wkdf = wkdf.reset_index()

        # Turn the date column into a string so it can be exported as json
        wkdf['date'] = wkdf['date'].dt.strftime('%Y-%m-%d')

        # We don't need the id column
        wkdf = wkdf.drop(columns='id')

        # Filter out any rows that are empty
        wkdf = wkdf[wkdf['team_id'] > 0]

        # Add calculated fields
        wkdf['hard_hit_per_nine'] = wkdf['hard_hits'].div(wkdf['plate_appearances']).mul(PA_PER_9)
        wkdf['expected_walk_rate'] = wkdf['balls'].div(wkdf['pitches']).mul(BB_SLOPE) - BB_INTERCEPT
        wkdf['swinging_strike_pct'] = wkdf['swings_and_misses'] / wkdf['pitches']
        wkdf['expected_k_pct'] = wkdf['swinging_strike_pct'].mul(1.9872) + 0.011

        # Round any fields that might have too many decimal places
        wkdf['hard_hit_per_nine'] = wkdf['hard_hit_per_nine'].round(3)
        wkdf['expected_walk_rate'] = wkdf['expected_walk_rate'].round(3)
        wkdf['wins_above_replacement'] = wkdf['wins_above_replacement'].round(1)
        wkdf['swinging_strike_pct'] = wkdf['swinging_strike_pct'].round(3)

        # Add computed columns
        S = wkdf['single']
        D = wkdf['doubles']
        T = wkdf['triples']
        HR = wkdf['home_runs']
        H = wkdf['hits']
        BB = wkdf['walks']
        HBP = wkdf['hit_by_pitches']
        IBB = wkdf['intentional_walks']
        SB = wkdf['stolen_bases']
        CS = wkdf['caught_stealings']
        GDP = wkdf['grounded_double_play']
        PA = wkdf['plate_appearances']
        SF = wkdf['sacrifice_flys']
        SH = wkdf['sacrifice_hits']
        XBBR = wkdf['expected_walk_rate']
        XKR = wkdf['swings_and_misses']
        HH9 = wkdf['hard_hit_per_nine']

        # These components are used in the computed calculations
        A = H + BB + HBP - (0.50 * IBB) - HR
        B = 1.1 * (1.4*(S+2*D+3*T+4*HR) - 0.6*H - 3*HR + 0.1*(BB+HBP-IBB) + 0.9*(SB-CS-GDP))
        C = PA - BB - SF - SH - HBP - H + CS + GDP
        D = HR

        wkdf['base_runs'] = ((A*B)/(B+C)) + D
        wkdf['base_runs_ppa'] = wkdf['base_runs'].div(PA)
        wkdf['base_runs_p9'] = wkdf['base_runs_ppa'].mul(37.4)
        wkdf['xbbk'] =  XBBR / wkdf['expected_k_pct']

        # Add columns for the fangraphs id and the team id
        wkdf['fgid'] = fgid
        wkdf['team_id'] = team_id

        # Add this dataframe we worked on to the list of all player dataframes
        weekly_player_dfs.append(wkdf)

    # Now we need to take all the individual player dataframes and combine them back into one big one
    df2 = pd.concat(weekly_player_dfs)

    # Filter out any rows where the plate appearances are less than ten
    df2 = df2[df2['plate_appearances'] >= 10]

    # Replace the database column names with short names for the JSON
    df2.rename(columns=COLUMN_NAMES, inplace=True)

    # Calculate the 3M Batting numbers and rank each week
    df2['hh9_rank'] = df2['hh9'].rank(pct=True)
    df2['br9_rank'] = df2['base_runs_p9'].rank(pct=True)
    df2['xbbk_rank'] = df2['xbbk'].rank(pct=True)

    df2['3M Batting Pct'] = (df2['br9_rank'].mul(0.35) + df2['hh9_rank'].mul(0.35) + df2['xbbk_rank'].mul(0.3))
    df2['3M Batting Rank'] = df2['3M Batting Pct'].rank(ascending=False)

    # Output the filtered dataframe as JSON
    data = df2.to_dict(orient='records')

    output_dict = {
        'batters': players,
        'teams': teams,
        'data': data,
    }

    output = json.dumps(output_dict, separators=(',', ':'))
    pathlib.Path('public_html/aggregated_batting.json').write_text(output)
