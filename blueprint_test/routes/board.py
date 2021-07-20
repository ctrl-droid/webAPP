from flask import Blueprint
bp = Blueprint('board', __name__, url_prefix='/board')

@bp.route('/list')
def join():
    return '글목록'

@bp.route('/write')
def login():
    return 'write'