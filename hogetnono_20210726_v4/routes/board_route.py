from flask import Blueprint, render_template, request, redirect, session
import hogetnono.models.board as board
import hogetnono.models.transaction as tr

bp = Blueprint('board', __name__, url_prefix='/board')  #url 생성기
board_service = board.BoardService()
transaction_service = tr.TransactionService

@bp.route('/list')
def list():
    aptinfo_sn = request.args.get('sn', '', str)
    boards = board_service.board_select_sn(aptinfo_sn)
    return render_template('board/list.html', boards=boards, sn=aptinfo_sn)

@bp.route('/add')
def add_form():
    aptinfo_sn = request.args.get('sn', '', str)
    return render_template('/board/add.html', sn=aptinfo_sn)

@bp.route('/add', methods = ['POST'])
def add():
    title = request.form['title']
    content = request.form['content']
    member_id = request.form['member_id']
    aptinfo_sn = request.form['aptinfo_sn']
    boards = board.Board(title=title, content=content, member_id=member_id, aptinfo_sn=aptinfo_sn)
    board_service.board_insert(boards)
    return redirect('/board/list?sn='+aptinfo_sn)

@bp.route('get_title')
def get_title():
    title = request.form['title']
    boards = board_service.board_select_title(title)
    return render_template('/board/list.html', boards=boards)

@bp.route('get_member_id')
def get_member_id():
    member_id = request.args.get('member_id', '', str)
    boards = board_service.board_select_member_id(member_id)
    return render_template('board/list.html', boards=boards)

@bp.route('get_content')
def get_content():
    content = request.args.get('content', '', str)
    boards = board_service.board_select_member_id(content)
    return render_template('board/list.html', boards=boards)




