from flask import Flask, render_template, request
from predict import predictor

home = Flask(__name__)


@home.route('/')
def homePage():
    return render_template('home.html')


@home.route('/predict')
def predict():
    innings = request.args.get("innings")
    bt = request.args.get("bt")
    over = request.args.get("over")
    params = [request.args.get("venue"), innings, over, bt,
              request.args.get("bwt"), request.args.get("batsmen"), request.args.get("bowlers")]
    score = predictor(*params)
    power_play_score = ""
    power_play_msg = ""
    if float(over) > 5.6:
        params[2] = 5.6
        power_play_score = predictor(*params)
        power_play_msg = "Expected Power Play Score is "
    params[2] = 19.6
    final_score = predictor(*params)
    o, b = str(19.6).split('.')
    run_rate = round(final_score / (int(o) + (int(b) / 6)), 2)
    return render_template('predict.html', team=bt, over=over, score=score, ppmsg=power_play_msg,
                           ppscore=power_play_score, run_rate=run_rate,
                           innings="1st" if innings == "1" else "2nd",
                           fscore=final_score)


home.run()
