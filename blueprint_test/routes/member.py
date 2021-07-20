from flask import Blueprint
bp = Blueprint('member', __name__, url_prefix='/Member') #url 생성기 Blueprint(이름, 모듈명, 기본 url)

@bp.route('/join')
def join():
    return 'join'

@bp.route('/login')
def login():
    return 'login'