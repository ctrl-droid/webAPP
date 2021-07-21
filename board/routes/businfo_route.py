from flask import Blueprint, render_template, request, redirect, session
import board.models.businfo as bus

bp = Blueprint('businfo', __name__, url_prefix='/businfo')  #url 생성기
busService = bus.BusService()

@bp.route('/')
def root():
    return render_template('businfo/loc.html')

@bp.route('/getroute-list', methods=['POST'])
def route_list():
    loc = request.form['loc']
    print(loc)
    lst = busService.getBusRouteList(loc)
    return render_template('businfo/routeList.html', lst=lst)

@bp.route('/getroute-info')
def getfoute_info():
    routeid = request.args.get('routeid','',str)
    b = busService.getRouteInfoItem(routeid)
    stations = busService.getStaionsByRouteList(routeid)
    return render_template('businfo/detail.html', b=b, stations=stations)

