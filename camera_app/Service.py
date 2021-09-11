import cv2, threading

class CamService:
    def __init__(self):
        self.flag = True    #쓰레드 멈출 조건으로 사용
