#/admin/ 관련된 url 등록

from flask import Blueprint, render_template, request, redirect, session
import hogetnono.models.location as local
import hogetnono.models.aptinfo as ai
import hogetnono.models.transaction as ts
import hogetnono.models.member as mem
import hogetnono.models.board as b
import hogetnono.models.apirequest as api

bp = Blueprint('admin', __name__, url_prefix='/admin')  #url 생성기
locationService = local.LocationService()
aptinfoService = ai.AptinfoService()
transactionService = ts.TransactionService()
memService = mem.MemberService()
boardService = b.BoardService()
openApiService = api.OpenApiService()

@bp.route('/')
def admin():
    if 'admin' == session['id']:  # 파라미터 변조에 의한 수정 방지(파라미터에서 받는 정보로 비교X)
        lols = locationService.getAllLocation()
        if len(lols) == 0:
            lols = None
        return render_template('admin/admin_location.html', lols=lols)
    else:
        return '관리자만 접근 가능합니다.'

@bp.route('locationadd', methods = ['POST'])
def add_location():
    code = request.form['code']
    name = request.form['name']
    locationService.addLocation(local.Location(code=code, name=name))
    # 강남구 CODE = '11680'
    for i in range(7, 13):
        date = '2020' + format(i, '02')
        openApiService.getTransactionAPI(code, date)
    for i in range(1, 8):
        date = '2021' + format(i, '02')
        openApiService.getTransactionAPI(code, date)

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

@bp.route('/member')
def member():
    mems = memService.getAllMember()
    if len(mems) == 0:
        mems = None
    return render_template('admin/admin_member.html', mems=mems)

@bp.route('/member/edit')
def member_editform():
    id = request.args.get('id', '', str)
    mem = memService.getMember(id)
    return render_template('admin/admin_member_edit.html', mem=mem)

@bp.route('/member/edit', methods = ['POST'])
def member_edit():
    id = request.form['id']
    pwd = request.form['pwd']
    name = request.form['name']
    tel = request.form['tel']

    memService.editMember(mem.Member(id=id, pwd=pwd, name=name, tel=tel))
    return redirect('/admin/member')

@bp.route('/member/del')
def member_del():
    id = request.args.get('id', '', str)
    memService.deleteMember(id)
    return redirect('/admin/member')

@bp.route('/board')
def board():
    aptinfo_sn = request.args.get('sn', '', str)
    boards = boardService.board_selectAll()
    return render_template('admin/admin_board.html', boards=boards, sn=aptinfo_sn)

@bp.route('/board/edit')
def board_editform():
    code = request.args.get('code', 0, int)
    boards = boardService.board_select_code(code)
    return render_template('admin/admin_board_edit.html', boards=boards)

@bp.route('/board/edit', methods = ['POST'])
def board_edit():
    content = request.form['content']
    code = request.form['code']
    boards = b.Board(content=content, code=code)
    boardService.board_edit(boards)
    return redirect('/admin/board')

@bp.route('/board/del')
def board_delete():
    code = request.args.get('code', '', str)
    boardService.board_delete(code)
    return redirect('/admin/board')

@bp.route('/transaction')
def transaction():
    apttrans = transactionService.getAllApttrans()
    if len(apttrans) == 0:
        apttrans = None

    return render_template('admin/admin_transaction.html', apttrans=apttrans)

@bp.route('/transaction/edit')
def apttrans_editform():
    code = request.args.get('code', '', str)
    apttrans = transactionService.getTransactionsByCode(code)
    return render_template('admin/admin_transaction_edit.html', apttrans=apttrans)

@bp.route('/transaction/edit', methods = ['POST'])
def apttrans_edit():
    code = request.form['code']
    amount = request.form['amount']
    date = request.form['date']
    area = request.form['area']
    floor = request.form['floor']
    aptinfo_sn = request.form['aptinfo_sn']
    transactionService.editApttrans(ts.Transaction(code=code, amount=amount, date=date, area=area, floor=floor, aptinfo_sn=aptinfo_sn))
    return redirect('/admin/transaction')

@bp.route('/transaction/del')
def apttrans_del():
    code = request.args.get('code', '', str)
    transactionService.delApttrans(code)
    return redirect('/admin/transaction')