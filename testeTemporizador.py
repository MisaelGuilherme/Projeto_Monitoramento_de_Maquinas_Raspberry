from tkinter import *
janela = Tk()
janela.geometry('500x500+200+100')

#------------------------------------ PARAR O TEMPORIZADOR --------------------------
def contagemFinalizada():
    global chaveFinalizar
    chaveFinalizar = True

#------------------------------------ TEMPORIZADOR -----------------------------------
def botaoIniciar():
    global sec
    global minu
    global hou
    global botaoInciarContador
    global chaveControle
    global chaveFinalizar

    if chaveControle == False:
        global botFinalizar
        botFinalizar = Button(janela, text='FINALIZAR.OS', font=('arial', 12, 'bold'), width=15, command=contagemFinalizada)
        botFinalizar.pack()
        chaveControle = True
        botaoInciarContador.destroy()

    if sec == None:
        sec = 0
    sec = sec + 1
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

    if chaveFinalizar == False:
        seconds.after(1000, botaoIniciar)
    else:
        botFinalizar.destroy()
#------------------------------------ LABELS QUE IMPRIMEM O CRONÔMETRO - CRONÔMETRO ------------------------------------
sec = None
minu = None
hou = None

seconds = Label(janela, text='0', font=('arial',30), width=2)
seconds.place(x=325, y=50)
minutes = Label(janela, text='0', font=('arial',30), width=2)
minutes.place(x=270, y=50)
hours = Label(janela, text='0', font=('arial',30), width=2)
hours.place(x=215, y=50)

chaveControle = False
chaveFinalizar = False


botaoInciarContador = Button(janela, text='INICIAR', font=('arial', 20, 'bold'), command = botaoIniciar)
botaoInciarContador.place(x=230, y=150)
'''
botFinalizar = Button(janela, text='FINALIZAR.OS', font=('arial', 20, 'bold'), width=15, command=contagemFinalizada)
botFinalizar.place(x=180, y=250)
'''

janela.mainloop()