from flask import Flask, request, render_template
import routes.admin_route as ar

app = Flask(__name__)
app.secret_key = 'affdasdf'

#생성한 블루프린트 등록
app.register_blueprint(ar.bp)

@app.route('/')
def root():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()#flask 서버 실행