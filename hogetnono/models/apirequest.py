import requests
import json
from bs4 import BeautifulSoup
import hogetnono.models.aptinfo as ai
import hogetnono.models.transaction as ts

class OpenApiService:
    def __init__(self):
        self.TSdao = ts.TransactionDao()
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
                self.TSdao.insert(ts.Transaction(amount=amount, date=date, area=area, floor=floor, aptinfo_sn=aptinfo_sn))

        else:
            print('대상 없음')
            return None

class MapApiService:
    def __init__(self):
        self.AIdao = ai.AptinfoDao()
        self.serviceKey = 'KakaoAK e3afa4092b9f256f3ca7cd4ac9422611'
        self.url = 'https://dapi.kakao.com/v2/local/search/address.json'

    # 카카오 API에 입력한 URL, 파라미터, 파라미터 값의 결과를 bs 형태로 반환한다.
    def getRequestsByParam(self, param):
        request_URL = self.url
        request_param = {'query': param}
        request_headers = {'Authorization': self.serviceKey}
        html = requests.get(request_URL, headers = request_headers, params=request_param).text.encode('utf-8')
        content = json.loads(html)
        return content

    # 카카오 API를 통해 주소에 대한 GPS를 더하여 aptinfos를 Json형태로 반환
    def getAptinfo_addGPS(self):
        aptinfos = self.AIdao.selectAll()
        agl = []
        for a in aptinfos:
            content = self.getRequestsByParam(a.address)
            x = content['documents'][0]['address']['x']
            y = content['documents'][0]['address']['y']
            agl.append({'sn':a.sn, 'name':a.name, 'address':a.address, 'location_code':a.location_code, 'gps':{'x':x, 'y':y}})
        return agl




