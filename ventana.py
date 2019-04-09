
class Ventana:
    def __init__(self,img,x,y,w,h,type,score):
        self.img = img
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = type
        self.score = score

    def str(self):
        return f'{self.img};{self.x};{self.y};{self.w+self.x};{self.h+self.y};1;{str(self.score)}\n'

    def str_tipo(self):
        return f'{self.img};{self.x};{self.y};{self.w+self.x};{self.h+self.y}{self.type};{str(self.score)}\n'
