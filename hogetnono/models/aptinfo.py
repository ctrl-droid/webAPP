# aptinfo와 관련된 vo, dao, service
import pymysql

class Aptinfo:
    def __init__(self, sn=None, name=None, address=None, location_code=None):
        self.sn = sn
        self.name = name
        self.address = address
        self.location_code = location_code

    def __str__(self):
        return 'sn:' + self.sn + 'name:' + self.name + 'address:' + self.address + 'location_code:' + self.location_code

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
        sql = 'insert into aptinfo values(%s, %s, %s, %s)'
        vals = (aptinfo.sn, aptinfo.name, aptinfo.address, aptinfo.location_code)
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
            aptinfos.append(Aptinfo(row[0], row[1], row[2], row[3]))
        self.disconnect()
        return aptinfos

    def selectBySn(self, sn):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from aptinfo where sn=%s'
        vals = (sn,)
        cur.execute(sql, vals)
        row = cur.fetchone()
        self.disconnect()
        if row != None:
            a = Aptinfo(row[0], row[1], row[2], row[3])
            return a

    def selectByName(self, name):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from aptinfo where name like %s'
        vals = ('%' + name + '%',)
        cur.execute(sql, vals)
        aptinfos = []
        for row in cur:
            aptinfos.append(Aptinfo(row[0], row[1], row[2], row[3]))
        self.disconnect()
        return aptinfos

    def edit(self, aptinfo):
        self.connect()
        cur = self.conn.cursor()
        sql = 'update aptinfo set name=%s, address=%s, location_code=%s where sn=%s'
        vals = (aptinfo.name, aptinfo.address, aptinfo.location_code, aptinfo.sn)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def delete(self, sn):
        self.connect()
        cur = self.conn.cursor()
        sql = 'delete from aptinfo where sn=%s'
        vals = (sn,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

class AptinfoService:
    def __init__(self):
        self.dao = AptinfoDao()

    def addAptinfo(self, aptinfo):
        self.dao.insert(aptinfo)

    def getAllAptinfo(self):
        return self.dao.selectAll()

    def getAptinfoByName(self, name):
        return self.dao.selectByName(name)

    def getAptinfoBySn(self, sn):
        return self.dao.selectBySn(sn)

    def editAptinfo(self, aptinfo):
        self.dao.edit(aptinfo)

    def delAptinfo(self, sn):
        self.dao.delete(sn)
