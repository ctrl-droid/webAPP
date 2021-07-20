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
        pass

    def selectByWriter(self, writer):
        pass

    def selectByTitle(self, title):
        pass

    def update(self, board):
        pass

    def delete(self, num):
        pass

class BoardService:
    def __init__(self):
        self.dao = BoardDao()

    def addBoard(self, board):
        self.dao.insert(board)

    def getAll(self):
        return self.dao.selectAll()

