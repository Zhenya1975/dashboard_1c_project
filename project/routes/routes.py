from flask import Blueprint, render_template, redirect, url_for, abort, request, jsonify, flash
# from models.models import SportDB, LeagueDB, TeamsDB, Match_statusDB, MatchesDB
from sqlalchemy import desc, asc
import pandas as pd
from datetime import datetime
import requests
import json


from extensions import extensions

# from sqlalchemy import desc, asc, func
# from sqlalchemy import and_, or_
# from flask_socketio import SocketIO, emit
# from datetime import datetime

db = extensions.db
# db.create_all()
# db.session.commit()
home = Blueprint('home', __name__, template_folder='templates')

socketio = extensions.socketio


@home.route('/weather')
def weather():
    URL = 'https://api.open-meteo.com/v1/forecast?latitude=51.16&longitude=71.43&hourly=temperature_2m'
    request = requests.get(URL)

    weather_data_dict = request.json()
    # print(weather_data_dict.keys())
    hourly_axis_data = weather_data_dict['hourly']
    time_axis_data = hourly_axis_data['time']
    temperature_axis_data = hourly_axis_data['temperature_2m']
    date_list_string = [date_string.split("T")[0] for date_string in time_axis_data]
    # dates_list = [datetime.strptime(date, "%Y-%m-%dT%H:%M").date() for date in time_axis_data]
    len_array = len(date_list_string)
    result_list = []
    for i in range(len_array):
        temp_dict = {}
        # print(date_list_string[i])
        date_string = date_list_string[i]
        date_string = date_string + " 00:00:00"
        temperature_value = temperature_axis_data[i]
        temp_dict["y"] = temperature_value
        temp_dict["x"] = date_string
        result_list.append(temp_dict)
    # print(result_list)

    with open("saved_data_weather.json", "w") as jsonFile:
        json.dump(result_list, jsonFile)

    with open('saved_data_weather.json', 'r') as openfile:
        saved_data_weather = json.load(openfile)


    return render_template("weather.html", saved_data_weather=saved_data_weather)

@home.route('/graphwindow')
def graphwindow():
    graph_data = [{"y": 4, "x": "2017-01-01 00:00:00"},
     {"y": 0, "x": "2017-01-02 00:00:00"},
     {"y": 9, "x": "2017-01-03 00:00:00"},
     {"y": 0, "x": "2017-01-04 00:00:00"},
     {"y": 14, "x": "2017-01-05 00:00:00"}]
    URL = 'https://api.open-meteo.com/v1/forecast?latitude=51.16&longitude=71.43&hourly=temperature_2m'
    request = requests.get(URL)
    weather_data_dict = request.json()
    print(weather_data_dict['hourly'])
    data_temp_time = weather_data_dict['hourly']['time']
    temperature_2m = weather_data_dict['hourly']['temperature_2m']
    print(data_temp_time)


    with open("saved_data.json", "w") as jsonFile:
        json.dump(graph_data, jsonFile)

    with open('saved_data.json', 'r') as openfile:
        saved_data = json.load(openfile)

    return render_template('graph_window.html', saved_data=saved_data)


# @home.route('/')
# def home_view():
    # request = requests.get('http://api.open-notify.org')
    # people = requests.get('http://api.open-notify.org/astros.json')
    # people_json = people.json()
    # To print the number of people in space
    # print("Number of people in space:", people_json['number'])
    # To print the names of people in space using a for loop
    # for p in people_json['people']:
    #    print(p['name'])

    # parameter = {"rel_rhy": "jingle"}
    # request = requests.get('https://api.datamuse.com/words', parameter)
    # rhyme_json = request.json()
    # for i in rhyme_json[0:3]:
        # print(i['word'])

    # return render_template('home.html')
    # return render_template(request.text)

@home.route('/graph_load_ajaxfile', methods=["POST", "GET"])
def graph_load_ajaxfile():
    if request.method == 'POST':

        return jsonify({'htmlresponse': render_template('graph_window.html')})
        # return redirect('/dash/')

