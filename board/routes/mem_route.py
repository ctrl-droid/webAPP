#/member/관련 url 등록

from flask import Blueprint, render_template, request, redirect, session
import board.models.member as mem

bp = Blueprint('member', __name__, url_prefix='/member')  #url 생성기
memService = mem.MemService()

@bp.route('/join')
def join_form():
    return render_template('member/join.html')

@bp.route('/join', methods=['POST'])
def join():
    id = request.form['id']
    pwd = request.form['pwd']
    name = request.form['name']
    email = request.form['email']
    m = mem.Member(id, pwd, name, email)
    memService.addMember(m)
    return redirect('/')

@bp.route('/login')
def login_form():
    return render_template('member/login.html')

@bp.route('/login', methods=['POST'])
def login():
    msg = ''  # 로그인 상태 메시지 저장
    path = 'member/login.html'  # 처리 완료 후 이동할 페이지의 경로

    # 로그인 폼에서 입력 값 받음
    id = request.form['id']
    pwd = request.form['pwd']

    # 입력받은 id로 검색
    m = memService.getMember(id)
    if m == None:
        msg = '없는 아이디'
    else:
        if pwd == m.pwd:
            session['id'] = id  # 로그아웃할때까지 유지해야하는 정보를 저장
            path = 'index.html'
            msg = '로그인 성공'
        else:
            msg = '패스워드 불일치'
    return render_template(path, msg=msg)

@bp.route('/logout')
def logout():
    if 'id' in session:  #세션에 id라는 키가 있냐?
        session.pop('id', None) #세션에서 id키 삭제
    return redirect('/')

@bp.route('/getmember')#로그인 한 사람 정보 검색
def getMember():
    if 'id' in session:
        id = session['id']
        m = memService.getMember(id)
    else:
        return '로그인 먼저'

    return render_template('member/detail.html', mem=m)

@bp.route('/edit', methods=['POST'])
def edit():
    id = request.form['id']
    pwd = request.form['pwd']
    m = mem.Member(id=id, pwd=pwd)
    memService.editMember(m)
    return redirect('/')

@bp.route('/del')
def delete():
    if 'id' in session:
        id = session['id']
    memService.delMember(id)
    session.pop('id', None)
    return redirect('/')
