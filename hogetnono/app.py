from flask import Flask, request, render_template
import routes.admin_route as ar
import routes.member_route as mr
import routes.board_route as br
import hogetnono.models.aptinfo as ai

app = Flask(__name__)
app.secret_key = 'affdasdf'

#생성한 블루프린트 등록
app.register_blueprint(ar.bp)
app.register_blueprint(mr.bp)
app.register_blueprint(br.bp)

@app.route('/')
def root():
    aptinfos = ai.AptinfoService().getAllAptinfo()
    return render_template('index.html', aptinfos=aptinfos)

if __name__ == '__main__':
    app.run()#flask 서버 실행