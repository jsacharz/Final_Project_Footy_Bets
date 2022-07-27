from tokenize import String
from flask import Flask, jsonify, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import scoped_session, sessionmaker
from config import password
import init_db
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle
import numpy as np


url = f'postgresql://postgres:{password}@localhost:5432/final_project'
# engine = create_engine(url)
app = Flask(__name__)
app = Flask(__name__, static_folder="templates")

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.debug = True
db = SQLAlchemy(app)

app.config['CORS_HEADERS'] = 'Content-Type'
filename = 'finalized_model.sav'
filename_minmax ='min_max_scalar.sav'

class matches(db.Model):
    __tablename__ = "matches_final"
    index = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=False)
    time = db.Column(db.String(), nullable=False)
    comp = db.Column(db.String(), nullable=False)
    round = db.Column(db.String(), nullable=False)
    day = db.Column(db.String(), nullable=False)
    venue = db.Column(db.String(), nullable=False)
    result = db.Column(db.String(), nullable=False)
    gf = db.Column(db.Integer(), nullable=False) 
    ga = db.Column(db.Integer(), nullable=False)
    opponent = db.Column(db.String(), nullable=False)
    xg = db.Column(db.Float(), nullable=False)
    xga = db.Column(db.Float(), nullable=False)
    poss = db.Column(db.Float(), nullable=False)
    attendance = db.Column(db.Integer(), nullable=False)
    captain = db.Column(db.String(), nullable=False)
    formation = db.Column(db.String(), nullable=False)
    referee = db.Column(db.String(), nullable=False)
    match_report = db.Column(db.String(), nullable=False)
    sh = db.Column(db.Float(), nullable=False)
    sot = db.Column(db.Float(), nullable=False)
    dist = db.Column(db.Float(), nullable=False)
    fk = db.Column(db.Float(), nullable=False)
    pk = db.Column(db.Float(), nullable=False)
    pkatt = db.Column(db.Float(), nullable=False)
    season  = db.Column(db.Integer(), nullable=False)
    team = db.Column(db.String(), nullable=False)

    def __init__(self, date, time, comp, round, day, venue, result, gf, ga, opponent, xg, xga, poss, attendance, captain, formation, referee, match_report, sh, sot, dist, fk, pk, pkatt, season, team):
        self.date = date
        self.time = time
        self.comp = comp
        self.round = round
        self.day = day 
        self.venue = venue 
        self.result = result
        self.gf = gf
        self.ga = ga
        self.opponent = opponent 
        self.xg = xg 
        self.xga = xga
        self.poss = poss
        self.attendance = attendance 
        self.captain = captain
        self.formation = formation
        self.referee = referee
        self.match_report = match_report
        self.sh = sh
        self.sot = sot
        self.dist = dist
        self.fk = fk
        self.pk = pk 
        self.pkatt = pkatt
        self.season = season 
        self.team = team

class team_list(db.Model):
    __tablename__="team_list"
    index = db.Column(db.Integer(), primary_key=True)
    team = db.Column(db.String(), nullable=False)
    def __init__(self, team):
        self.team=team

class upcoming_matches_df(db.Model):
    __tablename__ ="upcoming_matches_df"
    index = db.Column(db.Integer(), primary_key=True)
    Wk = db.Column(db.Float(), nullable=False)
    Day = db.Column(db.String(), nullable=False)
    Date = db.Column(db.Date(), nullable=False)
    Time  = db.Column(db.String(), nullable=False)
    Home  = db.Column(db.String(), nullable=False)
    Away = db.Column(db.String(), nullable=False)
    Venue  = db.Column(db.String(), nullable=False)
    season = db.Column(db.Integer(), nullable=False)
    mod1 = db.Column(db.String(), nullable=True)
    mod2 = db.Column(db.String(), nullable=True)

    def __init__(self, Wk, Day, Date, Time, Home, Away, Venue, season, mod1, mod2, mod3, mod4):
        self.wk = Wk
        self.day = Day
        self.date = Date
        self.time = Time
        self.home = Home
        self.away = Away
        self.venue = Venue
        self.season = season
        self.mod1 = mod1
        self.mod2 = mod2

def weeknum(weekday):
    switcher = {
        'Mon': 1,
        'Tue': 5,
        'Wed': 6,
        'Thu': 4,
        'Fri': 0,
        'Sat': 2,
        'Sun': 3
    } 
    return switcher.get(weekday, "nothing")

# Machine Learning calculation
def calculate_outcomes(day, venue, xg, xga, team, opponent):
    ## Column number is 2 for xg and 3 for xga
    df_mew = pd.DataFrame(columns=['day','venue','team','opponent'])
    df_mew.loc[0] = [day, venue, team, opponent]


    print(df_mew)

    file = open("dict_all.obj",'rb')
    dict_all_loaded = pickle.load(file)
    file.close()

    for col in df_mew.columns:
        df_mew.replace(dict_all_loaded[col], inplace=True)
    
    df_mew.insert(loc=2, column='xg', value=[xg])
    df_mew.insert(loc=3, column='xga', value=[xga])
    
    X=df_mew

    #     load.model(filename_ml, read)
    finalized_model = pickle.load(open(filename, 'rb'))
    #finalized_model = load.model(filename, read)
    y=finalized_model.predict(X)
    
    return y[0]

@app.route("/", methods=['POST', 'GET'])
def index():
    # Load drop down list data from postgres
    t_list = team_list.query.all()
    udata = upcoming_matches_df.query.all()
    uc_match_list = []
    weeknum_list = []
    lstWk = ''
    for uc_match in udata:
        uc_output = {}
        uc_output['wk'] =  uc_match.Wk
        uc_output['day'] =  uc_match.Day
        uc_output['date'] =  uc_match.Date
        uc_output['time'] =  uc_match.Time
        uc_output['home'] =  uc_match.Home
        uc_output['away'] =  uc_match.Away 
        uc_output['venue'] =  uc_match.Venue
        uc_output['season'] =  uc_match.season
        uc_output['mod1'] =  uc_match.mod1
        uc_output['mod2'] =  uc_match.mod2 
        uc_match_list.append(uc_output)
        if uc_match.Wk != lstWk:
            weeknum_list.append(uc_match.Wk)
        lstWk = uc_match.Wk
    
    # Machine Learning
    if request.method=='POST':
        day = request.form['day']
        print(day)
        venue = request.form['venue']
        print(venue)
        xg = request.form['xg']
        if xg == '':
            xg = 0.1
        xg = float(xg)

        xga = request.form['xga']
        if xga == '':
            xga = 0.1
        xga = float(xga)
        team = request.form['team']
        opponent = request.form['opponent']
        print(team)
        print(opponent)

        result = calculate_outcomes(day, venue, xg, xga, team, opponent)

        if result==0:
            result = 'Draw'
        elif result==1:
            result = 'Loss'
        else:
            result = 'Win'
        return result

    else:
        return render_template("index.html", upcoming_data=uc_match_list, weeknum_list = weeknum_list, t_list=t_list)

@app.route("/upcoming_matches")
def upcoming_matches():
    # init_db.upcoming_matches()
    t_list = team_list.query.all()
    # udata = upcoming_matches_df.query.all()
    udata = upcoming_matches_df.query.filter_by(Wk='1.0')
    uc_match_list = []
    weeknum_list = []
    lstWk = ''
    for uc_match in udata:
        uc_output = {}
        uc_output['wk'] =  uc_match.Wk
        uc_output['day'] =  uc_match.Day
        uc_output['date'] =  uc_match.Date
        uc_output['time'] =  uc_match.Time
        uc_output['home'] =  uc_match.Home
        uc_output['away'] =  uc_match.Away 
        uc_output['venue'] =  uc_match.Venue
        uc_output['season'] =  uc_match.season
        # uc_output['daynum'] = weeknum(uc_match.Day) 
        try:
            if calculate_outcomes(weeknum(uc_match.Day) , 'Home', 0, 0,uc_match.Home, uc_match.Away) == 0:
                uc_output['mod1'] =  'Draw'
            elif calculate_outcomes(weeknum(uc_match.Day) , 'Home', 0, 0,uc_match.Home, uc_match.Away) == 1:
                uc_output['mod1'] = 'Loss'
            else:
                uc_output['mod1'] = 'Win'    
        except ValueError:
            uc_output['mod1'] =''
        # uc_output['mod2'] =  uc_match.mod2 
        # uc_output['mod3'] =  uc_match.mod3
        # uc_output['mod4'] =  uc_match.mod4
        uc_match_list.append(uc_output)
        uc_match_list.append(uc_output)
        if uc_match.Wk != lstWk:
            weeknum_list.append(uc_match.Wk)
        lstWk = uc_match.Wk
    return render_template("index.html", upcoming_data=uc_match_list, weeknum_list = weeknum_list, t_list=t_list)

@app.route("/renew_data")
def renew_data():
    # init_db.scrape_data()
    init_db.retrieve_file()
    return redirect("/")

@app.route("/api", methods=['GET'])
def getMatchData():
    alldata = matches.query.all()
    output = []
    for match in alldata:
        dataoutput = {}
        dataoutput['date'] =  match.date
        dataoutput['time'] =  match.time
        dataoutput['comp'] =  match.comp
        dataoutput['round'] =  match.round
        dataoutput['day'] =  match.day 
        dataoutput['venue'] =  match.venue 
        dataoutput['result'] =  match.result
        dataoutput['gf'] =  match.gf
        dataoutput['ga'] =  match.ga
        dataoutput['opponent'] =  match.opponent 
        dataoutput['xg'] =  match.xg 
        dataoutput['xga'] =  match.xga
        dataoutput['poss'] =  match.poss
        dataoutput['attendance'] =  match.attendance 
        dataoutput['captain'] =  match.captain
        dataoutput['formation'] =  match.formation
        dataoutput['referee'] =  match.referee
        dataoutput['match_report'] =  match.match_report
        dataoutput['sh'] =  match.sh
        dataoutput['sot'] =  match.sot
        dataoutput['dist'] =  match.dist
        dataoutput['fk'] =  match.fk
        dataoutput['pk'] =  match.pk 
        dataoutput['pkatt'] =  match.pkatt
        dataoutput['season'] =  match.season 
        dataoutput['team'] =  match.team
        output.append(dataoutput)
    return jsonify(output)


if __name__ == '__main__':
   app.run(debug = True)