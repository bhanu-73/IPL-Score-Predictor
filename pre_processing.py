import math
import json
import pandas as pd


data = pd.read_csv('E:/Programming/pandas_files/cricket/all_matches.csv')
print(data.columns)

data.drop(['wides', 'noballs', 'byes', 'penalty', 'legbyes', 'other_wicket_type', 'other_player_dismissed'],
          inplace=True, axis=1)


def runs_per_ball(columns):
    return columns[0] + columns[1]


score = 0


def score_board(cols):
    ball = cols[0]
    runs = cols[1]
    global score
    if ball == 0.1:
        score = 0
    score += runs
    return score


def get_season(season):
    season = str(season)
    return int(season[:4])


wickets = 0


def get_wickets(columns):
    ball = columns[0]
    dismissal = columns[1]
    global wickets
    if not pd.isnull(dismissal):
        wickets += 1
    if ball == 0.1:
        wickets = 0
    return wickets


def get_venue(venue):
    venue = venue.split(',')
    return venue[0]


def replace(col, a, b):
    if col == a:
        return b
    return col


def adv_replace(col, dict):
    return dict[col]


def get_overs(ball):
    return math.ceil(ball)


def get_ball(ball):
    return int(str(ball)[-1:])


strikers_set = set()


def get_strikers(cols):
    global strikers_set
    ball = cols[0]
    striker = cols[1]
    strikers_set.add(striker)
    s = list(strikers_set)
    if ball == 0.1:
        strikers_set = set()
    return ','.join(s)


bowler_set = set()


def get_bowlers(cols):
    global bowler_set
    ball = cols[0]
    bowler = cols[1]
    bowler_set.add(bowler)
    b = list(bowler_set)
    if ball == 0.1:
        bowler_set = set()
    return ','.join(b)


def get_avg_strike_rates(strikers, dict):
    strikers = strikers.split(',')
    strikers = [round(float(dict.get(i,133.33)), 2) for i in strikers]
    return round(sum(strikers) / len(strikers),2)


def get_avg_economy(bowlers, dict):
    bowlers = bowlers.split(',')
    bowlers = [round(float(dict.get(i,8.0)), 2) for i in bowlers]
    return round(sum(bowlers) / len(bowlers),2)


data['season'] = data['season'].apply(lambda x: get_season(x))
data['venue'] = data['venue'].apply(lambda x: get_venue(x))
data['batting_team'] = data['batting_team'].apply(lambda x: replace(x, 'Delhi Daredevils', 'Delhi Capitals'))
data['batting_team'] = data['batting_team'].apply(
    lambda x: replace(x, 'Rising Pune Supergiant', 'Rising Pune Supergiants'))
data['batting_team'] = data['batting_team'].apply(lambda x: replace(x, 'Kings XI Punjab', 'Punjab Kings'))
data['bowling_team'] = data['bowling_team'].apply(lambda x: replace(x, 'Delhi Daredevils', 'Delhi Capitals'))
data['bowling_team'] = data['bowling_team'].apply(
    lambda x: replace(x, 'Rising Pune Supergiant', 'Rising Pune Supergiants'))
data['bowling_team'] = data['bowling_team'].apply(lambda x: replace(x, 'Kings XI Punjab', 'Punjab Kings'))
data['season'] = data['season'].apply(lambda x: replace(x, 2007, 2008))
data['season'] = data['season'].apply(lambda x: x - 2007)
data['venue'] = data['venue'].apply(lambda x: replace(x, 'M.Chinnaswamy Stadium', 'M Chinnaswamy Stadium'))
data['venue'] = data['venue'].apply(lambda x: replace(x, 'Feroz Shah Kotla', 'Arun Jaitley Stadium'))
data['venue'] = data['venue'].apply(lambda x: replace(x, 'Sardar Patel Stadium', 'Narendra Modi Stadium'))
# data  = data[(data['ball']==0.6) | (data['ball']==1.6) | (data['ball']==2.6) | (data['ball']==3.6) | (data['ball']==4.6) | (data['ball']==5.6)|(data['ball']==6.6) | (data['ball']==7.6) | (data['ball']==8.6) | (data['ball']==9.6) | (data['ball']==10.6) | (data['ball']==11.6)|(data['ball']==12.6) | (data['ball']==13.6) | (data['ball']==14.6) | (data['ball']==15.6) | (data['ball']==16.6) | (data['ball']==17.6)| (data['ball']==18.6)| (data['ball']==19.6)]
data = data[(data['batting_team'] != 'Kochi Tuskers Kerala') & (data['bowling_team'] != 'Kochi Tuskers Kerala') & (
        data['batting_team'] != 'Rising Pune Supergiants') & (data['bowling_team'] != 'Rising Pune Supergiants') & (
                    data['batting_team'] != 'Pune Warriors') & (data['bowling_team'] != 'Pune Warriors') & (
                    data['batting_team'] != 'Gujarat Lions') & (data['bowling_team'] != 'Gujarat Lions') & (
                    data['batting_team'] != 'Deccan Chargers') & (data['bowling_team'] != 'Deccan Chargers')]

#data = data[(data['ball'] < 6)]
with open('strikerates.json', 'r') as file:
    strike_rates = json.load(file)
with open('economies..json', 'r') as file:
    economies = json.load(file)
data['strikers'] = data[['ball', 'striker']].apply(lambda x: get_strikers(x), axis=1)
data['bowlers'] = data[['ball', 'bowler']].apply(lambda x: get_bowlers(x), axis=1)
strike_rates['PP Chawla'] = 111.45
strike_rates['KV Sharma'] = 115.69
strike_rates['Niraj Patel'] = 101.69
strike_rates['P Simran Singh'] = 134
strike_rates['JDP Oram'] = 28.4
strike_rates['M Kartik'] = 143.3
strike_rates['VY Mahesh'] = 39
strike_rates['Kamran Khan'] = 132.24
economies['V Sehwag'] = 10.37
economies['AM Nayar'] = 8.44
economies['SA Yadav'] = 7.25
economies['Gurkeerat Singh'] = 7.46
economies['M Vijay'] = 8.17
data['avg_strikerate'] = data['strikers'].apply(lambda x: get_avg_strike_rates(x, strike_rates))
data['avg_economy'] = data['bowlers'].apply(lambda x: get_avg_economy(x, economies))

data['runs'] = data[['runs_off_bat', 'extras']].apply(lambda x: runs_per_ball(x), axis=1)
data['wickets'] = data[['ball', 'player_dismissed']].apply(lambda x: get_wickets(x), axis=1)
# data['start_date'] = data['start_date'].apply(lambda x: pd.to_datetime(x))
# data['start_day'] = data['start_date'].dt.day
# data['start_month'] = data['start_date'].dt.month
data['score'] = data[['ball', 'runs']].apply(lambda x: score_board(x), axis=1)
# data['overs'] = data['ball'].apply(lambda x: get_overs(x))
# data['ball'] = data['ball'].apply(lambda x: get_ball(x))
data.drop(['match_id', 'start_date', 'runs_off_bat', 'runs', 'extras', 'wicket_type', 'player_dismissed'], axis=1,
          inplace=True)

df = data[(data['ball'] == 5.6)]
ser1 = data.groupby('venue').mean()['score'].sort_values()
ser1 = list(ser1.index)
ser2 = df.groupby('batting_team').mean()['score'].sort_values()
ser2 = list(ser2.index)

venues_numbered = [i for i in range(1, len(ser1) + 1)]
teams_numbered = [i for i in range(1, len(ser2) + 1)]
venues = {ser1[i]: venues_numbered[i] for i in range(len(ser1))}
teams = {ser2[i]: teams_numbered[i] for i in range(len(ser2))}
print(venues)
print(teams)

data['venue'] = data['venue'].apply(lambda x: adv_replace(x, venues))
data['batting_team'] = data['batting_team'].apply(lambda x: adv_replace(x, teams))
data['bowling_team'] = data['bowling_team'].apply(lambda x: adv_replace(x, teams))

data.drop(['striker', 'non_striker', 'bowler', 'strikers', 'bowlers'], axis=1,
          inplace=True)

data.to_csv('engineered_matches.csv', index=False)
