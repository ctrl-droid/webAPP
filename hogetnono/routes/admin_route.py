#/admin/ 관련된 url 등록

from flask import Blueprint, render_template, request, redirect, session
import hogetnono.models.aptinfo as ai
import hogetnono.models.transaction as ts

bp = Blueprint('admin', __name__, url_prefix='/admin')  #url 생성기
aptinfoService = ai.AptinfoService()
transactionService = ts.TransactionService()

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/add')
def add_form():
    transactionService.getTransactionAPI('202001')
    transactionService.getTransactionAPI('202002')
    transactionService.getTransactionAPI('202003')
    transactionService.getTransactionAPI('202004')
    return render_template('admin/add_form.html')
