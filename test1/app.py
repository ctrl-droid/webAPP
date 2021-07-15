from flask import Flask, render_template, request
#render_template : 뷰 페이지 만들어 주는 애

app = Flask(__name__)   #플라스크 객체 생성: 플라스크 제공 기능을 사용하려면 객체 필요

#요청을 받아서 처리할 url 등록: @app.route()
@app.route('/')  #시작 페이지
def root():
    return render_template('index.html')  #뷰 페이지 실행

@app.route('/member/join')
def join_form():
    return render_template('member/join.html')

@app.route('/member/login')
def login_form():
    return render_template('member/login.html')

@app.route('/get-test')    # methods=['GET']
def get_test():
    id = request.args.get('id','',str)
    pwd = request.args.get('pwd', '', str)
    return id +' /'+pwd

@app.route('/member/login', methods=['POST'])
def login():
    id = request.form['id']
    pwd = request.form['pwd']
    return render_template('/member/login_result.html',id=id, pwd=pwd)

@app.route('/view-test1')
def view_test1():
    id = 'aaa'
    pwd = '111'
    return render_template('test1.html', a=id, b=pwd)


if __name__ == '__main__':   #현재모듈 이름이 main이냐? main()함수 호출하는 것과 동일
    app.run()   #flask 서버 실행
