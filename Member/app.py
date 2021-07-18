from flask import Flask, render_template, request
import vo, model

app = Flask(__name__)
mem_service = model.MemService()

@app.route('/')
def home():
    return render_template('index.html')

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
    return render_template('index.html')

@app.route('/Member/get', methods=['POST'])
def get():
    id = request.form.get('id', 0, int)
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
    return render_template('index.html')

@app.route('/Member/del')
def delete():
    id = request.args.get('id', '', str)
    mem = mem_service.delMem(id)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

