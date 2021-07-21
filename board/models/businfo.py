import requests
from bs4 import BeautifulSoup

class BusVo:#버스 노선 정보 담을 클래스
    def __init__(self, busId=None,busNm=None,stStat=None,edStat=None,term=None,firstTm=None,lastTm=None,corpNm=None):
        self.busRouteId=busId
        self.busRouteNm=busNm
        self.stStationNm=stStat
        self.edStationNm=edStat
        self.term=term
        self.firstBusTm=firstTm
        self.lastBusTm=lastTm
        self.corpNm=corpNm

    #오버라이딩: 메서드 재정의. 부모로부터 물려받은거 고쳐서 사용하는 것. __str__():'클래스이름. 참조값'
    def __str__(self):
        res = ''
        res += 'bus id: ' + self.busRouteId
        res += '\nbus name: ' + self.busRouteNm
        res += '\nstart station: ' + self.stStationNm
        res += '\nend station: ' + self.edStationNm
        res += '\nterm: ' + self.term
        res += '\nfirst bus time: ' + self.firstBusTm
        res += '\nlast bus time: ' + self.lastBusTm
        res += '\ncorp name: ' + self.corpNm
        return res

class PointVo:
    def __init__(self, no=None, gps_x=None, gps_y=None):
        self.no = no
        self.gps_x = gps_x
        self.gps_y = gps_y

    def __str__(self):
        return 'no: '+self.no+' ('+ self.gps_x + ' , '+ self.gps_y + ')'


class StationVo:
    def __init__(self, seq=None, stat=None, id=None):
        self.seq=seq
        self.stationNm=stat
        self.arsId=id

    def __str__(self):
        return 'seq: '+self.seq+' / station name: '+self.stationNm+ ' / ars id:'+self.arsId


class BusService:  # 기능제공클래스
    def __init__(self):
        self.url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/%s?ServiceKey=%s&%s=%s'
        self.apiKey = 'BYgs6%2FjSL0du1z8yK4GxYdW1SepukkJ0gXtUP3tGUQpjThEU4JeQKRlspdSnxTWcjia6U6r5oPxW%2F7tK7HZ2sg%3D%3D'

    def getRouteInfoItem(self, busId):  #버스ID로 정보 출력
        url = self.url % ('getRouteInfo', self.apiKey, 'busRouteId', busId)
        print(url)
        html = requests.get(url).text  # url 에 웹 요청
        root = BeautifulSoup(html, 'lxml-xml')  # 파서의 종류를 xml로 지정
        code = root.find('headerCd').get_text()
        msg = root.find('headerMsg').get_text()
        print('처리결과:', msg)
        if code == '0':
            busRouteId = root.find('busRouteId').get_text()
            busRouteNm = root.find('busRouteNm').get_text()
            stStationNm = root.find('stStationNm').get_text()
            edStationNm = root.find('edStationNm').get_text()
            term = root.find('term').get_text()
            firstBusTm = root.find('firstBusTm').get_text()
            lastBusTm = root.find('lastBusTm').get_text()
            corpNm = root.find('corpNm').get_text()

            return BusVo(busRouteId, busRouteNm, stStationNm, edStationNm, term, firstBusTm, lastBusTm, corpNm)
        else:
            return msg

    # 노선id를 전달하면 노선의 경로를 (x,y)
    def getRoutePathList(self, busId):
        url = self.url % ('getRoutePath', self.apiKey, 'busRouteId', busId)
        print(url)
        html = requests.get(url).text  # url 에 웹 요청
        root = BeautifulSoup(html, 'lxml-xml')  # 파서의 종류를 xml로 지정
        code = roo
        t.find('headerCd').get_text()
        msg = root.find('headerMsg').get_text()
        print('처리결과:', msg)
        paths = []
        if code == '0':
            itemList = root.select('itemList')
            for item in itemList:
                no = item.find('no').get_text()
                x = item.find('gpsX').get_text()
                y = item.find('gpsY').get_text()
                paths.append(PointVo(no, x, y))
            return paths
        else:
            return msg

    def getBusRouteList(self, busName):
        url = self.url % ('getBusRouteList', self.apiKey, 'strSrch', busName)
        print(url)
        html = requests.get(url).text  # url 에 웹 요청
        root = BeautifulSoup(html, 'lxml-xml')  # 파서의 종류를 xml로 지정
        code = root.find('headerCd').get_text()
        msg = root.find('headerMsg').get_text()
        print('처리결과:', msg)
        bus = []
        if code == '0':
            itemList = root.select('itemList')
            for item in itemList:
                busRouteId = item.find('busRouteId').get_text()
                busRouteNm = item.find('busRouteNm').get_text()
                stStationNm = item.find('stStationNm').get_text()
                edStationNm = item.find('edStationNm').get_text()
                term = item.find('term').get_text()
                firstBusTm = item.find('firstBusTm').get_text()
                lastBusTm = item.find('lastBusTm').get_text()
                corpNm = item.find('corpNm').get_text()

                bus.append(
                    BusVo(busRouteId, busRouteNm, stStationNm, edStationNm, term, firstBusTm, lastBusTm, corpNm))
            return bus
        else:
            return msg

    def getStaionsByRouteList(self, busId):
        url = self.url % ('getStaionByRoute', self.apiKey, 'busRouteId', busId)
        print(url)
        html = requests.get(url).text  # url 에 웹 요청
        root = BeautifulSoup(html, 'lxml-xml')  # 파서의 종류를 xml로 지정
        code = root.find('headerCd').get_text()
        msg = root.find('headerMsg').get_text()
        print('처리결과:', msg)
        stations = []
        if code == '0':
            itemList = root.select('itemList')
            for item in itemList:
                seq = item.find('seq').get_text()
                stationNm = item.find('stationNm').get_text()
                arsId = item.find('arsId').get_text()
                stations.append(StationVo(seq, stationNm, arsId))
            return stations
        else:
            return msg