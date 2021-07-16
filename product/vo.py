class Product:
    def __init__(self, num=None, name=None, price=None, amount=None):  #None 넣어줘야 나중에 파라미터 생략가능
        self.num = num    #제품번호
        self.name = name  #제품이름
        self.price = price  #제품가격
        self.amount = amount  #수량
