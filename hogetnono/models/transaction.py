# aptinfo와 관련된 vo, dao, service
import pymysql

class Transaction:
    def __init__(self, code=None, amount=None, date=None, area=None, floor=None, aptinfo_sn=None):
        self.code = code
        self.amount = amount
        self.date = date
        self.area = area
        self.floor = floor
        self.aptinfo_sn = aptinfo_sn

    def __str__(self):
        return 'code:' + self.code + 'amount:' + self.amount + 'date:' + self.date \
               + 'area:' + self.area + 'floor:' + self.floor + 'aptinfo_sn:' + self.aptinfo_sn

class TransactionDao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='hogetnono', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self, transaction):
        self.connect()
        cur = self.conn.cursor()
        sql = 'insert into transaction(amount, date, area, floor, aptinfo_sn) values(%s, %s, %s, %s, %s)'
        vals = (transaction.amount, transaction.date, transaction.area, transaction.floor, transaction.aptinfo_sn)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def selectBySn(self, sn):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from transaction where aptinfo_sn=%s'
        vals = (sn,)
        cur.execute(sql, vals)
        transactions = []
        for row in cur:
            transactions.append(Transaction(row[0], row[1], row[2], row[3], row[4], row[5]))
        self.disconnect()
        return transactions

    def selectAll(self):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from transaction'
        cur.execute(sql)
        apttans = []
        for row in cur:
            apttans.append(Transaction(row[0], row[1], row[2], row[3], row[4], row[5]))
        self.disconnect()
        return apttans

    def selectByCode(self, code):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from transaction where code=%s'
        vals = (code,)
        cur.execute(sql, vals)
        # transactions = []
        for row in cur:
            vo = Transaction(row[0], row[1], row[2], row[3], row[4], row[5])
        self.disconnect()
        return vo

    def edit(self, apttrans):
        self.connect()
        cur = self.conn.cursor()
        sql = 'update transaction set amount=%s, date=%s, area=%s, floor=%s, APTinfo_SN=%s  where code=%s'
        vals = (apttrans.amount, apttrans.date, apttrans.area,apttrans.floor, apttrans.aptinfo_sn, apttrans.code)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def delete(self, code):
        self.connect()
        cur = self.conn.cursor()
        sql = 'delete from transaction where code=%s'
        vals = (code,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def selectUniqArea(self, sn):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select area from transaction where APTinfo_SN=%s group by area order by area'
        vals = (sn,)
        cur.execute(sql, vals)
        pre_area = []
        for row in cur:
            pre_area.append(row[0])
        self.disconnect()
        return pre_area

    def selectBySnAndArea(self, sn, area):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from transaction where aptinfo_sn=%s and area=%s order by date desc'
        vals = (sn, area)
        cur.execute(sql, vals)
        transactions = []
        for row in cur:
            transactions.append(Transaction(row[0], row[1], row[2], row[3], row[4], row[5]))
        self.disconnect()
        return transactions


class TransactionService:
    def __init__(self):
        self.dao = TransactionDao()

    def getTransactionsBySn(self, sn):
        return self.dao.selectBySn(sn)

    def getTransactionsByCode(self, code):
        return self.dao.selectByCode(code)

    def getAllApttrans(self):
        return self.dao.selectAll()

    def delApttrans(self, code):
        self.dao.delete(code)

    def editApttrans(self, arpttrans):
        self.dao.edit(arpttrans)

    def delApttrans(self, code):
        self.dao.delete(code)

    def getUniqArea(self, sn):
        return self.dao.selectUniqArea(sn)

    def getTransactionsArea(self, sn, area):
        return self.dao.selectBySnAndArea(sn, area)


