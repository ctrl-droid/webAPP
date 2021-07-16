import pymysql, vo

class ProductDao:
    def __init__(self):
        self.comm = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='encore', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self, prod):
        self.connect()
        cur = self.conn.cursor()
        sql = 'insert into product(name,price,amount) values(%s, %s, %s)'
        vals = (prod.name, prod.price, prod.amount)
        cur.execute(sql, vals)
        self.conn.commit()   #insert, update, delete는 커밋해야함함
        self.disconnect()

    def select(self, num):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from product where num=%s'
        vals = (num,)
        cur.execute(sql, vals)
        row = cur.fetchone()
        self.disconnect()
        if row!=None:
            prod = vo.Product(row[0],row[1],row[2],row[3])
            return prod

    def update(self, prod):
        self.connect()
        cur = self.conn.cursor()
        sql = 'update product set price=%s, amount=%s where num=%s'
        vals = (prod.price, prod.amount, prod.num,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def selectAll(self):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from product'
        cur.execute(sql)
        prods = []
        for row in cur:
            prods.append(vo.Product(row[0], row[1], row[2], row[3]))
        self.disconnect()
        return prods


class ProductService:
    def __init__(self):
        self.dao = ProductDao()

    def addProduct(self, prod):
        self.dao.insert(prod)

    def getProduct(self, num):
        return self.dao.select(num)

    def getAll(self):
        return self.dao.selectAll()

    def editProduct(self, prod):
        return self.dao.update(prod)