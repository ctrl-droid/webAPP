#board와 관련된 vo, dao, service
import pymysql

class Board:
    def __init__(self, num=None, writer=None, w_date=None, title=None, content=None):
        self.num = num
        self.writer = writer
        self.w_date = w_date
        self.title = title
        self.content = content
'''
글작성 - insert(Board)#작성자, title, content values(sysdate(), now()
글목록  - selectAll()
글번호로검색 - selectByNum(num)
글작성자로 검색 - selectByWriter(writer)
글 title로 검색 - selectByTitle(title)
글수정 - update(Board) : title, content, w_date: num을 같은 행에 대해 수정
글삭제 - delete(num)
'''
class BoardDao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='encore', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self, board):
        self.connect()
        cur = self.conn.cursor()
        sql = 'insert into board(writer, w_date, title, content) values(%s, now(), %s, %s)'
        vals = (board.writer, board.title, board.content)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def selectAll(self):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from board order by num desc'
        cur.execute(sql)
        boards = []
        for row in cur:
            boards.append(Board(row[0], row[1], row[2], row[3], row[4]))
        self.disconnect()
        return boards

    def selectByNum(self, num):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from board where num=%s'
        vals = (num,)
        cur.execute(sql, vals)  # 검색 결과는 실행한 cur객체에 담긴다
        row = cur.fetchone()  # 검색된 결과에서 한줄 팻치. 만약 검색된 결과 없으면 None반환
        self.disconnect()
        if row != None:  # 검색된 결과가 있으면 각 컬럼의 값을 꺼내라
            num = row[0]
            writer = row[1]
            w_date = row[2]
            title = row[3]
            content = row[4]

            b = Board(num, writer, w_date, title, content)
            return b

    def selectByWriter(self, writer):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from board where writer=%s order by num desc'
        vals = (writer, )
        cur.execute(sql, vals)
        boards = []
        for fow in cur:
            boards.append(Board(Board(row[0], row[1], row[2], row[3], row[4])))
        self.disconnect()
        return boards

    def selectByTitle(self, title):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from board where title like=%s order by num desc'
        vals = (title,)
        cur.execute(sql, vals)
        boards = []
        for fow in cur:
            boards.append(Board(Board(row[0], row[1], row[2], row[3], row[4])))
        self.disconnect()
        return boards

    def update(self, board):
        self.connect()
        cur = self.conn.cursor()
        sql = 'update board set title=%s, content=%s where num=%s'
        vals = (board.title, board.content, board.num)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def delete(self, num):
        self.connect()
        cur = self.conn.cursor()
        sql = 'delete from board where num=%s'
        vals = (num,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

class BoardService:
    def __init__(self):
        self.dao = BoardDao()

    def addBoard(self, board):
        self.dao.insert(board)

    def getAll(self):
        return self.dao.selectAll()

    def getNum(self, num):
        return self.dao.selectByNum(num)

    def getWriter(self, writer):
        return self.dao.selectByWriter(writer)

    def getTitle(self, title):
        return self.dao.selectByTitle(title)

    def editBoard(self, board):
        self.dao.update(board)

    def delBoard(self, num):
        self.dao.delete(num)


