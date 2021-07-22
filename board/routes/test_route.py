from flask import Blueprint, render_template, request, redirect, session
import matplotlib.pyplot as plt

bp = Blueprint('test', __name__, url_prefix='/test')  #url 생성기


@bp.route('/graph')
def graph():
    img_path = 'static/graph/my_plot.png'

    x = [1, 2, 3, 4]
    y = [3, 8, 5, 6]
    fig, ax = plt.subplots()  #그래프 그릴 플랏 생성. fig=그림, ax=축
    plt.plot(x, y)   #그래프 그림
    fig.savefig(img_path)  #이미지 저장할 경로
    img_path = '/' + img_path   #절대경로때문에 / 붙여줌
    return render_template('test/test.html', img_path=img_path)

@bp.route('/upload')
def upload_form():
    return render_template('test/form.html')

@bp.route('/upload', methods=['POST'])
def upload():
    upload_path = 'static/img/'
    f = request.files['file']
    fname = upload_path+f.filename
    f.save(fname)   #26번 줄에서 보낸 파일을 저장하는 명령문
    fname = '/' + fname
    return render_template('test/test.html', img_path=fname)



