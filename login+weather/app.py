from flask import Flask
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask import json
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

import datetime
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/bozkurt/Desktop/login-register-form/database.db'
db = SQLAlchemy(app)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route('/')
@app.route('/index.html')


# 1800 seconds == 30 minutes
@cache.cached(timeout=300)
def index():
    timestamp = datetime.datetime.now()
    raw_data = requests.get('https://forecast.weather.gov/MapClick.php?lat=40.74&lon=-74&unit=0&lg=english&FcstType=json').json()
    # raw_data = json.load(open('sample-forecast.json'))
    parsed_data = {
        'areaDescription' : raw_data['location']['areaDescription'],
        'forecast_time' : raw_data['time']['startPeriodName'][0],
        'forecast_data_weather' : raw_data['data']['weather'][0],
        'forecast_data_text' : raw_data['data']['text'][0],
        'forecast_time_1' : raw_data['time']['startPeriodName'][1],
        'forecast_data_weather_1' : raw_data['data']['weather'][1],
        'forecast_data_text_1' : raw_data['data']['text'][1],
        'forecast_time_2' : raw_data['time']['startPeriodName'][2],
        'forecast_data_weather_2' : raw_data['data']['weather'][2],
        'forecast_data_text_2' : raw_data['data']['text'][2],
        'forecast_time_3' : raw_data['time']['startPeriodName'][3],
        'forecast_data_weather_3' : raw_data['data']['weather'][3],
        'forecast_data_text_3' : raw_data['data']['text'][3],
        'forecast_data_weather_4' : raw_data['data']['weather'][4],
        'forecast_data_text_4' : raw_data['data']['text'][4]
    }
    return render_template('index.html',timestamp=timestamp, **parsed_data)


@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]

        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
