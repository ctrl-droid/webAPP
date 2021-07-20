#/board/ 관련된 url 등록

from flask import Blueprint, render_template, request, redirect, session
import board.models.board as b

bp = Blueprint('board', __name__, url_prefix='/board')  #url 생성기
boardService = b.BoardService()

@bp.route('/add')
def add_form():
    return render_template('board/form.html')

@bp.route('/add', methods=['POST'])
def add():
    id = request.form['id']
    title = request.form['title']
    content = request.form['content']
    bb = b.Board(writer=id, title=title, content=content)
    boardService.addBoard(bb)
    return redirect('/board/list')

@bp.route('/list')
def list():
    boards = boardService.getAll()
    return render_template('board/list.html', boards = boards)

@bp.route('/edit')
def edit_form():
    num = request.args.get('num', 0, int)
    board = boardService.getNum(num)
    return render_template('board/detail.html', board=board)

@bp.route('/edit', methods=['POST'])
def edit():
    num = request.form['num']
    title = request.form['title']
    content = request.form['content']

    board = b.Board(num=num, title=title, content=content)
    boardService.editBoard(board)
    return redirect('/board/list')

@bp.route('/del')
def delete():
    num = request.args.get('num', 0, int)
    boardService.delBoard(num)
    return redirect('/board/list')
