from flask import Flask, render_template, request
import model

app = Flask(__name__)
mem_service = model.MemService()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Member/add')
def add_form():
    return render_template('Member/add_form.html')

@app.route('/Member/add', methods=['POST'])
def add_mem():
    id = request.form.get('id', '', str)
    pwd = request.form.get('pwd', '', str)
    name = request.form.get('name', '', str)
    email = request.form.get('email', '', str)

    mem = model.MemberVo(id=id, pwd=pwd, name=name, email=email)
    mem_service.addMem(mem)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

