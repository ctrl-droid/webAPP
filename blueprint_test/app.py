from flask import Flask, request, render_template
import routes.member as rm
import routes.board as rb

app = Flask(__name__)

#생성한 블루프린트 등록
app.register_blueprint(rm.bp)
app.register_blueprint(rb.bp)

if __name__ == '__main__':
    app.run()#flask 서버 실행