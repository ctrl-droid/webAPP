#board와 관련된 vo, dao, service
import pymysql

class Board:
    def __init__(self, num=None, writer=None, w_date=None, title=None, content=None):
        self.num = num
        self.writer = writer
        self.w_date = w_date
        self.title = title
        self.content = content


class BoardDao:
    def __init__(self):
        self.conn = None  # db connection 객체 저장

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='encore', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self, board):
        self.connect()  # db 연결
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = "insert into board(writer,w_date,title,content) values(%s, now(), %s, %s)"
        vals = (board.writer, board.title, board.content)
        cur.execute(sql, vals)  # sql 실행
        self.conn.commit()  # insert, update, delete 문장 실행 시 호출
        self.disconnect()

    def selectAll(self):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from board order by num desc"
        cur.execute(sql)  # sql 실행.
        boards = [] #검색된 모든 값 저장.
        for row in cur:
            boards.append(Board(row[0], row[1], row[2], row[3],row[4]))   #Board Vo에다가!!
        self.disconnect()
        return boards

    def selectByNum(self, num):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from board where num=%s"  # 변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (num,)
        cur.execute(sql, vals)  # sql 실행. 검색한 결과 cur에 담음.
        row = cur.fetchone()  # 커서에서 검색된 한 줄을 꺼내어 row담음.
        self.disconnect()
        if row != None:  # 검색된 결과가 있으면
            bd = Board(row[0], row[1], row[2], row[3],row[4])  # num, name, price, amount
            return bd

    def selectBywriter(self, writer):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from board where writer=%s"  # 변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (writer,)
        cur.execute(sql, vals)  # sql 실행. 검색한 결과 cur에 담음.
        row = cur.fetchone()  # 커서에서 검색된 한 줄을 꺼내어 row담음.
        self.disconnect()
        if row != None:  # 검색된 결과가 있으면
            bd = Board(row[0], row[1], row[2], row[3], row[4])  # num, name, price, amount
            return bd

    def selectByTitle(self, title):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from board where title=%s"  # 변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (title,)
        cur.execute(sql, vals)  # sql 실행. 검색한 결과 cur에 담음.
        row = cur.fetchone()  # 커서에서 검색된 한 줄을 꺼내어 row담음.
        self.disconnect()
        if row != None:  # 검색된 결과가 있으면
            bd = Board(row[0], row[1], row[2], row[3], row[4])  # num, name, price, amount
            return bd

    def update(self, board):  # 수정할 제품의 번호와 새 가격과 새 수량
        self.connect()  # db 연결
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = "update board set  w_date=%s, title=%s, content=%s where num=%s"
        vals = (board.w_date, board.title, board.content, board.num)
        cur.execute(sql, vals)  # sql 실행
        self.conn.commit()  # insert, update, delete 문장 실행 시 호출
        self.disconnect()

    def delete(self, num):
        self.connect()  # db 연결
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = "delete from board where num=%s"  # 변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (num,)
        cur.execute(sql, vals)  # sql 실행
        self.conn.commit()
        self.disconnect()

class BoardService:
    def __init__(self):
        self.dao = BoardDao()

    def addBoard(self, board):
        self.dao.insert(board)

    def getAll(self):
        return self.dao.selectAll()

    def getWriter(self,writer):
        pass