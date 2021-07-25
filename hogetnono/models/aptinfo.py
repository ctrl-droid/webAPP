# aptinfo와 관련된 vo, dao, service
import pymysql

class Aptinfo:
    def __init__(self, sn=None, name=None, address=None):
        self.sn = sn
        self.name = name
        self.address = address

    def __str__(self):
        return 'sn:' + self.sn + 'name:' + self.name + 'address:' + self.address

class AptinfoDao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='hogetnono', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self, aptinfo):
        self.connect()
        cur = self.conn.cursor()
        sql = 'insert into aptinfo values(%s, %s, %s)'
        vals = (aptinfo.sn, aptinfo.name, aptinfo.address)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def selectAll(self):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from aptinfo'
        cur.execute(sql)
        aptinfos = []
        for row in cur:
            aptinfos.append(Aptinfo(row[0], row[1], row[2]))
        self.disconnect()
        return aptinfos

    def selectBysn(self, sn):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from aptinfo where sn=%s'
        vals = (sn,)
        cur.execute(sql, vals)
        row = cur.fetchone()
        self.disconnect()
        if row != None:
            a = Aptinfo(row[0], row[1], row[2])
            return a

    def selectByName(self, name):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from aptinfo where name like %s'
        vals = ('%' + name + '%',)
        cur.execute(sql, vals)
        aptinfos = []
        for row in cur:
            aptinfos.append(Aptinfo(row[0], row[1], row[2]))
        self.disconnect()
        return aptinfos

class AptinfoService:
    def __init__(self):
        self.dao = AptinfoDao()

    def addAptinfo(self, aptinfo):
        self.dao.insert(aptinfo)

    def getAllAptinfo(self):
        return self.dao.selectAll()