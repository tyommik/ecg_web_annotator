from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField

from database import Database

import base64
from io import BytesIO

SECRET_KEY = 'development'
app = Flask(__name__)
app.config.from_object(__name__)

table_idx = 0

BD = Database(csv_file='dynamic_no_fibr.csv')


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG')
    img_io.seek(0)
    return img_io

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SimpleForm(FlaskForm):

    # create a list of value/description tuples
    rhythm = [(x, x) for x in ('Синусовая Тахикардия',
                               'Синусовая брадикардия',
                               'Синусовая аритмия',
                               'Экстасистолия',
                               'ФП',
                               'Трепетание Предсердий',
                               'Трепетание желудочков',
                               'Фибр желудочков')
              ]
    #rhythm = [(x, x) for x in list_of_files]
    norma = MultiCheckboxField('Normal', choices=[('norm', 'Нормальный(синусовый) ритм')])
    rhythm = MultiCheckboxField('Rhythm', choices=rhythm)
    blocks = MultiCheckboxField('Blocks', choices=[('Блокада', 'Блокада')])
    hypertrophy = MultiCheckboxField('Hypertrophy', choices=[('Гипертрофия', 'Гипертрофия')])
    skip = MultiCheckboxField('Blocks', choices=[('Без заключения', 'Без заключения')])

@app.route('/',methods=['post','get'])
def hello_world():

    global table_idx
    form = SimpleForm()
    total = BD.getTotal()
    if form.validate_on_submit():
        print(form.data)
        # return render_template("success.html", norma=form.norma.data, rhythm=form.rhythm.data, blocks=form.blocks.data)
        BD.send(table_idx, form.data)
        return redirect(url_for('hello_world'))
    else:
        print("Validation Failed")
        print(form.errors)
        table_idx, diagnosis, img = BD.getNext()
        # img = serve_pil_image(img)
        b64 = base64.b64encode(img.getvalue()).decode()
        info = f'Обработано {table_idx} / {total} или {round(table_idx / total * 100, 2)} процентов'
    print(table_idx, diagnosis)
    return render_template('hello.html',diagnosis=diagnosis, form=form, info=info, image = b64)


if __name__ == '__main__':
    app.run(debug=True)