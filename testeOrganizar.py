from datetime import *
from tkinter import *
from time import sleep

class LoginAdmnistracao:

    #------------------------------- (Tela Operativa) - FUNÇÃO 8º A SER INVOCADA POR FUNÇÃO: confirmarTelaFuncionario() ----------
    def __init__(self):

        self.janelaTempExtra = Tk()
        self.janelaTempExtra.title('Tela Operativa')
        self.janelaTempExtra.iconbitmap('icone2.ico')
        self.janelaTempExtra.configure(background='#870000')
        self.janelaTempExtra.geometry('550x350+200+100')
        
        self.largura = 550
        self.altura = 350

        self.largura_screen = self.janelaTempExtra.winfo_screenwidth()
        self.altura_screen = self.janelaTempExtra.winfo_screenheight()

        self.posicaoX = self.largura_screen/2 - self.largura/2
        self.posicaoY = self.altura_screen/2 - self.altura/2

        self.janelaTempExtra.geometry('%dx%d+%d+%d' % (self.largura, self.altura, self.posicaoX, self.posicaoY))
        
        lt = Label(self.janelaTempExtra, text='Tempo Extra', font=('arial',20,'bold'), bg='#870000', fg='white')
        lt.place(x=195, y=10)
        
        lh = Label(self.janelaTempExtra, text='Horas:', font=('arial',20,'bold'), bg='#870000', fg='white')
        lh.place(x=70, y=135)
        lh.focus_force()
        
        ll = Entry(self.janelaTempExtra, font=('arial',15,'bold'), width=5)
        ll.place(x=170, y=140)
        
        lm = Label(self.janelaTempExtra, text='Minutos:', font=('arial',20,'bold'), bg='#870000', fg='white')
        lm.place(x=270,y=135)
        
        mm = Entry(self.janelaTempExtra, font=('arial',15,'bold'), width=5)
        mm.place(x=400,y=140)
        
        bc = Button(self.janelaTempExtra, text='Confirmar', font=('arial',15,'bold'), bg='orange', fg='white')
        bc.place(x=225,y=260)
        

        self.janelaTempExtra.mainloop()

instancia = LoginAdmnistracao()            