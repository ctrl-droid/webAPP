from flask import Blueprint, render_template, request, redirect, session
import matplotlib.pyplot as plt
import os

bp = Blueprint('test', __name__, url_prefix='/test')  #url 생성기


@bp.route('/graph')
def graph():
    img_path = 'static/graph/my_plot.png'

    x = [1, 2, 3, 4]
    y = [3, 8, 5, 6]
    fig, _ = plt.subplots() #그래프 그릴 플랏 생성
    plt.plot(x, y) #그래프 그림
    fig.savefig(img_path) #그래프 이미지 파일로 저장
    img_path = '/' + img_path
    return render_template('test/test.html', img_path=img_path)

@bp.route('/upload')
def upload_form():
    return render_template('test/form.html')

@bp.route('/upload', methods=['POST'])
def upload():
    upload_path = 'static/img/'
    f = request.files['file']
    fname = upload_path+f.filename
    f.save(fname)
    fname = '/' + fname
    return render_template('test/test.html', img_path=fname)

@bp.route('/upload2', methods=['POST'])
def upload2():
    upload_path = 'static/img/'
    f = request.files['file']
    fname = upload_path+f.filename
    f.save(fname)
    title = request.form['title']
    print(title)

    return '업로드 완료'

@bp.route('/list')
def list():
    path = 'static/img/'
    files = os.listdir(path)
    print(files)
    return render_template('test/list.html', files=files)





