from datetime import *
from tkinter import *
from time import sleep

class LoginAdmnistracao:

    #------------------------------- (Tela Operativa) - FUNÇÃO 8º A SER INVOCADA POR FUNÇÃO: confirmarTelaFuncionario() ----------
    def tela_de_operacao(self):
        self.janelaFuncio.destroy()

        self.janelaOper = Tk()
        self.janelaOper.title('Tela Operativa')
        self.janelaOper.iconbitmap('icone2.ico')
        self.janelaOper.configure(background='white')
        self.janelaOper.geometry('500x500+200+100')
        self.janelaOper.state('zoomed')

        #(Tela Operativa) - FRAMES DA TELA DE OPERAÇÃO ------------------------------------

        self.frameTop = Frame(self.janelaOper, width=1400, height=130, bg='#001333')
        self.frameTop.pack(side=TOP)

        self.frameLeft = Frame(self.janelaOper, width=800, height=550, bg='#001333')
        self.frameLeft.pack(side=LEFT)

        self.frameRight = Frame(self.janelaOper, width=550, height=550, bg='#001333') ##c4c0c0
        self.frameRight.pack(side=RIGHT)

        #(Tela Operativa) - LABELS E CAMPOS DE ENTRADA DA TELA DE OPERAÇÃO - DADOS DO OPERADOR -----------------------------

        self.operadorNome = Label(self.frameTop, text='Operador:', font=('arial', 12,'bold'), fg='red', bg='#001333')
        self.operadorNome.place(x=10, y=20)
        self.operadorNomeUser = Label(self.frameTop, text=str(self.operador),font=('arial', 12,'bold'), fg='red', bg='#001333')
        self.operadorNomeUser.place(x=100, y=20)

        self.horaInicial = Label(self.frameTop, text='Horário de Login:', font=('arial', 12,'bold'), fg='red', bg='#001333')
        self.horaInicial.place(x=10, y=60)
        self.horaAtualUser = Label(self.frameTop, text=self.horaLogin, font=('arial', 13,'bold'), fg='red', bg='white')
        self.horaAtualUser.place(x=150, y=60)

        self.multimolde = Label(self.frameTop, text='MULTIMOLDES', font=('arial', 40,'bold'), fg='red', bg='black', width=15)
        self.multimolde.place(x=500, y=20)
        
        self.sair = Button(self.frameTop, text='Sair', font=('arial',14,'bold'), fg='red', bg='white', width=5, command=lambda:self.sairTela())
        self.sair.place(x=1180,y=20)
        
        #(Tela Operativa) - LABELS E CAMPOS DE ENTRADA DA TELA DE OPERAÇÃO - FOMULÁRIO -----------------------------

        '''self.idLabel = Label(self.frameLeft, text='ID:', font=('arial', 16, 'bold'), bg='#001333', fg='red')
        self.idLabel.place(x=230, y=100)
        self.campoId = Entry(self.frameLeft, width=30, font=('arial', 15))
        self.campoId.place(x=300, y=100)
        self.campoId.focus_force()'''

        self.ordemServico = Label(self.frameLeft, text='Ordem de Serviço:', font=('arial', 16, 'bold'), bg='#001333', fg='red')
        self.ordemServico.place(x=70, y=100)
        self.campoServico = Entry(self.frameLeft, width=30, font=('arial', 15), bg='white')
        self.campoServico.place(x=300, y=100)
        
        self.codigoPeca = Label(self.frameLeft, text='Código da Peça:', font=('arial', 16, 'bold'), bg='#001333', fg='red')
        self.codigoPeca.place(x=90, y=200)
        self.campoPeca = Entry(self.frameLeft, width=30, font=('arial', 15))
        self.campoPeca.place(x=300, y=200)
        
        self.tempoProgramado = Label(self.frameLeft, text='Tempo Programado:', font=('arial', 16, 'bold'), bg='#001333', fg='red')
        self.tempoProgramado.place(x=60, y=300)
        self.campoProgramado = Label(self.frameLeft, width=30, font=('arial', 15), bg='white')
        self.campoProgramado.place(x=300, y=300)
        
        self.botConfirmar = Button(self.frameLeft, text='Confirmar', width=10, font=('arial', 15), bg='orange')
        self.botConfirmar.place(x=400, y=400)
        
        #(Tela Operativa) - LABELS QUE IMPRIMEM O CRONÔMETRO - CRONÔMETRO ------------------------------------

        self.seconds = Label(self.frameRight, text='0', font=('arial',30), fg=('red'), width=2)
        self.seconds.place(x=315, y=50)
        self.minutes = Label(self.frameRight, text='0', font=('arial',30), fg=('red'), width=2)
        self.minutes.place(x=260, y=50)
        self.hours = Label(self.frameRight, text='0', font=('arial',30), fg=('red'), width=2)
        self.hours.place(x=205, y=50)

    
        self.chaveControle = False

        
        self.botaoInciarContador = Button(self.frameRight, text='INICIAR', bg='red', fg='white', border=10, font=('arial', 25, 'bold'), command = lambda:self.botao_iniciar())
        self.botaoInciarContador.place(x=205, y=200)

        
        self.chaveFinalizar = False
        
        self.sec = None
        self.minu = None
        self.hou = None

        self.janelaOper.mainloop()

    #(Tela Operativa) - FUNÇÃO 1º A SER INVOCADA POR BOTÃO: botaoInciarContador - TEMPORIZADOR----------------------------

    def botao_iniciar(self):

        if self.chaveControle == False:
            
            self.botFinalizar = Button(self.frameRight, text='FINALIZAR.OS', bg='green', fg='white', border=10, font=('arial', 25, 'bold'), width=15, command = lambda: self.contagemFinalizada())
            self.botFinalizar.place(x=130, y=200)
            self.botaoInciarContador.destroy()
            time = datetime.now().time()
            lista = [str(time)]
            recebe = ''
            for c in lista:
                for i in c:
                    if i == '.':
                        break
                    else:
                        recebe += i
            self.horaInicial = recebe
            
            self.chaveControle = True

        if self.sec == None:
            self.sec = 0
        self.sec = self.sec + 1

        if self.sec >= 59:
            self.sec = 0

            if self.minu == None:
                self.minu = 0
            self.minu = self.minu + 1
            if self.minu >= 59:
                self.minu = 0
            
                if self.hou == None:
                    self.hou = 0
                self.hou = self.hou + 1

        self.seconds['text'] = self.sec
        self.minutes['text'] = self.minu
        self.hours['text'] = self.hou

        if self.chaveFinalizar == False:
            self.seconds.after(1000, self.botao_iniciar)
            
    def contagemFinalizada(self):
            
            self.chaveFinalizar = True
            if self.chaveFinalizar == True:
                self.botFinalizar.destroy()
                self.labFinalizar =  Label(self.frameRight, text='Processesso Finalizado',  bg='green', fg='white', font=('arial', 25, 'bold'))
                self.labFinalizar.place(x=100, y=150)
                
                time = datetime.now().time()
                lista = [str(time)]
                recebe = ''
                for c in lista:
                    for i in c:
                        if i == '.':
                            break
                        else:
                            recebe += i
                horaFinal = recebe
                
                try:
                    print('inicio')
                    self.cursor.execute('use empresa_funcionarios')
                    print('inicio2')
                    self.cursor.execute("insert into monitoria_funcionarios VALUES('id','"+str(self.operador)+"','"+str(self.horaLogin)+"','"+str(self.horaInicial)+"','"+str(horaFinal)+"','invalido','invalido','invalido','invalido','invalido')")
                    print('inicio3')
                    self.banco.commit()
                    print('inicio4')
                except:
                    print('erro ao salvar informações')

            

instancia = LoginAdmnistracao()            

'''

'''


'''
    #------------------------------- (Tela Operativa) - FUNÇÃO 9º A SER INVOCADA POR: sair -----------------
    def sairTela(self):
        if self.chaveFinalizar ==  True:
            self.janelaOper.destroy()
            self.__init__()
        elif self.chaveControle == False:
            self.janelaOper.destroy()
            self.__init__()
        else:
            self.alerta = Tk()
            self.alerta.title('Alerta')
            self.alerta.iconbitmap('icone2.ico')
            self.alerta.resizable(False, False)
            self.alerta.configure(background='yellow')

            largura = 350
            altura = 150

            largura_screen = self.alerta.winfo_screenwidth()
            altura_screen = self.alerta.winfo_screenheight()

            posicaoX = largura_screen/2 - largura/2
            posicaoY = altura_screen/2 - altura/2

            self.alerta.geometry('%dx%d+%d+%d' % (largura, altura, posicaoX, posicaoY))

            labelAlert = Label(self.alerta, text='Sistema em operacação ainda!!', font=('arial', 15, 'bold'), fg='red', bg='yellow')
            labelAlert.place(x=30,y=20)

            botaoAlert = Button(self.alerta, text='OK', width=10, bg='red', fg='white', command = lambda: self.fechar())
            botaoAlert.place(x=140,y=80)

'''