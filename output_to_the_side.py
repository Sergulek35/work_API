from flask import Flask, render_template, request
from hh import area, hh_parce
import os
from download_functions import add_history, show_history, dell_history
import sqlite3
import json

print_area = sorted(area.keys())
app = Flask(__name__)

record = []


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/history/", methods=['GET'])
def history_get():
    if show_history():

        return render_template('history.html', history=show_history())
    else:
        history_no = 'Здесь будет история запросов'
        return render_template('history.html', history_no=history_no)


@app.route("/history/", methods=['POST'])
def history_post():
    if request.form['clear']:
        dell_history()
    return render_template('index.html')


@app.route('/search/')
def search():
    return render_template('search.html', area=print_area)


@app.route("/run/", methods=['GET'])
def run_get():
    return render_template('search.html', area=print_area)


@app.route("/run/", methods=['POST'])
def run_post():
    try:
        vykansiya = request.form['vykansiya']
        area_persons = request.form['area_persons'].lower()
        time_persons = int(request.form['time_persons'])
        user_input = hh_parce(vykansiya, area_persons, time_persons)

        return render_template('results.html', **user_input)

    except KeyError:
        text_Key = 'Неверно введён город...'
        return render_template('error.html', text_Key=text_Key)

    except ZeroDivisionError:
        text_Zero = 'Вакансии не найдено или ошибка ввода...'
        return render_template('error.html', text_Zero=text_Zero)


@app.route("/results/", methods=['POST'])
def results_post():
    if request.form['save']:
        add_history()

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
