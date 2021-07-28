from flask import Flask, request, render_template, jsonify
import routes.admin_route as ar
import routes.member_route as mr
import routes.board_route as br
import routes.index_route as ir
import hogetnono.models.aptinfo as ai
import hogetnono.models.location as local
import hogetnono.models.news as news
import hogetnono.models.apirequest as api

app = Flask(__name__)
app.secret_key = 'affdasdf'

#생성한 블루프린트 등록
app.register_blueprint(ar.bp)
app.register_blueprint(mr.bp)
app.register_blueprint(br.bp)
app.register_blueprint(ir.bp)

locationService = local.LocationService()
aptinfoService = ai.AptinfoService()
newsService = news.NewsService()
mapApiService = api.MapApiService()

@app.route('/')
def root():
    aptinfos = mapApiService.getAptinfo_addGPS()
    news = newsService.NewsCrawler()
    lols = locationService.getAllLocation()
    if len(lols) == 0:
        lols = None
    return render_template('index.html', aptinfos=aptinfos, lols=lols, news=news)

if __name__ == '__main__':
    app.run()#flask 서버 실행