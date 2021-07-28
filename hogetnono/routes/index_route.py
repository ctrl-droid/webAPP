from flask import Blueprint, render_template, request, redirect, session, jsonify
import hogetnono.models.aptinfo as ai
import hogetnono.models.transaction as tr
import hogetnono.models.board as board

bp = Blueprint('', __name__, url_prefix='/index')  #url 생성기
aptinfo_service = ai.AptinfoService()
transaction_service = tr.TransactionService()
board_service = board.BoardService()

@bp.route('/aptsearch', methods=['POST'])
def aptsearch():
    data = request.get_json()
    apt_search = data['apt_search']
    aptvos = aptinfo_service.getAptinfoByName(apt_search)
    aptinfos = []   # json 타입으로 변환해서 전송
    for i in aptvos:
        aptinfos.append({'sn':i.sn, 'name':i.name,'address':i.address})
    return jsonify(result="success", aptinfos=aptinfos)

def transactionToJson(transactionvos):
    ts = []
    totamount = 0 # 가격 합계
    count = 0
    lastdate = str(transactionvos[0].date)[0:7]
    for t in transactionvos:
        if lastdate == str(t.date)[0:7]:
            totamount += t.amount
            count += 1

        amount_str = amountToStr(t.amount)
        ts.append({'code': t.code, 'amount': t.amount, 'amount_str': amount_str, 'date': t.date, 'area': t.area,
                   'floor': t.floor, 'aptinfo_sn': t.aptinfo_sn})
    avgAmount = amountToStr(int(totamount/count))
    return ts, avgAmount

def amountToStr(amount):
    amount_str = str(amount)
    if len(amount_str) > 4:
        if amount_str[-5:-1] == '0000':
            amount_str = amount_str[:-4] + '억 '
        else:
            amount_str = amount_str[:-4] + '억 ' + str(int(amount_str[-5:-1]))
    return amount_str

@bp.route('/showAptInfo', methods=['POST'])
def showAptInfo():
    data = request.get_json()
    sn = data['sn']

    # 아파트 정보 전달
    aptvo = aptinfo_service.getAptinfoBySn(sn)
    aptinfo = {'sn':aptvo.sn, 'name':aptvo.name,'address':aptvo.address}

    uniqArea = transaction_service.getUniqArea(sn)
    transactionvos = transaction_service.getTransactionsArea(sn, uniqArea[0])
    ts, avgAmount = transactionToJson(transactionvos)

    bs = board_service.board_select_sn(sn)
    boards = []
    for b in bs:
        boards.append({'code':b.code, 'date':b.date,'content':b.content,'member_id':b.member_id,'aptinfo_sn':b.aptinfo_sn})
    return jsonify(result="success", aptinfo=aptinfo, ts=ts, uniqArea=uniqArea, avgAmount=avgAmount, boards=boards)

@bp.route('/showSelect', methods=['POST'])
def showSelect():
    data = request.get_json()
    sn = data['sn']
    area = data['area']

    # 아파트 정보 전달
    aptvo = aptinfo_service.getAptinfoBySn(sn)
    aptinfo = {'sn': aptvo.sn, 'name': aptvo.name, 'address': aptvo.address}

    transactionvos = transaction_service.getTransactionsArea(sn, area)
    ts, avgAmount = transactionToJson(transactionvos)

    return jsonify(result="success", aptinfo=aptinfo, ts=ts, avgAmount=avgAmount)

@bp.route('/boardAdd', methods=['POST'])
def boardAdd():
    data = request.get_json()
    sn = data['sn']
    content = data['content']
    member_id = session['id']

    board_service.board_insert(board.Board(content=content , member_id=member_id, aptinfo_sn=sn))
    bs = board_service.board_select_sn(sn)
    boards = []
    for b in bs:
        boards.append({'code': b.code, 'date': b.date, 'content': b.content, 'member_id': b.member_id,
                       'aptinfo_sn': b.aptinfo_sn})
    return jsonify(result="success", boards=boards)

@bp.route('/boardDel', methods=['POST'])
def boardDel():
    data = request.get_json()
    sn = data['sn']
    code = data['code']
    board_service.board_delete(code)
    bs = board_service.board_select_sn(sn)
    boards = []
    for b in bs:
        boards.append({'code': b.code, 'date': b.date, 'content': b.content, 'member_id': b.member_id,
                       'aptinfo_sn': b.aptinfo_sn})
    return jsonify(result="success", boards=boards)