from flask import Blueprint, url_for, jsonify, render_template, request
from werkzeug.utils import redirect
import os

bp = Blueprint('main', __name__, url_prefix='/')

import random

n = 1

# 업로드된 파일을 저장할 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 파일 확장자가 허용된 확장자인지 확인하는 함수
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#########################################################

@bp.route('/', methods=['GET', 'POST'])
def hello_pybo():

    abab = random.randint(1, 1000)
    print(abab)
    print(3)
    global n
    n += 1
    # return render_template('question/new.html', club = abab)
    return jsonify({"index": n, "value": abab})



@bp.route('/hello', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ddata = request.json
        print("ddata : ", ddata)
    return ddata
    # return redirect(url_for('question._list'))

@bp.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # 업로드된 파일을 확인
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # 파일이 비어있는지 확인
        if file.filename == '':
            return redirect(request.url)

        # 파일이 허용된 확장자인지 확인
        if file and allowed_file(file.filename):
            # 파일을 업로드할 디렉토리 생성
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            # 파일을 저장
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            return '파일 업로드 완료'

    return render_template('upload.html')

@bp.route('/show', methods=['GET', 'POST'])
def show():
    imagine = 'one.png'
    return render_template('show.html', img=imagine)