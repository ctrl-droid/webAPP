import pymysql

class Product:
    def __init__(self, num=None, name=None, price=None, amount=None, img_path=None):
        self.num = num          #제품번호
        self.name = name        #제품명
        self.price = price      #제품가격
        self.amount = amount    #수량
        self.img_path = img_path

class ProductDao:
    def __init__(self):
        self.conn = None    #db connection 객체 저장

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='encore', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self, prod):
        self.connect() #db 연결
        cur = self.conn.cursor()  #사용할 커서 객체 생성
        #insert into member values(vo.id, vo.pwd, vo.name, vo.email)
        sql = "insert into product(name,price,amount,img_path) values(%s, %s, %s, %s)"   #변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (prod.name, prod.price, prod.amount, prod.img_path)
        cur.execute(sql, vals)  #sql 실행
        self.conn.commit()  #insert, update, delete 문장 실행 시 호출
        self.disconnect()

    def select(self, num):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from product where num=%s"   #변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (num,)
        cur.execute(sql, vals)  #sql 실행. 검색한 결과 cur에 담음.
        row = cur.fetchone() #커서에서 검색된 한 줄을 꺼내어 row담음.
        self.disconnect()
        if row!=None:   #검색된 결과가 있으면
            prod = Product(row[0], row[1], row[2], row[3], row[4])#num, name, price, amount
            return prod

    def selectAll(self):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from product"
        cur.execute(sql)  # sql 실행.
        prods = [] #검색된 모든 값 저장.
        for row in cur:
            prods.append(Product(row[0], row[1], row[2], row[3], row[4]))
        self.disconnect()
        return prods

    def update(self, prod):#수정할 제품의 번호와 새 가격과 새 수량
        self.connect()  # db 연결
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = "update product set price=%s, amount=%s where num=%s"  # 변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (prod.price, prod.amount, prod.num)
        cur.execute(sql, vals)  # sql 실행
        self.conn.commit()  # insert, update, delete 문장 실행 시 호출
        self.disconnect()

    def delete(self, num):
        self.connect()  # db 연결
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = "delete from product where num=%s"  # 변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (num,)
        cur.execute(sql, vals)  # sql 실행
        self.conn.commit()  # insert, update, delete 문장 실행 시 호출
        self.disconnect()



class ProductService:  #기능 정의
    def __init__(self):
        self.dao = ProductDao()

    def addProduct(self, prod):#제품추가. 제품 이름,가격,수량을 db에 저장
        self.dao.insert(prod)

    def getProduct(self, num): #제품 번호로 검색 기능
        return self.dao.select(num)

    def getAll(self):
        return self.dao.selectAll()

    def editProduct(self, prod):
        self.dao.update(prod)

    def delProduct(self, num):
        return self.dao.delete(num)
