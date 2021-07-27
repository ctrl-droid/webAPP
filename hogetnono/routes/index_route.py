from flask import Blueprint, render_template, request, redirect, session, jsonify
import hogetnono.models.aptinfo as ai
import hogetnono.models.transaction as tr

bp = Blueprint('', __name__, url_prefix='/index')  #url 생성기
aptinfo_service = ai.AptinfoService()
transaction_service = tr.TransactionService()
#board_service = board.BoardService()


@bp.route('/test')
def test():
    return render_template('test.html')

@bp.route('/aptsearch', methods=['POST'])
def aptsearch():
    data = request.get_json()
    apt_search = data['apt_search']
    aptvos = aptinfo_service.getAptinfoByName(apt_search)
    aptinfos = []   # json 타입으로 변환해서 전송
    for i in aptvos:
        aptinfos.append({'sn':i.sn, 'name':i.name,'address':i.address})
    return jsonify(result="success", aptinfos=aptinfos)

@bp.route('/showAptInfo', methods=['POST'])
def showAptInfo():
    data = request.get_json()
    sn = data['sn']

    # 아파트 정보 전달
    aptvo = aptinfo_service.getAptinfoBySn(sn)
    aptinfo = {'sn':aptvo.sn, 'name':aptvo.name,'address':aptvo.address}

    transactionvos = transaction_service.getTransactionsBySn(sn)
    ts = []
    for t in transactionvos:
        #
        amount_str = str(t.amount)
        if len(amount_str) > 4:
            if amount_str[-5:-1] == '0000':
                amount_str = amount_str[:-4] + '억 '
            else:
                amount_str = amount_str[:-4] + '억 ' + amount_str[-5:-1]

        ts.append({'code':t.code, 'amount':amount_str,'date':t.date, 'area':t.area, 'floor':t.floor, 'aptinfo_sn':t.aptinfo_sn})

    return jsonify(result="success", aptinfo=aptinfo, ts=ts)