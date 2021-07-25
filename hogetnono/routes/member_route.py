from flask import Blueprint, render_template, request, redirect, session
import hogetnono.models.member as mem

bp = Blueprint('member', __name__, url_prefix='/member')  #url 생성기
member_service = mem.MemberService()

@bp.route('/login')
def login_form():
    return render_template('member/login.html')

@bp.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    pwd = request.form['pwd']
    member = member_service.getMember(id)
    if member == None:
        msg = '가입된 계정이 없습니다.'
    else:
        if pwd == member.pwd:
            session['id'] = id
            return redirect('/')
        else:
            msg = '패스워드가 일치하지 않습니다.'
    return render_template('member/login.html', msg=msg)

@bp.route('/join')
def join_form():
    return render_template('member/join.html')

@bp.route('/join', methods=['POST'])
def join():
    id = request.form['id']
    pwd = request.form['pwd']
    name = request.form['name']
    tel = request.form['tel']
    members = mem.Member(id=id, pwd=pwd, name=name, tel=tel)
    member_service.addMember(members)
    return redirect('/member/login')

@bp.route('/logout')
def logout():
    if 'id' in session:
        session.pop('id', None)
    return redirect('/')

@bp.route('/get')
def get():
    if 'id' in session:
        id = session['id']
        member = member_service.getMember(id)
    else:
        return '로그인이 안되있습니다'
    return render_template('member/detail.html', member=member)

@bp.route('/edit')
def edit_form():
    id = request.args.get('id', '', str)
    print(id)
    member = member_service.getMember(id)
    return render_template('member/edit.html', member=member)

@bp.route('/edit', methods=['POST'])
def edit():
    id = request.form['id']
    pwd = request.form['pwd']
    tel = request.form['tel']
    member = mem.Member(id=id,pwd=pwd,tel=tel)
    member_service.editMember(member)
    return redirect('/member/get')

@bp.route('/del')
def delete():
    if 'id' in session:
        id = session['id']
    member_service.deleteMember(id)
    session.pop('id', None)
    return redirect('/')

