from flask import Blueprint, url_for, jsonify, render_template
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

import random

n = 1

@bp.route('/')
def hello_pybo():

    abab = random.randint(1, 100)
    print(abab)
    print(3)
    global n
    n += 1
    # return render_template('question/new.html', club = abab)
    return jsonify({"index": n, "value": abab})

@bp.route('/hello')
def index():
    return redirect(url_for('question._list'))

@bp.route('/show', methods=['GET', 'POST'])
def show():
    imagine = 'one.png'
    return render_template('question/show.html', img=imagine)