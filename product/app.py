from flask import Flask, render_template, request
import vo

app = Flask(__name__)

@app.route('/add')
def add_form():
    return render_template('add.html')

@app.route('/add', methods=['POST'])
def add():
    num = request.form["num"]
    name = request.form["name"]
    price = request.form["price"]
    amount = request.form["amount"]

    pd = vo.Product(num, name, price, amount)
    return render_template('add_result.html', pd=pd)


if __name__ == '__main__':
    app.run()