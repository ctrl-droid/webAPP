from flask import Blueprint, render_template, request, redirect, session
import board.models.product as prod

bp = Blueprint('prod', __name__, url_prefix='/product')
prodService = prod.ProductService()

@bp.route('/')
def list():
    prods = prodService.getAll()
    return render_template('product/list.html', prods=prods)

@bp.route('/add')
def add_form():
    return render_template('product/form.html')

@bp.route('/add', methods=['POST'])
def add():
    upload_path = 'static/img/'   #파일 복사할 경로
    f = request.files['img_path']   #파일업로드 폼에서 동일한 이름의 파일 받아옴
    fname = upload_path + f.filename
    f.save(fname)   #클라이언트가 보낸 파일을 서버에 복사
    name = request.form['name']
    price = request.form.get('price', 0, int)
    amount = request.form.get('amount', 0, int)
    img_path = '/' + fname
    p = prod.Product(name=name, price=price, amount=amount, img_path=img_path)
    prodService.addProduct(p)
    return redirect('/product/')

@bp.route('/get')
def get():
    num = request.args.get('num', 0, int)
    p = prodService.getProduct(num)
    return render_template('product/detail.html', p=p)