#/admin/ 관련된 url 등록

from flask import Blueprint, render_template, request, redirect, session
import hogetnono.models.location as local
import hogetnono.models.aptinfo as ai
import hogetnono.models.transaction as ts

bp = Blueprint('admin', __name__, url_prefix='/admin')  #url 생성기
locationService = local.LocationService()
aptinfoService = ai.AptinfoService()
transactionService = ts.TransactionService()

@bp.route('/')
def admin():
    lols = locationService.getAllLocation()
    if len(lols) == 0:
        lols = None
    return render_template('admin/admin_location.html', lols=lols)

@bp.route('locationadd', methods = ['POST'])
def add_location():
    code = request.form['code']
    name = request.form['name']
    locationService.addLocation(local.Location(code=code, name=name))
    # 강남구 CODE = '11680'
    for i in range(1, 7):
        date = '20210' + str(i)
        transactionService.getTransactionAPI(code, date)
    return redirect('/admin')

@bp.route('/aptinfo')
def aptinfo():
    aptins = aptinfoService.getAllAptinfo()
    if len(aptins) == 0:
        trans = None
    return render_template('admin/admin_aptinfo.html', aptins=aptins)

@bp.route('/aptinfo/edit')
def aptinfo_editform():
    sn = request.args.get('sn', '', str)
    aptinfo = aptinfoService.getAptinfoBySn(sn)
    return render_template('admin/admin_aptinfo_edit.html', aptinfo=aptinfo)

@bp.route('/aptinfo/edit', methods = ['POST'])
def aptinfo_edit():
    sn = request.form['sn']
    name = request.form['name']
    address = request.form['address']
    location_code = request.form['location_code']
    aptinfoService.editAptinfo(ai.Aptinfo(sn=sn, name=name, address=address, location_code=location_code))
    return redirect('/admin/aptinfo')

@bp.route('/aptinfo/del')
def aptinfo_del():
    sn = request.args.get('sn', '', str)
    aptinfoService.delAptinfo(sn)
    return redirect('/admin/aptinfo')

@bp.route('/board')
def board():
    return render_template('admin/admin_board.html')

@bp.route('/member')
def member():
    return render_template('admin/admin_member.html')

@bp.route('/transaction')
def transaction():
    return render_template('admin/admin_transaction.html')