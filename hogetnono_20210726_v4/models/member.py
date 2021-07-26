import pymysql
import requests

class Member:
    def __init__(self, id=None, pwd=None, name=None, tel=None):
        self.id = id
        self.pwd = pwd
        self.name = name
        self.tel = tel

    def __str__(self):
        return self.id+' / '+self.pwd+' / '+self.name+' / '+self.tel


class MemberDao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='hogetnono', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self, mem):
        self.connect()
        cur = self.conn.cursor()
        sql = "insert into member value(%s,%s,%s,%s)"
        vals = (mem.id, mem.pwd, mem.name, mem.tel)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def select(self, id):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from member where id=%s"
        vals = (id,)
        cur.execute(sql, vals)
        row = cur.fetchone()
        self.disconnect()
        if row != None:
            mem = Member(row[0],row[1],row[2],row[3])
            return mem

    def edit(self, mem):
        self.connect()
        cur = self.conn.cursor()
        sql = 'update member set pwd=%s, tel=%s where id=%s'
        vals = (mem.pwd, mem.tel, mem.id)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()


    def delete(self, id):
        self.connect()
        cur = self.conn.cursor()
        sql = 'delete from member where id=%s'
        vals = (id,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

class MemberService:
    def __init__(self):
        self.dao = MemberDao()

    def addMember(self,mem):
        self.dao.insert(mem)

    def getMember(self, id):
        return self.dao.select(id)

    def editMember(self, mem):
        self.dao.edit(mem)

    def deleteMember(self, id):
        self.dao.delete(id)
