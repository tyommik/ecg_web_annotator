import base64
from io import BytesIO
import json

import wfdb
from flask import Flask, render_template, redirect, url_for, make_response, jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

from utils import read_mit_data
import rtypes

from database import Database

SECRET_KEY = 'development'
app = Flask(__name__)
app.config.from_object(__name__)

from app import create_app


@app.route('/stats', methods=['GET'])
def stats():
    pass

@app.route('/',methods=['post','get'])
def hello_world():
    return render_template('index.html')


@app.route('/getlist', methods=['get'])
def getlist():
    ecglist = db.query_holded_list()
    if request.args.get('new'):
        db.unhold_list(ecglist)
        ecglist = db.query_new_list(5)
        db.hold_list(ecglist)
    data = [{"id": idx, "rank": num, "title": "экг"} for idx, num in enumerate(ecglist)]
    return make_response(jsonify(data), 200)


@app.route('/leads/<int:index>', methods=['get'])
def getleads(index):
    request = db.query(index)
    ecg_path = request.get("path")
    if ecg_path:
        ecg_path = "data/" + ecg_path[:-4]
    # if request['done'] is True:
    #     return make_response(jsonify({'data': {}}), 200)

    try:
        leads = read_mit_data(ecg_path)
        leads = [lead.tolist() for lead in leads]
    except FileNotFoundError as err:
        db.mask_as_done(index)
        return make_response(jsonify({'data': {}}), 200)
    else:
        return make_response(jsonify({'data': leads}), 500)


@app.route('/anno/<int:index>', methods=['POST'])
def setanno(index):

    # name -> расшифровка
    types_mapping = {
        "norm": ("(N)Нормальный ритм", "Ритм сердца"),
        "tah": ("Синусовая тахикардия", "Ритм сердца"),
        "brad": ("Синусовая брадикардия", "Ритм сердца"),
        "extrasys": ("Экстрасистолия", "Ритм сердца"),
        "aritm": ("Синусовая аритмия", "Ритм сердца"),
        "trepred": ("Трепетание предсердий", "Ритм сердца"),
        "afib": ("Фибрилляция предсердий", "Ритм сердца"),
        "vfib": ("Трепетание и фибрилляция желудочков", "Ритм сердца"),

        "atrio1": ("Атриовентрикулярная блокада I", "Нарушения функции проводимости"),
        "artio2": ("Атриовентрикулярная блокада II", "Нарушения функции проводимости"),
        "atrio3": ("Атриовентрикулярная блокада III", "Нарушения функции проводимости"),
        "lgis": ("(БЛНПГ)Блокада левой ножки пучка Гиса", "Нарушения функции проводимости"),
        "nlgis": ("(НБЛНПГ)Неполная блокада левой ножки пучка Гиса", "Нарушения функции проводимости"),
        "pgis": ("(ПБПНПГ)Полная блокада правой ножки пучка Гиса", "Нарушения функции проводимости"),
        "npgis": ("(НБПНПГ)Неполная блокада правой ножки пучка Гиса", "Нарушения функции проводимости"),

        "glj": ("Гипертрофия левого желудочка", "Другие Показатели"),
        "gpj": ("Гипертрофия правого желудочка", "Другие Показатели"),
        "glp": ("Гипертрофия левого предсердия", "Другие Показатели"),
        "gpp": ("Гипертрофия правого предсердия", "Другие Показатели"),
        "ishmio": ("Ишемия миокарда", "Другие Показатели"),
        "inmio": ("Инфаркт миокарда", "Другие Показатели")
    }



    form = request.form
    if form:
        pass

    db.update_anno(index, {})

    return make_response(jsonify("", 200))


@app.route('/anno/<int:index>', methods=['GET'])
def getanno(index):
    request = db.query(index)
    report = request['report'] if request['report'] else "Заключение остутствует"

    request = db.query_anno(index)
    data = json.loads(request.get("anno"))

    if not data:

        data = [
            {'group_label': "Ритм сердца",
              'group_data': [{"view": "checkbox", "label": "(N)Нормальный ритм", "value": 0, "name": "one"},
                             {"view": "checkbox", "label": "Синусовая тахикардия", "value": 0, "name": "two"},
                             {"view": "checkbox", "label": "Синусовая брадикардия", "value": 0, "name": "three"},
                             {"view": "checkbox", "label": "Экстрасистолия", "value": 0, "name": "five"},
                             {"view": "checkbox", "label": "Синусовая аритмия", "value": 0, "name": "six"},
                             {"view": "checkbox", "label": "Трепетание предсердий", "value": 0, "name": "seven"},
                             {"view": "checkbox", "label": "Фибрилляция предсердий", "value": 0, "name": "eight"},
                             {"view": "checkbox", "label": "Трепетание и фибрилляция желудочков", "value": 0, "name": "nine"}

                             ]},
            {'group_label': "Нарушения функции проводимости",
              'group_data': [{"view": "checkbox", "label": "Атриовентрикулярная блокада I", "value": 0, "name": "one"},
                             {"view": "checkbox", "label": "Атриовентрикулярная блокада II", "value": 0, "name": "two"},
                             {"view": "checkbox", "label": "Атриовентрикулярная блокада III", "value": 0, "name": "three"},
                             {"view": "checkbox", "label": "(БЛНПГ)Блокада левой ножки пучка Гиса", "value": 0, "name": "three"},
                             {"view": "checkbox", "label": "(НБЛНПГ)Неполная блокада левой ножки пучка Гиса", "value": 0,
                              "name": "three"},
                             {"view": "checkbox", "label": "(ПБПНПГ)Полная блокада правой ножки пучка Гиса", "value": 0, "name": "three"},
                             {"view": "checkbox", "label": "(НБПНПГ)Неполная блокада правой ножки пучка Гиса", "value": 0,
                              "name": "three"}
                             ]},
            {'group_label': "Другие Показатели",
              'group_data': [{"view": "checkbox", "label": "Гипертрофия левого желудочка", "value": 0, "name": "one"},
                             {"view": "checkbox", "label": "Гипертрофия правого желудочка", "value": 0, "name": "two"},
                             {"view": "checkbox", "label": "Гипертрофия левого предсердия", "value": 0, "name": "three"},
                             {"view": "checkbox", "label": "Гипертрофия правого предсердия", "value": 0, "name": "three"},
                             {"view": "checkbox", "label": "Ишемия миокарда", "value": 0, "name": "three"},
                             {"view": "checkbox", "label": "Инфаркт миокарда", "value": 0, "name": "three"},
                             ]}

    ]

    return make_response(jsonify({'data': data, 'report': report}), 200)



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)