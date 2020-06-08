import json

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Flask, render_template, redirect, url_for, make_response, jsonify, request

from utils import read_mit_data

# from . import db

from app import db

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    user = current_user.name
    user_score = db.count_done_by_user(user)
    total = len(db)
    user_precent = round((user_score / total) * 100, 2)
    return render_template('profile.html', user=user, score=user_score, total_score=total, user_precent=user_precent)


@main.route('/stats')
@login_required
def stats():
    done = db.count_done()
    total = len(db)
    precent = round((done / total) * 100, 2)
    return render_template('stats.html', done=done, total=total, percent=precent)


@main.route('/getlist', methods=['get'])
@login_required
def getlist():
    user = current_user.name

    ecglist = db.query_holded_list(length=10, user=user)
    if request.args.get('new'):
        db.unhold_list(ecglist, user=user)
        ecglist = db.query_new_list(5)
        db.hold_list(ecglist,user=user)
    data = [{"id": idx, "rank": num, "title": "экг"} for idx, num in enumerate(ecglist)]
    return make_response(jsonify(data), 200)


@main.route('/leads/<int:index>', methods=['get'])
@login_required
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
        user = current_user.name
        db.mask_as_done(index, user)
        return make_response(jsonify({'data': {}}), 200)
    else:
        return make_response(jsonify({'data': leads}), 500)


@main.route('/anno/<int:index>', methods=['POST'])
@login_required
def setanno(index):

    # name -> расшифровка
    types_mapping = {
        "1": ("(N)Нормальный ритм"),
        "2": ("Синусовая тахикардия"),
        "3": ("Синусовая брадикардия"),
        "4": ("Экстрасистолия"),
        "5": ("Синусовая аритмия"),
        "6": ("Трепетание предсердий"),
        "7": ("Фибрилляция предсердий"),
        "8": ("Трепетание и фибрилляция желудочков"),

        "11": ("Атриовентрикулярная блокада I"),
        "12": ("Атриовентрикулярная блокада II"),
        "13": ("Атриовентрикулярная блокада III"),
        "14": ("(БЛНПГ)Блокада левой ножки пучка Гиса"),
        "15": ("(НБЛНПГ)Неполная блокада левой ножки пучка Гиса"),
        "16": ("(ПБПНПГ)Полная блокада правой ножки пучка Гиса"),
        "17": ("(НБПНПГ)Неполная блокада правой ножки пучка Гиса"),

        "21": ("Гипертрофия левого желудочка"),
        "22": ("Гипертрофия правого желудочка"),
        "23": ("Гипертрофия левого предсердия"),
        "24": ("Гипертрофия правого предсердия"),
        "25": ("Ишемия миокарда"),
        "26": ("Инфаркт миокарда")
    }

    form = request.form
    if form:
        try:
            txt = list(form.keys())[0]
            data = json.loads(txt)
        except json.decoder.JSONDecodeError as err:
            return make_response(jsonify("", 500))
        else:

            for group in data:
                for checkbox in group["group_data"]:
                    checkbox["label"] = types_mapping[checkbox["name"]]
            db.update_anno(index, current_user.name, json.dumps(data))
    return make_response(jsonify("", 200))


@main.route('/anno/<int:index>', methods=['GET'])
def getanno(index):
    request = db.query(index)
    report = request['report'] if request['report'] else "Заключение остутствует"

    request = db.query_anno(index)
    data = json.loads(request.get("anno"))

    if not data:

        data = [
            {'group_label': "Ритм сердца",
              'group_data': [{"view": "checkbox", "label": "(N)Нормальный ритм", "value": 0, "name": "1"},
                             {"view": "checkbox", "label": "Синусовая тахикардия", "value": 0, "name": "2"},
                             {"view": "checkbox", "label": "Синусовая брадикардия", "value": 0, "name": "3"},
                             {"view": "checkbox", "label": "Экстрасистолия", "value": 0, "name": "4"},
                             {"view": "checkbox", "label": "Синусовая аритмия", "value": 0, "name": "5"},
                             {"view": "checkbox", "label": "Трепетание предсердий", "value": 0, "name": "6"},
                             {"view": "checkbox", "label": "Фибрилляция предсердий", "value": 0, "name": "7"},
                             {"view": "checkbox", "label": "Трепетание и фибрилляция желудочков", "value": 0, "name": "8"}

                             ]},
            {'group_label': "Нарушения функции проводимости",
              'group_data': [{"view": "checkbox", "label": "Атриовентрикулярная блокада I", "value": 0, "name": "11"},
                             {"view": "checkbox", "label": "Атриовентрикулярная блокада II", "value": 0, "name": "12"},
                             {"view": "checkbox", "label": "Атриовентрикулярная блокада III", "value": 0, "name": "13"},
                             {"view": "checkbox", "label": "(БЛНПГ)Блокада левой ножки пучка Гиса", "value": 0, "name": "14"},
                             {"view": "checkbox", "label": "(НБЛНПГ)Неполная блокада левой ножки пучка Гиса", "value": 0,
                              "name": "15"},
                             {"view": "checkbox", "label": "(ПБПНПГ)Полная блокада правой ножки пучка Гиса", "value": 0, "name": "16"},
                             {"view": "checkbox", "label": "(НБПНПГ)Неполная блокада правой ножки пучка Гиса", "value": 0,
                              "name": "17"}
                             ]},
            {'group_label': "Другие Показатели",
              'group_data': [{"view": "checkbox", "label": "Гипертрофия левого желудочка", "value": 0, "name": "21"},
                             {"view": "checkbox", "label": "Гипертрофия правого желудочка", "value": 0, "name": "22"},
                             {"view": "checkbox", "label": "Гипертрофия левого предсердия", "value": 0, "name": "23"},
                             {"view": "checkbox", "label": "Гипертрофия правого предсердия", "value": 0, "name": "24"},
                             {"view": "checkbox", "label": "Ишемия миокарда", "value": 0, "name": "25"},
                             {"view": "checkbox", "label": "Инфаркт миокарда", "value": 0, "name": "26"},
                             ]}

    ]
    else:
        data = json.loads(data)

    return make_response(jsonify({'data': data, 'report': report}), 200)