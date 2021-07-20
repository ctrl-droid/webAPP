# /board/관련 url 등록

from flask import Blueprint, render_template, request, session, redirect
import board.models.board as b

bp = Blueprint('member', __name__, url_prefix='/board') #url 생성기 Blueprint(이름, 모듈명, 기본 url)
boardService = b.BoardService()

@bp.route('/add')
def add_form():
    return render_template('board/form.html')

@bp.route('/add', methods=['POST'])
def add():
    writer = request.form['writer']
    title = request.form['title']
    content = request.form['content']

    bb = b.Board(writer=id, title=title, content=content)
    boardService.addBoard(bb)
    return redirect('/board/list')

@bp.route('/list')
def list():
    boards = boardService.getAll()
    return render_template('board/list.html', boards=boards)

