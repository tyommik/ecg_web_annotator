import json

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Flask, render_template, redirect, url_for, make_response, jsonify, request

from utils import read_mit_data
from app import db

from rtypes import types_mapping, default_data

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    user = current_user.name
    return render_template('index.html', user=user)


@main.route('/admin')
@login_required
def admin():
    user = current_user.name
    if user == 'admin':
        return render_template('admin.html')
    else:
        return redirect(url_for('main.index'))


@main.route('/howto')
@login_required
def howto():
    user = current_user.name
    user_score = db.count_done_by_user(user)
    total = len(db)
    user_precent = round((user_score / total) * 100, 2)
    return render_template('howto.html', user=user, score=user_score, total_score=total, user_precent=user_precent)


@main.route('/profile')
@login_required
def profile():
    user = current_user.name
    user_score = db.count_done_by_user(user)
    total = len(db)
    user_percentage = round((user_score / total) * 100, 2)

    total_done = db.count_done()
    percentage = round((total_done / total) * 100, 2)
    return render_template('profile.html',
                           user=user,
                           score=user_score,
                           total_score=total,
                           user_percentage=user_percentage,
                           total_done=total_done,
                           percentage=percentage

                           )


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

    ecglist = db.query_holded_list(length=50, user=user)
    if request.args.get('new'):
        db.unhold_list(ecglist, user=user)
        ecglist = db.query_new_list()
        db.hold_list(ecglist, user=user)
    data = [{"id": idx, "rank": rank, "title": timestamp} for idx, (rank, timestamp) in enumerate(ecglist)]
    return make_response(jsonify(data), 200)


@main.route('/getlistdone', methods=['get'])
@login_required
def getlistdone():

    """
    Admin method to get all marked ecgs by patients
    """
    user = current_user.name
    if user == 'admin':
        ecglist = db.query_done_list(length=500, user=user)
        data = [{"id": idx, "rank": rank, "title": timestamp, "patient_id": patient_id, "done": isDone, "user": user} for idx, (rank, patient_id, isDone, user, timestamp) in enumerate(ecglist)]
        return make_response(jsonify(data), 200)
    else:
        return make_response(jsonify([]), 403)


@main.route('/leads/<int:index>', methods=['get'])
@login_required
def getleads(index):
    request = db.query(index)
    ecg_path = request.get("path")
    if ecg_path:
        ecg_path = "data/" + ecg_path[:-4]
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
    form = request.form
    if form:
        try:
            txt = list(form.keys())[0]
            data = json.loads(txt)
        except json.decoder.JSONDecodeError as err:
            return make_response(jsonify("", 500))
        else:

            for group in data:
                for view in group["group_data"]:
                    view["label"] = types_mapping[view["name"]]
            db.update_anno(index, current_user.name, json.dumps(data))
    return make_response(jsonify("", 200))


@main.route('/anno/<int:index>', methods=['GET'])
@login_required
def getanno(index):
    request = db.query(index)
    sex = "Мужской" if request['sex'] else "Женский"
    age = request['age']
    report = f"Пол: {sex}, возраст: {age}.<br><br><b>Заключение врача:</b> {request['report']}" \
        if request['report'] else f"Пол: {sex}, возраст: {age}.<br><br><b>Заключение врача остутствует</b>"

    request = db.query_anno(index)
    data = json.loads(request.get("anno"))

    if not data:
        data = default_data.copy()
    else:
        data = json.loads(data)

    return make_response(jsonify({'data': data, 'report': report}), 200)