from flask import Blueprint, url_for, jsonify
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

import random
# from flask import render_template

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
