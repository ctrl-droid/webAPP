# aptinfo와 관련된 vo, dao, service
import pymysql
import requests
from bs4 import BeautifulSoup
import hogetnono.models.aptinfo as ai

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

class TransactionService:
    def __init__(self):
        self.TSdao = TransactionDao()
        self.AIdao = ai.AptinfoDao()
        self.serviceKey = 'qllrU5q/Iy5IEY7QPdyk29YFEKziTWkVrdkGJEGW4bYjZF19Wpbm7P6jel3RuGrAmWWX+HcBVCxYsKFAsxsh2w=='
        self.url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'

    # 공공 API에 입력한 URL, 파라미터, 파라미터 값의 결과를 bs 형태로 반환한다.
    def getRequestsByParam(self, lawd_cd, deal_ymd):
        request_URL = self.url
        request_param = {'serviceKey': self.serviceKey, 'pageNo': '1', 'numOfRows':'700', 'LAWD_CD':lawd_cd, 'DEAL_YMD':deal_ymd}
        html = requests.get(request_URL, params=request_param).text.encode('utf-8')
        content = BeautifulSoup(html, 'lxml-xml')
        return content

    def getTransactionAPI(self, lawd_cd, deal_ymd):
        content = self.getRequestsByParam(lawd_cd, deal_ymd)
        if content.find('resultCode').get_text() == '00':
            itemList = content.find_all('item')
            for item in itemList:
                # API에서 조회 후 데이터 가공

                name = item.find('아파트').get_text()

                add1 = item.find('도로명').get_text()
                add2 = item.find('도로명건물본번호코드').get_text()
                add3 = item.find('도로명건물부번호코드').get_text()
                aptinfo_sn = add1+add2+add3
                add3 = int(add3)
                if add3 == 0:
                    add3 = ''
                else:
                    add3 = '-' + str(add3)
                add = add1+' '+str(int(add2))+add3

                tranSN = item.find('일련번호') # 취소 매물 거를때
                if tranSN == None:
                    break

                amount = item.find('거래금액').get_text()
                amount = int(amount.replace(',',''))

                Y = item.find('년').get_text()
                M = item.find('월').get_text()
                D = item.find('일').get_text()

                if len(M) == 1:
                    M = '0' + M
                if len(D) == 1:
                    D = '0' + D
                date = Y + M + D

                area = item.find('전용면적').get_text()

                floor = item.find('층').get_text()

                # aptinfo 넣는곳
                aptinfo = self.AIdao.selectBySn(aptinfo_sn)
                if aptinfo == None:
                    self.AIdao.insert(ai.Aptinfo(sn=aptinfo_sn, name=name, address=add, location_code=lawd_cd))

                # transaction 넣는곳
                self.TSdao.insert(Transaction(amount=amount, date=date, area=area, floor=floor, aptinfo_sn=aptinfo_sn))

        else:
            print('대상 없음')
            return None

    def getTransactionsBySn(self, sn):
        return self.TSdao.selectBySn(sn)

    def getTransactionsByCode(self, code):
        return self.TSdao.selectByCode(code)

    def getAllApttrans(self):
        return self.TSdao.selectAll()

    def delApttrans(self, code):
        self.TSdao.delete(code)

    def editApttrans(self, arpttrans):
        self.TSdao.edit(arpttrans)

    def delApttrans(self, code):
        self.TSdao.delete(code)