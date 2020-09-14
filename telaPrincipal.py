#Pogramador: Misael Jesus

from datetime import *
from tkinter import *
from time import sleep
#import sqlite3
import mysql.connector

class LoginAdmnistracao:
    
    #------------------------------- (Login Funcionário) - FUNÇÃO 1º A SER INICIADA -------------------------

    def __init__(self):
        
        self.janelaFuncio = Tk()
        self.janelaFuncio.title('Login Funcionário')
        self.janelaFuncio.iconbitmap('icone2.ico')
        self.janelaFuncio.configure(background='white')
        self.janelaFuncio.resizable(False, False)
        self.janelaFuncio.geometry('500x500+200+100')
        
        self.largura = 500
        self.altura = 500

        self.largura_screen = self.janelaFuncio.winfo_screenwidth()
        self.altura_screen = self.janelaFuncio.winfo_screenheight()

        self.posicaoX = self.largura_screen/2 - self.largura/2
        self.posicaoY = self.altura_screen/2 - self.altura/2

        self.janelaFuncio.geometry('%dx%d+%d+%d' % (self.largura, self.altura, self.posicaoX, self.posicaoY))
        
        self.imgFun = PhotoImage(file="funcionario.png")

        self.imagemPricipalFun = Label(self.janelaFuncio, image=self.imgFun, bg='white')
        self.imagemPricipalFun.place(x=170,y=10)

        self.labelLogin = Label(self.janelaFuncio, text='Usuário', bg='white', fg='#3e8e94', font=('arial',11,'bold'))
        self.labelLogin.place(x=80, y=200)

        self.campoLogin = Entry(self.janelaFuncio, width=30)
        self.campoLogin.place(x=150, y=200)
        self.campoLogin.focus_force()

        self.labelSenha = Label(self.janelaFuncio, text='Senha', bg='white', fg='#3e8e94', font=('arial',11,'bold'))
        self.labelSenha.place(x=80, y=250)

        self.campoSenha = Entry(self.janelaFuncio, width=30, show='*')
        self.campoSenha.place(x=150, y=250)

        self.botao = Button(self.janelaFuncio, text='Confirmar', fg='white', bg='#3e8e94', border=0, font=('arial', 10, 'bold'), width=10, command = lambda: self.confirmar_tela_funcionario())
        self.botao.place(x=200, y=300)

        self.lbCadastrar = Label(self.janelaFuncio, text='Cadastrar Funcionário', bg='white', fg='#3e8e94',font=('arial',10,'bold'))
        self.lbCadastrar.place(x=340, y=410)
        self.botCadastrar = Button(self.janelaFuncio, text='Cadastrar',fg='white', bg='#3e8e94', border=0, font=('arial', 10, 'bold'), width=10, command = lambda: self.tela_admin(1))
        self.botCadastrar.place(x=370, y=440)

        self.janelaFuncio.mainloop()
    
    #------------------------------- (Login Administração) - FUNÇÃO 2º A SER INVOCADA POR: botCadastrar ------------------

    def tela_admin(self, botao):
    
        #------------------------------- (Login Administração) - Configurações da Janela ------------------------------- 
        #------------------------------- (Login Administração) - Dimensões da Janela -----------------------------------
        #------------------------------- (Login Administração) - Resolução do Sistema ----------------------------------
        #------------------------------- (Login Administração) - Posicão da Tela ---------------------------------------
        #------------------------------- (Login Administração) - Definição da Janela -----------------------------------
        #------------------------------- (Login Administração) - Imagem Logo da Empresa --------------------------------
        self.janelaADM = Toplevel()
        self.janelaADM.title('Login Administração')
        self.janelaADM.iconbitmap('icone2.ico')
        self.janelaADM.resizable(False, False)
        self.janelaADM.configure(background='white')

        self.largura = 500
        self.altura = 500

        self.largura_screen = self.janelaADM.winfo_screenwidth()
        self.altura_screen = self.janelaADM.winfo_screenheight()

        self.posicaoX = self.largura_screen/2 - self.largura/2
        self.posicaoY = self.altura_screen/2 - self.altura/2

        self.janelaADM.geometry('%dx%d+%d+%d' % (self.largura, self.altura, self.posicaoX, self.posicaoY))

        self.imgAdm = PhotoImage(file="icone1.png")

        self.imagemPricipalAdm = Label(self.janelaADM, image=self.imgAdm, bg='white')
        self.imagemPricipalAdm.place(x=170,y=10)

        #------------------------------- Label e campo da Tela Login Administração-------------------------------

        self.admLabelPrincipal = Label(self.janelaADM, text='Senha Admin', fg='#3e8e94', font=('arial', 12, 'bold'), bg='white')
        self.admLabelPrincipal.place(x=40,y=210)

        self.admSenhaPrincipal = Entry(self.janelaADM, width=30, border=2, show='*')
        self.admSenhaPrincipal.place(x=160,y=210)
        self.admSenhaPrincipal.focus_force()

        self.admBotaoPrincipal = Button(self.janelaADM, text='Continuar', bg='#3e8e94', fg='white', border=0, font=('arial', 12), width=10, command = lambda:self.verificar_adm(botao))
        self.admBotaoPrincipal.place(x=210,y=300)

        self.janelaADM.mainloop()
    
    #------------------------------- (Login Administração) - FUNÇÃO 3º A SER INVOCADA POR: admBotaoPrincipal -----------------

    def verificar_adm(self, contV):
        if str(self.admSenhaPrincipal.get()).isnumeric():
            self.valor = self.admSenhaPrincipal.get()
            if self.valor == str(123) and contV == 1:                
                self.janelaADM.destroy()
                self.tela_cadastrar()
            elif self.valor == str(123) and contV == 2:
                self.janelaADM.destroy()
                self.tempo_extra()
                
            else:
                self.labelErro2 = Label(self.janelaADM, text='Senha Incorreta. Tente Novamente!', bg='white', fg='#bf0606')
                self.labelErro2.place(x=157, y=233)
        elif self.admSenhaPrincipal.get() == '':
            self.labelErro1 = Label(self.janelaADM, text='Preencha o campo!', bg='white', fg='#bf0606', width=26)
            self.labelErro1.place(x=160, y=233)
        else:
            self.labelErro2 = Label(self.janelaADM, text='Senha Incorreta. Tente Novamente!', bg='white', fg='#bf0606')
            self.labelErro2.place(x=157, y=233)
    def tempo_extra(self):
        
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
        
        self.ll = Entry(self.janelaTempExtra, font=('arial',15,'bold'), width=5)
        self.ll.place(x=170, y=140)
        
        lm = Label(self.janelaTempExtra, text='Minutos:', font=('arial',20,'bold'), bg='#870000', fg='white')
        lm.place(x=270,y=135)
        
        self.mm = Entry(self.janelaTempExtra, font=('arial',15,'bold'), width=5)
        self.mm.place(x=400,y=140)
        
        bc = Button(self.janelaTempExtra, text='Confirmar', font=('arial',15,'bold'), bg='orange', fg='white', command= lambda: self.verificar_tempo_extra())
        bc.place(x=225,y=260)
        
        self.janelaTempExtra.mainloop()

    def verificar_tempo_extra(self):
        def alertaTE(vlr):
            self.alerta = Toplevel()
            self.alerta.title('Alerta')
            self.alerta.iconbitmap('icone2.ico')
            self.alerta.resizable(False, False)
            self.alerta.configure(background='white')

            largura = 350
            altura = 150

            largura_screen = self.alerta.winfo_screenwidth()
            altura_screen = self.alerta.winfo_screenheight()

            posicaoX = largura_screen/2 - largura/2
            posicaoY = altura_screen/2 - altura/2

            self.alerta.geometry('%dx%d+%d+%d' % (largura, altura, posicaoX, posicaoY))
            
            if vlr == 1:
                labelAlert = Label(self.alerta, text='Verifique os Campos!', font=('arial', 15, 'bold'), fg='red', bg='white')
                labelAlert.place(x=75,y=20)
            elif vlr == 2:
                labelAlert = Label(self.alerta, text='Valor mínimo: 5 minutos', font=('arial', 15, 'bold'), fg='red', bg='white')
                labelAlert.place(x=75,y=20)
            botaoAlert = Button(self.alerta, text='OK', width=10, bg='red', fg='white', command = lambda: self.fechar())
            botaoAlert.place(x=130,y=90)
        
        if self.ll.get() == '' or self.mm.get() == '':
            alertaTE(1)

        
        elif str(self.ll.get()).isnumeric() == False or str(self.mm.get()).isnumeric() == False:
            alertaTE(1)
        
        elif int(self.mm.get()) < 5:
            alertaTE(2)
        else:
            self.configurar_tempo_extra()

    def configurar_tempo_extra(self):
        ll = self.ll.get()
        mm = self.mm.get()
        
        self.janelaTempExtra.destroy()
        
        self.seconds['text'] = '00'
        self.minutes['text'] = '00'
        self.hours['text'] = '00'
        
        self.chaveControle = False
        self.chaveFinalizar = False

        self.sec = None

        self.minu = None

        self.hou = None

        self.botaoReabilitar.destroy()
        
        self.labFinalizar.destroy()
        
        self.mi = 0
        self.se = 0
        self.tempHora = ll
        self.tempMin = mm
        
        if int(self.tempHora) == 0:
            self.ho = 0
            print(self.ho)
            if int(self.tempMin) == 0:
                self.mi = 0
                self.se = 0
                print(self.mi)
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                self.mi = int(self.tempMin) // 2
                a = int(self.tempMin)/2
                b = str(a)
                c = int(b[-1])
                d = (c*10) - 20
                self.se = d
                print(self.mi)
                print(self.se)
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                self.mi = int(self.tempMin) // 2
                self.se = 0
                print(self.mi)
                print(self.se)
            elif int(self.tempMin) == 1:
                self.mi = 0
                self.se = (int(self.tempMin) * 60 ) // 2
                print(self.mi)
                print(self.se)
            #============================ ANALISAR O CODIGO =======================
            '''elif int(self.tempMin) == 2:
                self.mi = 1
                self.se = 0
                print(self.mi)
                print(self.se)'''
        
        elif int(self.tempHora) == 1:
            self.ho = 0
            print(self.ho)
            if int(self.tempMin) == 0:
                self.mi = (int(self.tempHora) * 60) // 2
                self.se = 0
                print(self.mi)
                print(self.se)
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                self.mi = ((int(self.tempHora) * 60) // 2) + (int(self.tempMin) // 2)
                a = int(self.tempMin)/2
                b = str(a)
                c = int(b[-1])
                d = (c*10) - 20
                self.se = d
                print(self.mi)
                print(self.se)
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                self.mi = ((int(self.tempHora) * 60) // 2) + (int(self.tempMin) // 2)
                self.se = 0
                print(self.mi)
                print(self.se)
            elif int(self.tempMin) == 1:
                self.mi = (int(self.tempHora) * 60) // 2 
                self.se = (int(self.tempMin) * 60) // 2
                print(self.mi)
                print(self.se)
        
        elif int(self.tempHora) > 1 and int(self.tempHora) % 2 == 0:
            self.ho = int(self.tempHora) // 2
            print(self.ho)
            if int(self.tempMin) == 0:
                self.mi = 0
                self.se = 0
                print(self.mi)
                print(self.se)
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                self.mi = int(self.tempMin) // 2
                a = int(self.tempMin)/2
                b = str(a)
                c = int(b[-1])
                d = (c*10) - 20
                self.se = d
                print(self.mi)
                print(self.se)
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                self.mi = int(self.tempMin) // 2
                self.se = 0
                print(self.mi)
                print(self.se)
            elif int(self.tempMin) == 1:
                self.mi = 0
                self.se = (int(self.tempMin) * 60) // 2
                print(self.mi)
                print(self.se)
        elif int(self.tempHora) > 1 and int(self.tempHora % 2 != 0):
            self.ho = int(self.tempHora) // 2
            print(self.ho)
            a1 = int(self.tempHora)/2
            b2 = str(a)
            c3 = int(b[-1])
            d4 = (c*10) - 20
            
            if int(self.tempMin) == 0:
                self.mi = d4
                self.se = 0
                print(self.mi)
                print(self.se)
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                self.mi = (d4) + (int(self.tempMin) // 2)
                a = int(self.tempMin)/2
                b = str(a)
                c = int(b[-1])
                d = (c*10) - 20
                self.se = d
                print(self.mi)
                print(self.se)
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                self.mi = (d4) + (int(self.tempMin) // 2)
                self.se = 0
                print(self.mi)
                print(self.se)
            elif int(self.tempMin) == 1:
                self.mi = d4
                self.se = (int(self.tempMin) * 60) // 2        
                print(self.mi) 

        #Transformando a hora, minuto e segundo em decimal para exibir no label o tempo extra
        if int(self.tempHora) > 0 and int(self.tempHora) < 10:
            A = int(self.tempHora) / 100
            B = str(A)
            final1 = B[2:]
        elif int(self.tempHora) == 0:
            final1 = '00'
        else: 
            final1 = str(self.tempHora)
            
        if int(self.tempMin) > 0 and int(self.tempMin) < 10:
            A = int(self.tempMin) / 100
            B = str(A)
            final2 = B[2:]
        elif int(self.tempMin) == 0:
            final2 = '00'
        else: 
            final2 = str(self.tempMin)
            
        if int(self.tempSeg) > 0 and int(self.tempSeg) < 10:
            A = int(self.tempSeg) / 100
            B = str(A)
            final3 = B[2:]
        elif int(self.tempSeg) == 0:
            final3 = '00'
        else: 
            final3 = str(self.tempSeg)
        
        #Armazenando na variável já formatado
        self.tempProgExt = final1+':'+final2+':'+final3
        print(self.tempProgExt)
        
        #Exibindo no label o horário adcionado após o tempo ser esgotado
        self.campoProExt = Label(self.frameLeft, text=self.tempProgExt, width=15, font=('arial', 15, 'bold'), bg='white', fg='red')
        self.campoProExt.place(x=300, y=400)
        
        #Invocando o botão sair(login) após o horário ser adcionado
        self.sair = Button(self.frameTop, text='Sair', font=('arial',14,'bold'), fg='white', bg='red', width=5, command=lambda:self.sairTela())
        self.sair.place(x=1180,y=20)
        
        #Botão inciar a contagem do cronômetro
        self.botaoInciarContador = Button(self.frameRight, text='INICIAR', bg='green', fg='white',border=5, relief='ridge', font=('arial', 25, 'bold'), command = lambda:self.botao_iniciar())
        self.botaoInciarContador.place(x=205, y=200)
            
    #------------------------------- (Tela Cadastrar) - FUNÇÃO 4º A SER INVOCADA POR FUNÇÃO: verificar_adm() ------------------

    def tela_cadastrar(self):
        self.janelaCad = Toplevel()
        self.janelaCad.title('Cadastro')
        self.janelaCad.iconbitmap('icone2.ico')
        self.janelaCad.resizable(False, False)
        self.janelaCad.configure(background='white')

        self.largura = 500
        self.altura = 500

        self.largura_screen = self.janelaCad.winfo_screenwidth()
        self.altura_screen = self.janelaCad.winfo_screenheight()

        self.posicaoX = self.largura_screen/2 - self.largura/2
        self.posicaoY = self.altura_screen/2 - self.altura/2

        self.janelaCad.geometry('%dx%d+%d+%d' % (self.largura, self.altura, self.posicaoX, self.posicaoY))

        self.lbtitle = Label(self.janelaCad, text='Cadastrar Funcionário', font=('arial', 15, 'bold'), bg='white', fg='#3e8e94')
        self.lbtitle.place(x=170,y=10)

        self.lbNome = Label(self.janelaCad, text='Nome:', font=('arial',12,'bold'), bg='white', fg='#3e8e94')
        self.lbNome.place(x=90, y=80)

        self.lbCpf = Label(self.janelaCad, text='CPF:', font=('arial',12,'bold'), bg='white', fg='#3e8e94')
        self.lbCpf.place(x=100, y=150)

        self.lbSenha = Label(self.janelaCad, text='Senha:', font=('arial',12,'bold'), bg='white', fg='#3e8e94')
        self.lbSenha.place(x=90, y=220)

        self.lbConfSenha = Label(self.janelaCad, text='Confirme a Senha:', font=('arial',12,'bold'),  bg='white', fg='#3e8e94')
        self.lbConfSenha.place(x=20, y=300)

        self.campNome = Entry(self.janelaCad, width=25, font=12)
        self.campNome.place(x=180, y=80)
        self.campNome.focus_force()

        self.campCpf = Entry(self.janelaCad, width=25, font=12)
        self.campCpf.place(x=180, y=150)

        self.campSenha = Entry(self.janelaCad, width=25, font=12, show='*')
        self.campSenha.place(x=180, y=220)

        self.confSenha = Entry(self.janelaCad, width=25, font=12, show='*')
        self.confSenha.place(x=180, y=300)

        self.cadastrar = Button(self.janelaCad, text='Cadastrar', font=12, command = lambda: self.conferir_valores(),bg='#3e8e94', fg='white')
        self.cadastrar.place(x=230,y=370)
        self.janelaCad.mainloop()

    #--------------------------- (Conferir Campos Tela Cadastrar) - FUNÇÃO 5º A SER INVOCADA POR: cadastrar ------------------
    
    def conferir_valores(self):
        #CASO O CAMPO "NOME" DA TELA CADASTRO DO FUNCIONÁRIO ESTEJA VAZIA
        if self.campNome.get() == '':
            self.error = Label(self.janelaCad, text='Preencha o campo!', fg='red', bg='white', width=30)
            self.error.place(x=175, y=110)
            
        #CASO O CAMPO "NOME" DA TELA CADASTRO DO FUNCIONÁRIO SEJA DIGITADO NÚMEROS
        elif str(self.campNome.get()).isnumeric():
            self.error = Label(self.janelaCad, text='O uso de números é invalido!', fg='red', bg='white')
            self.error.place(x=210, y=110)
            
        #SENÃO O A MENSAGEM DE ERROS SUMIRA
        else:
            self.error = Label(self.janelaCad, text='', fg='red', bg='white', width=30)
            self.error.place(x=210, y=110)
            
        #CASO O CAMPO "CPF" DA TELA CADASTRO DO FUNCIONÁRIO ESTEJA VAZIA
        if self.campCpf.get() == '':
            self.error = Label(self.janelaCad, text='Preencha o campo!', fg='red', bg='white')
            self.error.place(x=230, y=180)
        
        #CASO O CAMPO "CPF" DA TELA CADASTRO DO FUNCIONÁRIO SEJA DIGITADO LETRAS
        elif str(self.campCpf.get()).isnumeric() == False:
            self.error = Label(self.janelaCad, text='O campo precisa ser numérico', fg='red', bg='white')
            self.error.place(x=210, y=180)
            
        #CASO O CAMPO "CPF" DA TELA CADASTRO DO FUNCIONÁRIO SEJA DIFERENTE DE 11 NÚMEROS
        elif len(self.campCpf.get()) != 11:
            print(len(self.campCpf.get()))
            self.error = Label(self.janelaCad, text='O CPF precisa conter 11 dígitos', fg='red', bg='white')
            self.error.place(x=210, y=180)

        #SENÃO A MENSAGEM DE ERROS SUMIRÁ
        else:
            self.error = Label(self.janelaCad, text='', fg='red', bg='white', width=30)
            self.error.place(x=210, y=180)
        
        #CASO O CAMPO "SENHA E CONFIRMAR SENHA" DA TELA CADASTRO DO FUNCIONÁRIO ESTEJA VAZIA
        if self.campSenha.get() == '' or self.confSenha.get() == '':
            self.error = Label(self.janelaCad, text='Preencha o campo!', fg='red', bg='white', width=30)
            self.error.place(x=175, y=325)
            
        #PROCESSO DE VERIFICÇÃO SE AS SENHAS SÃO IGUAIS
        elif str(self.campSenha.get()).isnumeric() == True and str(self.confSenha.get()).isnumeric() == True and str(self.campSenha.get()).isnumeric() == str(self.confSenha.get()).isnumeric() :
            if len(self.campSenha.get()) != 4 or len(self.confSenha.get()) != 4:
                self.error = Label(self.janelaCad, text='A senha precisa conter 4 dígitos', fg='red', bg='white', width=30)
                self.error.place(x=175, y=325) 
                
            elif self.campSenha.get() != self.confSenha.get():
                self.error = Label(self.janelaCad, text='As senhas não coincidem', fg='red', bg='white', width=30)
                self.error.place(x=175, y=325)
            else:
                self.error = Label(self.janelaCad, text='', bg='white', width=30)
                self.error.place(x=175, y=325)
                self.banco_de_dados_cadastro()
        
        #CASO O CAMPO "SENHA E CONFIRMAR SENHJA" DA TELA CADASTRO DO FUNCIONÁRIO SEJA DIGITADO LETRAS
        else:
            self.error = Label(self.janelaCad, text='A senha precisa ser numérica', fg='red', bg='white', width=30)
            self.error.place(x=175, y=325)

    #------------------------------- (Banco de Dados) - FUNÇÃO 6º A SER INVOCADA POR: conferir_valores() -------------------

    def banco_de_dados_cadastro(self):
        cpf = self.campCpf.get()
        nome = self.campNome.get().upper()
        senha = self.campSenha.get()
        try:
            banco = mysql.connector.connect(
            host="localhost",
            user="root",
            password="")
            
            cursor = banco.cursor()
            cursor.execute('USE empresa_funcionarios')
            cursor.execute('select * from funcionarios where cpf = '+str(cpf))
            valido = cursor.fetchall()
            
            #VERIFICANDO SE O CPF DO FUNCIONÁRIO JÁ ESTÁ CADASTRADO
            if len(valido) == 1: 
                
                #SE O CPF JÁ FOI CADASTRO APARECERÁ UM ALERTA
                self.alerta = Toplevel()
                self.alerta.title('Alerta')
                self.alerta.iconbitmap('icone2.ico')
                self.alerta.resizable(False, False)
                self.alerta.configure(background='white')

                largura = 250
                altura = 100

                largura_screen = self.alerta.winfo_screenwidth()
                altura_screen = self.alerta.winfo_screenheight()

                posicaoX = largura_screen/2 - largura/2
                posicaoY = altura_screen/2 - altura/2

                self.alerta.geometry('%dx%d+%d+%d' % (largura, altura, posicaoX, posicaoY))

                labelAlert = Label(self.alerta, text='CPF já Cadastrado!', font=('arial', 10, 'bold'), fg='red', bg='white')
                labelAlert.place(x=65,y=20)

                botaoAlert = Button(self.alerta, text='OK', width=10, bg='red', fg='white', command = lambda: self.fechar())
                botaoAlert.place(x=90,y=60)
            
            #CADASTRANDO ENVIANDO DADOS DO FUNCIONÁRIO PRO BANCO DE DADOS
            else:
                    
                cursor.execute("INSERT INTO funcionarios VALUES(id,'"+nome+"','"+cpf+"','"+senha+"')")
                banco.commit()
                comando = 1
                
                self.janelaCad.destroy()    
                
                self.alerta = Toplevel()
                self.alerta.title('Alerta')
                self.alerta.iconbitmap('icone2.ico')
                self.alerta.resizable(False, False)
                self.alerta.configure(background='white')

                largura = 250
                altura = 100

                largura_screen = self.alerta.winfo_screenwidth()
                altura_screen = self.alerta.winfo_screenheight()

                posicaoX = largura_screen/2 - largura/2
                posicaoY = altura_screen/2 - altura/2

                self.alerta.geometry('%dx%d+%d+%d' % (largura, altura, posicaoX, posicaoY))

                labelAlert = Label(self.alerta, text='Funcionário Cadastrado!', font=('arial', 10, 'bold'), fg='green', bg='white')
                labelAlert.place(x=50,y=20)

                botaoAlert = Button(self.alerta, text='OK', width=10, bg='green', fg='white', command = lambda: self.fechar())
                botaoAlert.place(x=90,y=60)
        
        #CASO O A LIGAÇÃO OU AS CONDIÇÕES NÃO TENHAM SIDO EXECUTADAS COM ÊXITOS
        except:
            print('Erro ao inserir no Banco de Dados:')#, erro)
    
    #FUNCÃO PARA DESTRUIR TODOS OS ALERTAS
    def fechar(self):
        self.alerta.destroy()
        
    #------------------------------- (Banco de Dados) - FUNÇÃO 7º A SER INVOCADA POR: botao ------------------------------- 
    def confirmar_tela_funcionario(self):
        
        #verificando se o campo "login" é numérico e possui 11 caracteres
        if str(self.campoLogin.get()).isnumeric() and len(self.campoLogin.get()) == 11:
            self.user = self.campoLogin.get()

            #verificando se a senha é númerica e possui 4 caracteres
            if str(self.campoSenha.get()).isnumeric() and len(self.campoSenha.get()) == 4:
                self.password = self.campoSenha.get()
                users = self.campoLogin.get()
                password = self.campoSenha.get()
                
                #tentamos conectar-se ao banco
                try:
                    self.banco = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "")
                    
                    #verificando se usuário existe no banco de dados
                    self.cursor = self.banco.cursor()
                    self.cursor.execute('use empresa_funcionarios')
                    self.cursor.execute("select * from funcionarios where cpf = '"+users+"' and senha = '"+password+"'")
                    valido = self.cursor.fetchall()
                    
                    #pegando hora atual de login caso encontrar resultado na busca
                    if len(valido) == 1:
                        self.operador = valido[0][1]
                        time = datetime.now().time()
                        lista = [str(time)]
                        recebe = ''
                        for c in lista:
                            for i in c:
                                if i == '.':
                                    break
                                else:
                                    recebe += i
                        self.horaLogin = recebe
                        self.janelaFuncio.destroy()
                        self.tela_de_operacao()
                    
                    #alerta caso o usuário não seja encontrado
                    else:
                        self.alerta = Toplevel()
                        self.alerta.title('Alerta')
                        self.alerta.iconbitmap('icone2.ico')
                        self.alerta.resizable(False, False)
                        self.alerta.configure(background='white')

                        self.largura = 250
                        self.altura = 100

                        self.largura_screen = self.alerta.winfo_screenwidth()
                        self.altura_screen = self.alerta.winfo_screenheight()

                        self.posicaoX = self.largura_screen/2 - self.largura/2
                        self.posicaoY = self.altura_screen/2 - self.altura/2

                        self.alerta.geometry('%dx%d+%d+%d' % (self.largura, self.altura, self.posicaoX, self.posicaoY))

                        self.labelAlert = Label(self.alerta, text='Login Não Existe!', font=('arial', 10, 'bold'), fg='red', bg='white')
                        self.labelAlert.place(x=70,y=20)

                        self.botaoAlert = Button(self.alerta, text='OK', width=10, bg='red', fg='white', command=lambda:self.fechar())
                        self.botaoAlert.place(x=90,y=60)
                        
                #mensaem de erro caso ocorra alguma excessão ao tentar logar
                except:
                    print('Error ao tentar logar')
            
            #caso o campo "senha" esteja vazio
            elif self.campoSenha.get() == '':
                self.labelError = Label(self.janelaFuncio, text='Preencha o campo!', fg='#bf0606', bg='white', width=40)
                self.labelError.place(x=100, y=165)   
            
            #caso o campo "senha" diferentee de 11 caracteres
            else:
                self.labelError = Label(self.janelaFuncio, text='Usuário ou Senha Incorreta!', fg='#bf0606', bg='white', width=40)
                self.labelError.place(x=100, y=165)
        
        #caso o campo "login" esteja vazio
        elif self.campoSenha.get() == '':
            self.labelError = Label(self.janelaFuncio, text='Preencha o campo!', fg='#bf0606', bg='white', width=40)
            self.labelError.place(x=100, y=165) 
        
        #se caso o campo "login" seja diferente de 11 caracteres
        else:
            self.labelError = Label(self.janelaFuncio, text='Usuário ou Senha Incorreta!', fg='#bf0606', bg='white', width=40)
            self.labelError.place(x=100, y=165)

    #------------------------------- (Tela Operativa) - FUNÇÃO 8º A SER INVOCADA POR FUNÇÃO: confirmarTelaFuncionario() ----------
    def tela_de_operacao(self):

        self.janelaOper = Tk()
        self.janelaOper.title('Tela Operativa')
        self.janelaOper.iconbitmap('icone2.ico')
        self.janelaOper.configure(background='#2e2e2e')
        self.janelaOper.geometry('500x500+200+100')
        self.janelaOper.state('zoomed')

        #(Tela Operativa) - FRAMES DA TELA DE OPERAÇÃO

        self.frameTop = Frame(self.janelaOper, width=1400, height=130, bg='#001333',highlightthickness=3,highlightcolor='black')
        self.frameTop.config(highlightbackground='black')
        self.frameTop.pack(side=TOP)

        self.frameLeft = Frame(self.janelaOper, width=800, bg='#001333', height=550,highlightthickness=3,highlightcolor='black')
        self.frameLeft.config(highlightbackground='black')
        self.frameLeft.pack(side=LEFT)

        self.frameRight = Frame(self.janelaOper, width=550, height=550, bg='#001333',highlightthickness=3,highlightcolor='black') ##c4c0c0
        self.frameRight.config(highlightbackground='black')
        self.frameRight.pack(side=RIGHT)

        #(Tela Operativa) - LABELS E CAMPOS DE ENTRADA DA TELA DE OPERAÇÃO - DADOS DO OPERADOR 

        self.operadorNome = Label(self.frameTop, text='Operador:', font=('arial', 12,'bold'), fg='red', bg='#001333')
        self.operadorNome.place(x=10, y=20)
        self.operadorNomeUser = Label(self.frameTop, text=str(self.operador),font=('arial', 12,'bold'), fg='red', bg='#001333')
        self.operadorNomeUser.place(x=100, y=20)

        self.horaInicialLb = Label(self.frameTop, text='Horário de Login:', font=('arial', 12,'bold'), fg='red', bg='#001333')
        self.horaInicialLb.place(x=10, y=60)
        self.horaAtualUser = Label(self.frameTop, text=self.horaLogin, font=('arial', 13,'bold'), fg='red', bg='white')
        self.horaAtualUser.place(x=160, y=60)

        self.multimolde = Label(self.frameTop, text='MULTIMOLDES', font=('arial', 40,'bold'), fg='red', bg='#001333', width=15)
        self.multimolde.place(x=500, y=20)
        
        self.sair = Button(self.frameTop, text='Sair', font=('arial',14,'bold'), fg='white', bg='red', width=5, command=lambda:self.sairTela())
        self.sair.place(x=1180,y=20)
        
        #(Tela Operativa) - LABELS E CAMPOS DE ENTRADA DA TELA DE OPERAÇÃO - FOMULÁRIO

        self.ordemServico = Label(self.frameLeft, text='Ordem de Serviço:', font=('arial', 16, 'bold'), bg='#001333', fg='red')
        self.ordemServico.place(x=70, y=100)
        self.campoServico = Entry(self.frameLeft, width=25, font=('arial', 15), bg='white')
        self.campoServico.place(x=300, y=100)
        self.campoServico.focus_force()
        
        self.codigoPeca = Label(self.frameLeft, text='Código da Peça:', font=('arial', 16, 'bold'), bg='#001333', fg='red')
        self.codigoPeca.place(x=90, y=200)
        self.campoPeca = Entry(self.frameLeft, width=25, font=('arial', 15))
        self.campoPeca.place(x=300, y=200)
        
        
        self.botConfirmar = Button(self.frameLeft, text='Confirmar', width=10, font=('arial', 15), bg='orange', command=lambda:self.confirmarCampos())
        self.botConfirmar.place(x=360, y=350)
        
        #(Tela Operativa) - LABELS QUE IMPRIMEM O CRONÔMETRO - CRONÔMETRO

        self.seconds = Label(self.frameRight, text='00', font=('arial',30), fg=('red'), width=2)
        self.seconds.place(x=315, y=50)
        self.minutes = Label(self.frameRight, text='00', font=('arial',30), fg=('red'), width=2)
        self.minutes.place(x=260, y=50)
        self.hours = Label(self.frameRight, text='00', font=('arial',30), fg=('red'), width=2)
        self.hours.place(x=205, y=50)

        '''Chave de controle, respomsável de quando ser TRUE, informar que o botão INICIAR iniciou a contagem e em seguida
        destrui-lo fazendo o botão FINALIZAR 0S aparecer'''
        self.chaveControle = False

        '''Chave finalizar, responsável de quando TRUE, informar que o botão FINALIZAR OS foi acionado, e destrui-lo, mostrando um label que o OS foi finalizado.'''
        self.chaveFinalizar = False
        
        #variaveis que tornaram possiveis a contagem do cronômetro
        self.sec = None
        self.minu = None
        self.hou = None

        #Encerra a janela de operação na parte de label, Campos de entradas e de Frames, as demais serão chamadas através de funções
        self.janelaOper.mainloop()
        
    def confirmarCampos(self):
        if self.campoServico.get() == '' or self.campoPeca.get() == '':
            self.alerta = Tk()
            self.alerta.title('Alerta')
            self.alerta.iconbitmap('icone2.ico')
            self.alerta.resizable(False, False)
            self.alerta.configure(background='white')

            largura = 350
            altura = 150

            largura_screen = self.alerta.winfo_screenwidth()
            altura_screen = self.alerta.winfo_screenheight()

            posicaoX = largura_screen/2 - largura/2
            posicaoY = altura_screen/2 - altura/2

            self.alerta.geometry('%dx%d+%d+%d' % (largura, altura, posicaoX, posicaoY))

            labelAlert = Label(self.alerta, text='Verifique os Campos!', font=('arial', 15, 'bold'), fg='red', bg='white')
            labelAlert.place(x=75,y=20)

            botaoAlert = Button(self.alerta, text='OK', width=10, bg='red', fg='white', command = lambda: self.fechar())
            botaoAlert.place(x=130,y=90)
        
        else:
            self.botaoConfirmarOS()
            
        
        
    def botaoConfirmarOS(self):
        
        self.numOS = str(self.campoServico.get())
        peca = self.campoPeca.get()
        
        try:
            self.cursor.execute('use empresa_funcionarios')
            self.cursor.execute("select * from pecas_codigo where codigo = "+str(peca))
            valido = self.cursor.fetchall()
            if len(valido) == 1:
                
                self.mi = 0
                self.se = 0
                self.tempHora = str(valido[0][3])
                self.tempMin = str(valido[0][4])
                self.tempSeg = str(valido[0][5])
                
                if int(self.tempHora) == 0:
                    self.ho = 0
                    print(self.ho)
                    if int(self.tempMin) == 0:
                        self.mi = 0
                        self.se = 0
                        print(self.mi)
                    elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                        self.mi = int(self.tempMin) // 2
                        a = int(self.tempMin)/2
                        b = str(a)
                        c = int(b[-1])
                        d = (c*10) - 20
                        self.se = d
                        print(self.mi)
                        print(self.se)
                    elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                        self.mi = int(self.tempMin) // 2
                        self.se = 0
                        print(self.mi)
                        print(self.se)
                    elif int(self.tempMin) == 1:
                        self.mi = 0
                        self.se = (int(self.tempMin) * 60 ) // 2
                        print(self.mi)
                        print(self.se)
                
                elif int(self.tempHora) == 1:
                    self.ho = 0
                    print(self.ho)
                    if int(self.tempMin) == 0:
                        self.mi = (int(self.tempHora) * 60) // 2
                        self.se = 0
                        print(self.mi)
                        print(self.se)
                    elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                        self.mi = ((int(self.tempHora) * 60) // 2) + (int(self.tempMin) // 2)
                        a = int(self.tempMin)/2
                        b = str(a)
                        c = int(b[-1])
                        d = (c*10) - 20
                        self.se = d
                        print(self.mi)
                        print(self.se)
                    elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                        self.mi = ((int(self.tempHora) * 60) // 2) + (int(self.tempMin) // 2)
                        self.se = 0
                        print(self.mi)
                        print(self.se)
                    elif int(self.tempMin) == 1:
                        self.mi = (int(self.tempHora) * 60) // 2 
                        self.se = (int(self.tempMin) * 60) // 2
                        print(self.mi)
                        print(self.se)
                
                elif int(self.tempHora) > 1 and int(self.tempHora) % 2 == 0:
                    self.ho = int(self.tempHora) // 2
                    print(self.ho)
                    if int(self.tempMin) == 0:
                        self.mi = 0
                        self.se = 0
                        print(self.mi)
                        print(self.se)
                    elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                        self.mi = int(self.tempMin) // 2
                        a = int(self.tempMin)/2
                        b = str(a)
                        c = int(b[-1])
                        d = (c*10) - 20
                        self.se = d
                        print(self.mi)
                        print(self.se)
                    elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                        self.mi = int(self.tempMin) // 2
                        self.se = 0
                        print(self.mi)
                        print(self.se)
                    elif int(self.tempMin) == 1:
                        self.mi = 0
                        self.se = (int(self.tempMin) * 60) // 2
                        print(self.mi)
                        print(self.se)
                elif int(self.tempHora) > 1 and int(self.tempHora % 2 != 0):
                    self.ho = int(self.tempHora) // 2
                    print(self.ho)
                    a1 = int(self.tempHora)/2
                    b2 = str(a)
                    c3 = int(b[-1])
                    d4 = (c*10) - 20
                    
                    if int(self.tempMin) == 0:
                        self.mi = d4
                        self.se = 0
                        print(self.mi)
                        print(self.se)
                    elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                        self.mi = (d4) + (int(self.tempMin) // 2)
                        a = int(self.tempMin)/2
                        b = str(a)
                        c = int(b[-1])
                        d = (c*10) - 20
                        self.se = d
                        print(self.mi)
                        print(self.se)
                    elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                        self.mi = (d4) + (int(self.tempMin) // 2)
                        self.se = 0
                        print(self.mi)
                        print(self.se)
                    elif int(self.tempMin) == 1:
                        self.mi = d4
                        self.se = (int(self.tempMin) * 60) // 2        
                        print(self.mi)                

                self.tempProg = self.tempHora+':'+self.tempMin+':'+self.tempSeg
                self.codP = str(valido[0][2])
    
                self.tempoProgramado = Label(self.frameLeft, text='Tempo Programado:', font=('arial', 16, 'bold'), bg='#001333', fg='red')
                self.tempoProgramado.place(x=60, y=300)
                
                self.campoProgramado = Label(self.frameLeft, width=15, font=('arial', 15, 'bold'), bg='white')
                self.campoProgramado.place(x=300, y=300)
                
                self.campoProgramado['text'] = self.tempProg
                
                self.botConfirmar.destroy()
                
                self.campoServico = Label(self.frameLeft, text=self.campoServico.get(), width=25, font=('arial', 15), bg='white')
                self.campoServico.place(x=300, y=100)

                self.campoPeca = Label(self.frameLeft, text=self.campoPeca.get(), width=25, font=('arial', 15))
                self.campoPeca.place(x=300, y=200)
                
                self.botaoInciarContador = Button(self.frameRight, text='INICIAR', bg='green', fg='white',border=5, relief='ridge', font=('arial', 25, 'bold'), command = lambda:self.botao_iniciar())
                self.botaoInciarContador.place(x=205, y=200)
            
            else:
                self.alerta = Tk()
                self.alerta.title('Alerta')
                self.alerta.iconbitmap('icone2.ico')
                self.alerta.resizable(False, False)
                self.alerta.configure(background='white')

                largura = 350
                altura = 150

                largura_screen = self.alerta.winfo_screenwidth()
                altura_screen = self.alerta.winfo_screenheight()

                posicaoX = largura_screen/2 - largura/2
                posicaoY = altura_screen/2 - altura/2

                self.alerta.geometry('%dx%d+%d+%d' % (largura, altura, posicaoX, posicaoY))

                labelAlert = Label(self.alerta, text='Código não encontrado!', font=('arial', 15, 'bold'), fg='red', bg='white')
                labelAlert.place(x=65,y=20)

                botaoAlert = Button(self.alerta, text='OK', width=10, bg='red', fg='white', command = lambda: self.fechar())
                botaoAlert.place(x=130,y=90)
                    
        except:
            print('ERRO NO BANCO DE DADOS, CONFIRMAR OS')

    #(Tela Operativa) - FUNÇÃO 1º A SER INVOCADA POR BOTÃO: botaoInciarContador - TEMPORIZADOR----------------------------

    def botao_iniciar(self):

        if self.chaveControle == False:
            
            self.botFinalizar = Button(self.frameRight, text='FINALIZAR.OS', bg='red', fg='white',border=5, relief='ridge', font=('arial', 25, 'bold'), width=15, command = lambda: self.contagemFinalizada())
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
            
            self.frameTop['bg'] = 'green'
            self.frameLeft['bg'] = 'green'
            self.frameRight['bg'] = 'green'
            self.operadorNome['bg'] = 'green'
            self.operadorNomeUser['bg'] = 'green'
            self.horaInicialLb['bg'] = 'green'
            self.multimolde['bg'] = 'green'
            self.ordemServico['bg'] = 'green'
            self.codigoPeca['bg'] = 'green'
            self.tempoProgramado['bg'] = 'green'
            
            self.operadorNome['fg'] = 'red'
            self.operadorNomeUser['fg'] = 'red'
            self.horaInicialLb['fg'] = 'red'
            self.multimolde['fg'] = 'red'
            self.ordemServico['fg'] = 'red'
            self.codigoPeca['fg'] = 'red'
            self.tempoProgramado['fg'] = 'red' 
            
            self.chaveControle = True

        #Congfigurando os segundos do temporizador
        if self.sec == None:
            self.sec = 0
            self.secC = '00'
            self.minuC = '00'
            self.houC = '00'

        self.sec = self.sec + 1
        if self.sec > 0 and self.sec < 10:
            secA = self.sec / 100
            secB = str(secA)
            self.secC = secB[2:]
        else: 
            self.secC = str(self.sec)

        if self.sec > 59:
            self.sec = 0
            self.secC = '00'
            
            #Configurando o minuto do temporizador
            if self.minu == None:
                self.minu = 0
            self.minu = self.minu + 1
            if self.minu > 0 and self.minu < 10:
                minuA = self.minu / 100
                minuB = str(minuA)
                self.minuC = minuB[2:]
            else:
                self.minuC = str(self.minu)
            
            if self.minu > 59:
                self.minu = 0
                self.minuC = '00'
                
                #Congfigurando a hora do temporizador
                if self.hou == None:
                    self.hou = 0
                self.hou = self.hou + 1
                if self.hou > 0 and self.minu < 10:
                    houA = self.hou / 100
                    houB = str(houA)
                    self.houC = houB[2:]
                else:
                    houB = str(self.hou)

        h = int(self.houC)
        m = int(self.minuC)
        s = int(self.secC)
        
        if self.se == s and self.mi == m and h == self.ho:

            self.frameTop['bg'] = 'yellow'
            self.frameLeft['bg'] = 'yellow'
            self.frameRight['bg'] = 'yellow'
            self.operadorNome['bg'] = 'yellow'
            self.operadorNomeUser['bg'] = 'yellow'
            self.horaInicialLb['bg'] = 'yellow'
            self.multimolde['bg'] = 'yellow'
            self.ordemServico['bg'] = 'yellow'
            self.codigoPeca['bg'] = 'yellow'
            self.tempoProgramado['bg'] = 'yellow'
            
            self.operadorNome['fg'] = 'red'
            self.operadorNomeUser['fg'] = 'red'
            self.horaInicialLb['fg'] = 'red'
            self.multimolde['fg'] = 'red'
            self.ordemServico['fg'] = 'red'
            self.codigoPeca['fg'] = 'red'
            self.tempoProgramado['fg'] = 'red' 
        
        def telaVermelha2():
            self.frameTop['bg'] = 'red'
            self.frameLeft['bg'] = 'red'
            self.frameRight['bg'] = 'red'
            self.operadorNome['bg'] = 'red'
            self.operadorNomeUser['bg'] = 'red'
            self.horaInicialLb['bg'] = 'red'
            self.multimolde['bg'] = 'red'
            self.ordemServico['bg'] = 'red'
            self.codigoPeca['bg'] = 'red'
            self.tempoProgramado['bg'] = 'red'
            
            self.operadorNome['fg'] = 'white'
            self.operadorNomeUser['fg'] = 'white'
            self.horaInicialLb['fg'] = 'white'
            self.multimolde['fg'] = 'white'
            self.ordemServico['fg'] = 'white'
            self.codigoPeca['fg'] = 'white'
            self.tempoProgramado['fg'] = 'white'
            
            self.imgRelogio = PhotoImage(file="relogio.png")

            self.imagemTempRel = Label(self.frameRight, image=self.imgRelogio, bg='red')
            self.imagemTempRel.place(x=20,y=10)
            
        if int(self.tempHora) > 1:
            #para contagens a partir de uma hora
            if h == int(self.tempHora) and m + 5 == int(self.tempMin) and s == 0:
                telaVermelha2()
            elif h == int(self.tempHora) - 1 and 0 == int(self.tempMin) and m + 5 == 60  and s == 0:
                telaVermelha2()
        
        elif int(self.tempHora) == 1:
            
            if m + 5 == int(self.tempMin) and s == 0:
                telaVermelha2()
            elif int(self.tempMin) == 0 and m + 5 == 60  and s == 0:
                telaVermelha2()
                        
        elif int(self.tempHora) == 0:
    
            #print(self.tempHora, self.tempMin, self.tempSeg)
            if int(self.tempMin) <= 59 and int(self.tempMin) >= 10 and m + 5 == int(self.tempMin) and s == 0:
                telaVermelha2()
                
            #Falta configurar esta linha SABER O QUE FARÁ SE O TEMPO FOR >= A 5 E MENOR <= 10
            elif int(self.tempMin) <= 10 and int(self.tempMin) > 5 and m + 5 == int(self.tempMin) and s == 0:
                telaVermelha2()

            for c in range(1, 6):
                if int(self.tempMin) == c and m == 0 and s == 1:
                    telaVermelha2()

            #PROVISÓRIO ATÉ ACHAR OUTRA SOLUÇÃO MAIS CURTA =======================================================


        
        
        if int(self.tempHora) == 0:
            self.teste = 0
            for c in range(1, 6):
                
                if m + c == int(self.tempMin) and m == 0 and s == 1 and int(self.tempMin) <= 4:
                    self.mensag = Label(self.frameRight, text='Restaaaam '+str(c)+' Minutos!!', bg='red', fg='white', font=('arial', 15, 'bold'))
                    self.mensag.place(x=180, y=400)
                    print('parte 1')
                    print(c)
                    self.chaveMostrar = True
                elif m + c == int(self.tempMin) and m <= 4 and s == 1 and int(self.tempMin) <= 4 and self.chaveMostrar == True:
                    for i in range(1,6):
                        if i + m == int(self.tempMin):
                            self.mensag['text'] = 'Restaaaam '+str(i)+' Minutos!!'
                            print('FUNCIONOOUU 1')
                
                elif m + c == int(self.tempMin) and int(self.tempMin) - 5 == m and s == 1:
                    self.mensag2 = Label(self.frameRight, text='Restam kk Minutos!!', bg='red', fg='white', font=('arial', 15, 'bold'))
                    self.mensag2.place(x=180, y=400)
                    print('parte 2')
                    print(c)
                    self.chaveMostrar2 = True
                    
                elif m + c == int(self.tempMin) and m >= 0 and s == 1 and int(self.tempMin) >= 5 and self.chaveMostrar2 == True:
                    for i in range(1,6):
                        if i + m == int(self.tempMin):
                            self.mensag2['text'] = 'Restaaaam '+str(i)+' Minutos!!'
                            print('FUNCIONOOUU 1')
                
                if s == int(self.tempSeg) and m == int(self.tempMin) and h == int(self.tempHora) and self.chaveMostrar2 == True:
                    self.mensag2.destroy()
                    
                '''elif m + c == int(self.tempMin) and int(self.tempMin) - 5 > m and s == 1:
                    for i in range(1,6):
                        if i + m == int(self.tempMin):
                            self.mensag2['text'] = 'Restaaaam '+str(i)+' Minutos!!'
                            print('FUNCIONOOUU 2')
                            self.teste = 1'''
            #if self.teste == 1:
                #self.chaveMostrar2 = True
                    
        
        '''if self.chaveMostrar == True:
            for i in range(1,6):
                if i + m == int(self.tempMin):
                    self.mensag['text'] = 'Restaaaam '+str(i)+' Minutos!!
            print('FUNCIONOOUU 1')
        
        elif self.chaveMostrar2 == True:
            for i in range(1,6):
                if i + m == int(self.tempMin):
                    self.mensag2['text'] = 'Restaaaam '+str(i)+' Minutos!!'
                    chaveMostar2 = False
                    
            print('FUNCIONOOUU 2')'''
        
        
        
        if s == int(self.tempSeg) and m == int(self.tempMin) and h == int(self.tempHora):
            self.mensag.destroy()
            
            self.mensag2.destroy()
                
            self.imagemTempRel['bg'] = '#870000'
            self.imagemTempRel.destroy()
            self.frameTop['bg'] = '#870000'
            self.frameLeft['bg'] = '#870000'
            self.frameRight['bg'] = '#870000'
            self.operadorNome['bg'] = '#870000'
            self.operadorNomeUser['bg'] = '#870000'
            self.horaInicialLb['bg'] = '#870000'
            self.multimolde['bg'] = '#870000'
            self.ordemServico['bg'] = '#870000'
            self.codigoPeca['bg'] = '#870000'
            self.tempoProgramado['bg'] = '#870000'
            
            self.operadorNome['fg'] = 'white'
            self.operadorNomeUser['fg'] = 'white'
            self.horaInicialLb['fg'] = 'white'
            self.multimolde['fg'] = 'white'
            self.ordemServico['fg'] = 'white'
            self.codigoPeca['fg'] = 'white'
            self.tempoProgramado['fg'] = 'white'            
            
            self.botFinalizar.destroy()
            self.sair.destroy()
            
            self.labFinalizar = Label(self.frameRight, text='Tempo excedido!!',  bg='#870000', fg='white', font=('arial', 25, 'bold'))
            self.labFinalizar.place(x=150, y=150)
            
            self.botaoReabilitar = Button(self.frameRight, text='REABILITAR', bg='orange', fg='white',border=5, relief='ridge', font=('arial', 25, 'bold'), command = lambda: self.tela_admin(2))
            self.botaoReabilitar.place(x=170, y=220)
            
            self.chaveFinalizar = True
        
        
        self.seconds['text'] = self.secC
        self.minutes['text'] = self.minuC
        self.hours['text'] = self.houC


        if self.chaveFinalizar == False:
            self.seconds.after(1000, self.botao_iniciar)

#------------------------------- (Tela Operativa) - FUNÇÃO xº A SER INVOCADA POR: botReinciar -----------------            
    def contagemFinalizada(self):
        '''Função rensponsável por finalizar a contagem, informando
        que o tempo foi atingido dentro do limite.'''
            
        self.chaveFinalizar = True
        
        #Se o cahveFinalizar foir verdadeira, o crobômetro para a contagem
        if self.chaveFinalizar == True:
            self.botFinalizar.destroy()
            self.labFinalizar =  Label(self.frameRight, text='Processesso Finalizado!',  bg='red', fg='white', font=('arial', 25, 'bold'))
            self.labFinalizar.place(x=100, y=150)
            
            #Pegando a hora atual em que o processo foi finalizado
            time = datetime.now().time()
            
            #Utilizando formula para não pegar os milisegundos
            lista = [str(time)]
            recebe = ''
            for c in lista:
                for i in c:
                    if i == '.':
                        break
                    else:
                        recebe += i
            horaFinal = recebe
            
            #Tempo formatado para enviar ao banco
            self.tempGasto = self.houC+':'+self.minuC+':'+self.secC
            
            #Botão caso o operado queira realizar outra S.O
            self.botReiniciar = Button(self.frameRight, text='NOVO.OS', bg='green', fg='white',border=5, relief='ridge', font=('arial', 20, 'bold'), width=15, command = lambda: self.nova_tela_operacao())
            self.botReiniciar.place(x=150, y=230)
            
            #Enviando todos os dados ao banco
            try:
                self.cursor.execute('use empresa_funcionarios')
                self.cursor.execute("insert into monitoria_funcionarios VALUES('id','"+str(self.operador)+"','"+str(self.horaLogin)+"','"+str(self.horaInicial)+"','"+str(horaFinal)+"','"+self.tempGasto+"','"+str(self.tempProg)+"','"+self.codP+"','"+self.numOS+"','invalido','invalido')")
                self.banco.commit()
            #Excessão caso ocorra de não conseguir salvar
            except:
                print('erro ao salvar informações da Tela de Operação')

    #------------------------------- (Tela Operativa) - FUNÇÃO xº A SER INVOCADA POR: botReinciar -----------------
    def nova_tela_operacao(self):
        '''Função responsável por apertar o botão "NOVO.OS" após finalizar a 
        operação, caso o operador deseje executar uma nova tarefa'''
        
        self.janelaOper.destroy()
        self.tela_de_operacao()
        
    #------------------------------- (Tela Operativa) - FUNÇÃO 9º A SER INVOCADA POR: sair -----------------    
    def sairTela(self):
        '''Função responsavel por ao apertar o botão "Sair" no lado superior
        direito o cronômetro estiver em contagem, abrirá automaticamente um 
        alerta informando que o programa ainda está sendo executado, e só 
        permitira sair ao encerrar a operação, '''
            
        #Se a chave for True significa que a operação foi finalizada
        if self.chaveFinalizar ==  True:
            self.janelaOper.destroy()
            self.__init__()
        
        #Se a chaveContre for False significa que a operação foi finalizada
        elif self.chaveControle == False:
            self.janelaOper.destroy()
            self.__init__()
        
        #Senão significa que o cronômetro ainda está em execução
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

instancia = LoginAdmnistracao()
