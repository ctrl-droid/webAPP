from flask import Flask, render_template, request
import vo, model

app = Flask(__name__)
prod_service = model.ProductService() #서비스 객체 생성

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/product/add')
def add_form():
    return render_template('product/form.html')

@app.route('/product/add', methods=['POST'])
def add():
    name = request.form.get('name', '', str)
    price = request.form.get('price', 0, int)
    amount = request.form.get('amount', 0, int)
    prod = vo.Product(name=name, price=price, amount=amount)
    prod_service.addProduct(prod) #서비스의 등록 함수 호출
    return render_template('index.html')

@app.route('/product/get', methods=['POST'])
def get():
    num = request.form.get('num', 0, int)
    prod = prod_service.getProduct(num)
    if prod==None:
        return '없는 제품 번호'
    else:
        return render_template('product/detail.html', prod=prod)

@app.route('/product/list')
def list():
    prods = prod_service.getAll()
    return render_template('product/list.html', prods=prods)

@app.route('/product/edit')  #수정폼: /product/edit?num=3
def edit_form():
    num = request.args.get('num', 0, int)
    prod = prod_service.getProduct(num)
    if prod == None:
        return '없는 제품 번호'
    else:
        return render_template('product/edit_form.html', prod=prod)

@app.route('/product/edit', methods=['POST']) #수정완료
def edit():
    return '준비중'





if __name__ == '__main__':
    app.run()