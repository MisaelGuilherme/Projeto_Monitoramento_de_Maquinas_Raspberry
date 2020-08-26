from time import sleep
from tkinter import *
cont = 0
valor = None

janela = Tk()
janela.title('Tela Operativa')
janela.iconbitmap('icone2.ico')
janela.configure(background='white')
janela.geometry('500x500+200+100')
janela.state('zoomed')

#------------------------------ (Tela Operativa) - FRAMES DA TELA DE OPERAÇÃO ------------------------------------

frameTop = Frame(janela, width=1400, height=130, bg='#85c7ed')
frameTop.pack(side=TOP)

frameLeft = Frame(janela, width=800, height=550, bg='#85c7ed')
frameLeft.pack(side=LEFT)

frameRight = Frame(janela, width=550, height=550, bg='#85c7ed') ##c4c0c0
frameRight.pack(side=RIGHT)

#------------------------------ (Tela Operativa) - LABELS E CAMPOS DE ENTRADA DA TELA DE OPERAÇÃO - DADOS DO OPERADOR -----------------------------

operadorNome = Label(frameTop, text='Operador:', font=('arial', 12,'bold'), fg='red', bg='#85c7ed', width=8)
operadorNome.place(x=20, y=20)

horaInicial = Label(frameTop, text='Horário de Login:', font=('arial', 12,'bold'), fg='red', bg='#85c7ed', width=15)
horaInicial.place(x=13, y=60)

multimolde = Label(frameTop, text='MULTIMOLDE', font=('arial', 40,'bold'), fg='#56b0e3', bg='black', width=15)
multimolde.place(x=500, y=20)
#------------------------------ (Tela Operativa) - LABELS E CAMPOS DE ENTRADA DA TELA DE OPERAÇÃO - FOMULÁRIO -----------------------------

iD = Label(frameLeft, text='ID', font=('arial', 16, 'bold'), bg='#85c7ed')
iD.place(x=80, y=60)
campoId = Entry(frameLeft, width=30, font=('arial', 15))
campoId.place(x=120, y=60)

ordemServico = Label(frameLeft, text='Ordem de Serviço', font=('arial', 16, 'bold'), bg='#85c7ed')
ordemServico.place(x=80, y=160)
campoServico = Entry(frameLeft, width=30, font=('arial', 15))
campoServico.place(x=285, y=160)

codigoPeca = Label(frameLeft, text='Código da Peça', font=('arial', 16, 'bold'), bg='#85c7ed')
codigoPeca.place(x=80, y=260)
campoPeca = Entry(frameLeft, width=30, font=('arial', 15))
campoPeca.place(x=265, y=260)

tempoProgramador = Label(frameLeft, text='Tempo Programador', font=('arial', 16, 'bold'), bg='#85c7ed')
tempoProgramador.place(x=80, y=360)
campoProgramador = Entry(frameLeft, width=30, font=('arial', 15))
campoProgramador.place(x=315, y=360)

'''operador = Label(frameLeft, text='Operador', font=('arial', 16, 'bold'), bg='#85c7ed')
operador.place(x=80, y=460)
campoOperador = Entry(frameLeft, width=30, font=('arial', 15))
campoOperador.place(x=200, y=460)'''

#------------------------------ (Tela Operativa) - FUNÇÃO 1º A SER INVOCADA - TEMPORIZADOR----------------------------
sec = None
minu = None
hou = None

havePause = False
def botaoPause():
    pass

def botaoIniciar():

    global botaoInciarContador
    global chaveControle

    if chaveControle == False:
        sleep(1)
        botaoInciarContador.destroy()
        chaveControle = True

    global sec
    global minu
    global hou

    if sec == None:
        sec = 0
    sec = sec + 1

    #TENTATIVA DE PAUSAR O CRONOMETRO
    '''global chavePause
    pausa = sec
    if chavePause == True:
        sec = pausa
    '''  

    if sec >= 59:
        sec = 0

        if minu == None:
            minu = 0
        minu = minu + 1
        if minu >= 59:
            minu = 0
        
            if hou == None:
                hou = 0
            hou = hou + 1

    seconds['text'] = sec
    minutes['text'] = minu
    hours['text'] = hou
    seconds.after(1000, botaoIniciar)

    botPause = Button(frameRight, text='PAUSAR', bg='yellow', fg='white', font=('arial', 18, 'bold'), width=8, command = botaoPause)
    botPause.place(x=160, y=150)
    botStop = Button(frameRight, text='PARAR', bg='red', fg='white', font=('arial', 18, 'bold'), width=8)
    botStop.place(x=310, y=150)

#------------------------------ (Tela Operativa) - LABELS QUE IMPRIMEM O CRONÔMETRO - CRONÔMETRO ------------------------------------

seconds = Label(frameRight, text='0', font=('arial',30), fg=('red'), width=2)
seconds.place(x=325, y=50)
minutes = Label(frameRight, text='0', font=('arial',30), fg=('red'), width=2)
minutes.place(x=270, y=50)
hours = Label(frameRight, text='0', font=('arial',30), fg=('red'), width=2)
hours.place(x=215, y=50)

chaveControle = False
botaoInciarContador = Button(frameRight, text='INICIAR', bg='red', fg='white', font=('arial', 20, 'bold'), command = botaoIniciar)
botaoInciarContador.place(x=230, y=150)


janela.mainloop()
