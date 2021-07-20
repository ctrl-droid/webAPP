#member와 관련된 vo, dao, service
import pymysql

class Member:

    def __init__(self, id=None, pwd=None, name=None, email=None):
        #파라메터 id=None : 생략가능.
        self.id = id
        self.pwd = pwd
        self.name = name
        self.email = email

    def __str__(self):
        return self.id+' / '+self.pwd+' / '+self.name+' / '+self.email

class MemDao:
    def __init__(self):
        self.conn = None    #db connection 객체 저장. 클래스 내에서 전역변수.

    def connect(self):#self는 현재 객체의 참조값
        #db에 로그인하는 함수
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='encore', charset='utf8')

    def disconnect(self):#db와 연결을 끊음
        self.conn.close()

    def insert(self, m):#m: vo객체로 회원가입시 입력한 id, pwd, name, email 받아옴
        self.connect()#db 연결
        cur = self.conn.cursor()#db 작업 하려면 cursor 객체가 필요
        sql = 'insert into member values(%s, %s, %s, %s)'  #sql문 작성
        vals = (m.id, m.pwd, m.name, m.email)               #sql의 %s 매칭에 사용할 튜플 생성
        cur.execute(sql, vals) #sql문 실행
        self.conn.commit()  #쓰기 완료
        self.disconnect()#db 연결 끊음

    def select(self, id):#id로 검색
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from member where id=%s'
        vals = (id, )
        cur.execute(sql, vals)  #검색 결과는 실행한 cur객체에 담긴다
        row = cur.fetchone()    #검색된 결과에서 한줄 팻치. 만약 검색된 결과 없으면 None반환
        self.disconnect()
        if row!=None:#검색된 결과가 있으면 각 컬럼의 값을 꺼내라
            id = row[0]     #row에서 0번 컬럼 즉 id 컬럼 값 꺼내서 변수 id에 저장
            pwd = row[1]    #row에서 1번 컬럼 즉 pwd 컬럼 값 꺼내서 변수 pwd에 저장
            name = row[2]   #row에서 2번 컬럼 즉 name 컬럼 값 꺼내서 변수 name에 저장
            email = row[3]  #row에서 3번 컬럼 즉 email 컬럼 값 꺼내서 변수 email에 저장
            m = Member(id, pwd, name, email) #id, pwd, name, email 변수의 값으로 Member 객체 생성
            return m    #생성한 객체 반환

    def update(self, m):#수정할 사람의 id, 수정할 새pwd
        self.connect()
        cur = self.conn.cursor()
        sql = 'update member set pwd=%s where id=%s'
        vals = (m.pwd, m.id)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def delete(self, id):#id로 찾아서 삭제
        self.connect()
        cur = self.conn.cursor()
        sql = 'delete from member where id=%s'
        vals = (id,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

class MemService: #app.py에서 사용할 기능 정의. 기능에서 db작업이 필요하다면 dao 객체가 필요.
    def __init__(self):
        self.dao = MemDao()

    def addMember(self, m): #회원 등록, member객체 파라메터로 받아서 db에 insert
        self.dao.insert(m)

    def getMember(self, id): #검색할 id를 받아서 db에서 select
        m = self.dao.select(id)
        return m

    def editMember(self, m):#수정할 id와 새 pwd 받아서 db에서 update
        self.dao.update(m)

    def delMember(self, id):#삭제할 id받아서 db에서 delete
        self.dao.delete(id)