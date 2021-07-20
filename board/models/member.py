#member와 관련된 vo, dao, service

import pymysql

class Member:
    def __init__(self, id=None, pwd=None, name=None, email=None):
        self.id = id
        self.pwd = pwd
        self.name = name
        self.email = email

    def __str__(self):
        return self.id+' /' + self.pwd + ' /' + self.name + ' /'+ self.email


class MemDao:
    def __init__(self):
        self.conn = None    #db connection 객체 저장

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='encore', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self, mem):
        self.connect() #db 연결
        cur = self.conn.cursor()  #사용할 커서 객체 생성
        sql = "insert into member(id,pwd,name,email) values(%s, %s, %s, %s)"
        vals = (mem.id, mem.pwd, mem.name, mem.email)
        cur.execute(sql, vals)  #sql 실행
        self.conn.commit()  #insert, update, delete 문장 실행 시 호출
        self.disconnect()

    def select(self, id):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from member where id=%s"   #변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (id,)
        cur.execute(sql, vals)  #sql 실행. 검색한 결과 cur에 담음.
        row = cur.fetchone() #커서에서 검색된 한 줄을 꺼내어 row담음.
        self.disconnect()
        if row!=None:   #검색된 결과가 있으면
            mem = Member(row[0], row[1], row[2], row[3])#num, name, price, amount
            return mem

    def update(self, new_pwd, id):#수정할 제품의 번호와 새 가격과 새 수량
        self.connect()  # db 연결
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = "update member set pwd=%s where id=%s"
        vals = (new_pwd, id)
        cur.execute(sql, vals)  # sql 실행
        self.conn.commit()  # insert, update, delete 문장 실행 시 호출
        self.disconnect()

    def delete(self, id):
        self.connect()  # db 연결
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = "delete from member where id=%s"  # 변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (id,)
        cur.execute(sql, vals)  # sql 실행
        self.conn.commit()
        self.disconnect()


class MemService:
    def __init__(self):
        self.dao = MemDao()

    def addMem(self, mem):
        self.dao.insert(mem)

    def getMem(self, id):
        return self.dao.select(id)

    def editMem(self, new_pwd, id):
        self.dao.update(new_pwd, id)

    def delMem(self, id):
        return self.dao.delete(id)