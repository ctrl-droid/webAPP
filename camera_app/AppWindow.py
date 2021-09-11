import tkinter as tk
import cv2, threading
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
import os, requests

class AppWin(tk.Frame):#AppWin은 Frame(위젯을 배치하는 판)
    def __init__(self, root=None, geo=None): #root:Tk()객체 geo=창크기위치
        #fr = tk.Frame(self.root)
        super().__init__(root)      # 부모 생성자에 기본 윈도우 전달
        self.root = root            # 기본 윈도우를 멤버변수로 저장
        self.root.geometry(geo)     # 윈도우의 크기 및 위치 설정
        self.root.resizable(True, True)  # 윈도우의 가로, 세로 크기 재조정 가능으로 설정
        self.pack()
        self.sub_fr = None          #버튼 배치할 하위 프레임
        self.img_src = None         #레이블에 출력할 이미지 값
        self.img_label = None       #이미지 출력할 레이블
        self.ent_title = None
        self.fileName_ent = None    #이미지 저장시 파일명 입력받을 엔트리
        self.flag = True    #preview 쓰레드를 실행/중지 제어
        self.flag2 = False  #동영상저장을 실행(True) /중지(False) 제어
        self.pic = None     #사진 저장을 위해 preview의 마지막 영상을 담을 변수
        self.mode = 1   #1:사진 / 2:동영상
        self.create_widgets()

    def read_img(self, path):#path:읽을 이미지 경로
        src = cv2.imread(path) #이미지 파일에서 영상 읽음
        src = cv2.resize(src, (640, 400))#이미지 가로,세로 크기 조절
        img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB) #opencv[b, g, r] => tkinter:[r, g, b]
        img = Image.fromarray(img)  #opencv용 이미지배열값을 필로우용 이미지로 변환
        self.img_src = ImageTk.PhotoImage(image=img) #tkinter용 이미지 변환

    def read_cam(self, flag, flag2):#미리보기, 동영상저장
        cap = cv2.VideoCapture(0)
        codec = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter('pic/tmp.avi', codec, 25.0, (640, 400))
        while flag():
            ret, src = cap.read()
            if ret:
                src = cv2.resize(src, (640, 400))  # 이미지 가로,세로 크기 조절
                img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)  # opencv[b, g, r] => tkinter:[r, g, b]
                img = Image.fromarray(img)  # opencv용 이미지배열값을 필로우용 이미지로 변환
                self.img_src = ImageTk.PhotoImage(image=img)
                #self.img_label['image'] = self.img_src
                self.img_label.configure(image=self.img_src)
                self.img_label.image = self.img_src
                if flag2():
                    out.write(src) #pic/tmp.avi에 영상 저장

            #cv2.waitKey(100)
        self.pic = src
        cap.release()
        out.release()

    def btn1_handler(self):  #사진촬영 버튼 클릭시 호출될 핸들러
        self.flag = False
        self.mode = 1

    def start_preview(self):    #미리보기 함수. 프로그램 시작시 호출
        self.flag = True
        #쓰레드 생성
        th = threading.Thread(target=self.read_cam, args=(lambda:self.flag, lambda:self.flag2))
        th.start()  #쓰레드 시작

    def btn2_handler(self): #저장 버튼 클릭시 호출될 핸들러
        fname = self.fileName_ent.get()  #엔트리에 입력한 파일명
        if fname=='' or fname==None:
            tk.messagebox.showinfo(title='오류', message='파일명 누락')
            return
        if self.mode==1:#사진저장
            cv2.imwrite('pic/'+fname+'.jpg', self.pic)
        else:#동영상저장
            os.rename('pic/tmp.avi', 'pic/'+fname+'.avi')
        self.fileName_ent.delete(0, tk.END)
        self.start_preview()

    def btn3_handler(self):
        self.flag2 = True #미리보기에서 동영상 저장 시작
        self.mode = 2 #저장 번튼 클릭시 저장할 파일의 종류를 동영상을 결정

    def btn4_handler(self):
        self.flag = False #미리보기 중지
        self.flag2 = False #미리보기에서 동영상 저장 중지

    def btn5_handler(self):
        fname = self.fileName_ent.get()  # 엔트리에 입력한 파일명
        if fname == '' or fname == None:
            tk.messagebox.showinfo(title='오류', message='파일명 누락')
            return
        path = 'pic/' + fname + '.jpg'
        cv2.imwrite(path, self.pic)
        f = open(path, 'rb')
        upload = {'file':f}
        params = {'title':fname+'_title'}
        res = requests.post('http://127.0.0.1:5000/test/upload2', files=upload, data=params)
        cont = res.content
        tk.messagebox.showinfo(title='upload', message=cont)
        self.fileName_ent.delete(0, tk.END)
        self.start_preview()

    def create_widgets(self):  # 원하는 구성요소 부착
        self.read_img('start.jpg')
        self.img_label = tk.Label(self, image=self.img_src)
        self.img_label.pack()
        self.ent_title = tk.Label(self, text='파일명:')
        self.ent_title.pack()
        self.fileName_ent = tk.Entry(self, width=60)
        self.fileName_ent.pack()
        self.sub_fr = tk.Frame(self)
        self.sub_fr.pack()
        self.start_preview()

        self.btn1 = tk.Button(self.sub_fr, text='사진촬영')
        self.btn2 = tk.Button(self.sub_fr, text='저장')
        self.btn3 = tk.Button(self.sub_fr, text='동영상시작')
        self.btn4 = tk.Button(self.sub_fr, text='동영상종료')
        self.btn5 = tk.Button(self.sub_fr, text='web upload')

        #버튼 그리드 배치
        self.btn1.grid(row=0, column=0)
        self.btn2.grid(row=0, column=1)
        self.btn3.grid(row=0, column=2)
        self.btn4.grid(row=0, column=3)
        self.btn5.grid(row=0, column=4)

        #버튼에 핸들러 등록
        self.btn1['command'] = self.btn1_handler
        self.btn2['command'] = self.btn2_handler
        self.btn3['command'] = self.btn3_handler
        self.btn4['command'] = self.btn4_handler
        self.btn5['command'] = self.btn5_handler


