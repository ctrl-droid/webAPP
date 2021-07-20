from flask import Flask, render_template, request, redirect, session
import model

app = Flask(__name__)
mem_service = model.MemService()
app.secret_key = 'affdasdf'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Member/login')
def login_form():
    return render_template('member/login.html')

@app.route('/Member/login', methods=['POST'])
def login():
    msg = ''   #로그인 상태 메시지 저장
    path = 'member/login.html'   #처리 완료 후 이동할 페이지의 경로
    #로그인 폼에서 입력 값 받음
    id = request.form['id']
    pwd = request.form['pwd']
    #입력받은 id로 검색
    m = mem_service.getMem(id)
    if m == None:
        msg = '없는 아이디'
    else:
        if pwd == m.pwd:
            session['id']=id  #로그아웃할떄까지 유지해야하는 정보를 저장
            path = 'index.html'
            msg = '로그인 성공'
        else:
            msg ='패스워드 불일치'
    return render_template(path, msg=msg)

@app.route('/Member/logout')
def logout():
    if 'id' in session:  #세션에서 id라는 키가 있냐?
        session.pop('id', None)   #세션에서 id키 삭제제    return redirect('/')

@app.route('/Member/add')
def add_form():
    return render_template('member/add_form.html')

@app.route('/Member/add', methods=['POST'])
def add_mem():
    id = request.form.get('id', '', str)
    pwd = request.form.get('pwd', '', str)
    name = request.form.get('name', '', str)
    email = request.form.get('email', '', str)

    mem = model.MemberVo(id=id, pwd=pwd, name=name, email=email)
    mem_service.addMem(mem)
    return redirect('/')

@app.route('/Member/get', methods=['POST'])
def get():
    id = request.form.get('id', '', str)
    mem = mem_service.getMem(id)
    if mem==None:
        return '없는 ID입니다.'
    else:
        return render_template('member/detail.html', mem=mem)

@app.route('/Member/get', methods=['POST', 'GET'])
def getMember():
    if request.method == 'POST':
        id = request.form['id']
    else:
        id = request.args.get('id', '',str)

    mem = mem_service.getMem(id)
    if mem==None:
        return '없는 ID입니다.'
    else:
        return render_template('member/detail.html', mem=mem)

@app.route('/Member/list')
def list():
    mems = mem_service.getAll()
    return render_template('member/list.html', mems=mems)

@app.route('/Member/detail')
def get_mem():
    id = request.args.get('id', '', str)
    mem = mem_service.getMem(id)
    if mem==None:
        return '없는 ID입니다'
    else:
        return render_template('member/detail.html', mem=mem)

@app.route('/Member/edit')  #수정폼: /Member/edit?id=
def edit_form():
    id = request.args.get('id', '', str)
    mem = mem_service.getMem(id)
    if mem == None:
        return '없는 ID입니다'
    else:
        return render_template('member/edit_form.html', mem=mem)

@app.route('/Member/edit', methods=['POST']) #수정완료
def edit():
    id = request.form.get('id', '', str)
    new_pwd = request.form.get('pwd', '', str)

    mem = model.MemberVo(pwd=new_pwd, id=id)
    mem_service.editMem(new_pwd, id)
    return redirect('/')

@app.route('/Member/del')
def delete():
    id = request.args.get('id', '', str)
    mem_service.delMem(id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

