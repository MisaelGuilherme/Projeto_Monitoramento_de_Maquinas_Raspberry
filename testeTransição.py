from tkinter import *

class loginJanela:

    def __init__(self):
        self.janela = Tk()
        print('FUNCIONA 1')
        self.botao = Button(self.janela, text='vermelho', command=lambda:self.a()).pack()
        self.janela.mainloop()
    def a(self):
        self.janela.destroy()
        self.botao_azul()
    def botao_azul(self):
        self.janela2 = Tk()
        print('FUNCIONA 2')
        self.botao2 = Button(self.janela2, text='Azul', command=lambda:self.b()).pack()
        self.janela2.mainloop()
    def b(self):
        self.janela2.destroy()
        self.__init__()
            
lp = loginJanela()
