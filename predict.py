import pickle
import json
import pandas as pd
import numpy as np

models_path = "C:/Users/Teja/PycharmProjects/IPL_Score_Predictor/pickle_files/"
data_path = "C:/Users/Teja/PycharmProjects/IPL_Score_Predictor/data/"


def get_strike_rate(batsmen):
    with open(data_path + 'strike_rates.json', 'r') as file:
        strike_rates = json.load(file)

    strikers = batsmen.split(',')
    strikers = [round(float(strike_rates.get(i, 133.33)), 2) for i in strikers]
    return round(sum(strikers) / len(strikers), 2)


def get_economies(bowlers):
    with open(data_path + 'economies.json', 'r') as file:
        economies = json.load(file)

    bowlers = bowlers.split(',')
    bowlers = [round(float(economies.get(i, 8.0)), 2) for i in bowlers]
    return round(sum(bowlers) / len(bowlers), 2)


def get_team(team):
    with open(data_path + "teams.json", 'r') as file:
        teams = json.load(file)
    return teams.get(team)


def get_venue(venue):
    with open(data_path + "venues.json", 'r') as file:
        venues = json.load(file)
    return venues.get(venue)


def predictor(venue, innings, over, bt, bwt, batsmen, bowlers, model="random_forest"):
    with open(models_path + model, 'rb') as file:
        model = pickle.load(file)
    y = [15, get_venue(venue), innings, over, get_team(bt), get_team(bwt), get_strike_rate(batsmen),
         get_economies(bowlers), abs(len(batsmen.split(',')) - 2)]
    y = pd.DataFrame(np.array(y).reshape(1, 9),
                     columns=['season', 'venue', 'innings', 'ball', 'batting_team', 'bowling_team',
                              'avg_strikerate', 'avg_economy', 'wickets'])  # np.array(Y).reshape(1, 9)
    return int(round(model.predict(y)[0], 0))
