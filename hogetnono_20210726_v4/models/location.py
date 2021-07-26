# aptinfo와 관련된 vo, dao, service
import pymysql

class Location:
    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name

    def __str__(self):
        return 'code:' + self.code + 'name:' + self.name

class LocationDao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='hogetnono', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self, location):
        self.connect()
        cur = self.conn.cursor()
        sql = 'insert into location values(%s, %s)'
        vals = (location.code, location.name)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def selectAll(self):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from location'
        cur.execute(sql)
        aptinfos = []
        for row in cur:
            aptinfos.append(Location(row[0], row[1]))
        self.disconnect()
        return aptinfos

    def selectBycode(self, code):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from location where code=%s'
        vals = (code,)
        cur.execute(sql, vals)
        row = cur.fetchone()
        self.disconnect()
        if row != None:
            vo = Location(row[0], row[1])
            return vo

class LocationService:
    def __init__(self):
        self.dao = LocationDao()

    def addLocation(self, location):
        self.dao.insert(location)

    def getAllLocation(self):
        return self.dao.selectAll()

    def getLocationByCode(self, code):
        return self.dao.selectBycode(code)