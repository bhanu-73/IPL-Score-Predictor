import pickle
import time
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

train = pd.read_csv("C:/Users/Teja/PycharmProjects/IPL_Score_Predictor/data/engineered_matches.csv")
x = train.drop('score', axis=1)
y = train['score']


def train_and_store(model, path):
    start = time.time()
    model.fit(x, y)
    with open(path, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model trained and stored in {time.time() - start} secs")


lg_model = LinearRegression()
dt_model = DecisionTreeRegressor()
rf_model = RandomForestRegressor()

base_path = "C:/Users/Teja/PycharmProjects/IPL_Score_Predictor/pickle_files"
train_and_store(lg_model, base_path + "/linear_regression_model")
train_and_store(dt_model, base_path + "/decision_tree_model")
train_and_store(rf_model, base_path + "/random_forest_model")
