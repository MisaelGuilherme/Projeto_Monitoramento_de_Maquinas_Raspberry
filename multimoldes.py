#Pogramador: Misael Jesus
#Date: 18/08/2020

from datetime import *
from tkinter import *
from time import sleep
from tkinter import messagebox
import mysql.connector

class LoginAdmnistracao:
    
    #------------------------------- (Centralizando Janelas) - FUNÇÃO REUTILIZÁVEL --------------------------
    def centraliza_tela(self, larg, alt, jane):
                
        # Dimensões da Janela
        largura = larg
        altura = alt
        
        # Resolução do Sistema
        largura_screen = jane.winfo_screenwidth()
        altura_screen = jane.winfo_screenheight()
        
        # Definição da Janela
        posicaoX = largura_screen / 2 - largura / 2
        posicaoY = altura_screen / 2 - altura / 2
        
        # Posicão da Tela 
        return jane.geometry('%dx%d+%d+%d' % (largura, altura, posicaoX, posicaoY))

    #------------------------------- (Criando Janelas-Alerta-Servidor) - FUNÇÃO REUTILIZÁVEL -----------------
    
    def alerta_erro_servidor(self, parte):
        
        self.alerta = Tk()
        self.alerta.title('Alerta')
        self.alerta.iconbitmap('img/icone2.ico')
        self.alerta.resizable(False, False)
        self.alerta.configure(background='#ff2e2e')

        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(350, 150, self.alerta)

        labelAlert = Label(self.alerta, text=parte, font=('arial', 12, 'bold'), fg='white', bg='#ff2e2e')
        labelAlert.place(x=13,y=20)

        botaoAlert = Button(self.alerta, text='OK', width=10, bg='red', fg='white', command = lambda: self.fechar())
        botaoAlert.place(x=140,y=80)
        botaoAlert.focus_force()
        botaoAlert.bind("<Return>", self.fechar(self.fechar))
        self.alerta.mainloop()

    #FUNCÃO PARA DESTRUIR TODOS OS ALERTAS
    def fechar(self):
        self.alerta.destroy()
                
    #------------------------------- (Criando Alerta-Mensagens) - FUNÇÃO REUTILIZÁVEL ------------------------
    
    def alerta_mensagem(self, text, tam, ladX, ladY):
        
        alertaMensage = Tk()
        alertaMensage.title('Alerta')
        alertaMensage.iconbitmap('img/icone2.ico')
        alertaMensage.resizable(False, False)
        alertaMensage.configure(background='white')

        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(350, 150, alertaMensage)
        
        def fechar_alerta_Mensage(event):
            alertaMensage.destroy()        

        labelAlert = Label(alertaMensage, text=text, font=('arial', tam, 'bold'), fg='red', bg='white')
        labelAlert.place(x=ladX, y=ladY)

        botaoAlert = Button(alertaMensage, text='OK', width=10, bg='red', fg='white', command = lambda: fechar_alerta_Mensage(fechar_alerta_Mensage))
        botaoAlert.place(x=135,y=90)
        botaoAlert.focus_force()
        botaoAlert.bind("<Return>", fechar_alerta_Mensage)
        
        alertaMensage.mainloop()         
        
    #------------------------------- (Senha Administração) - FUNÇÃO REUTILIZÁVEL ----------------------------
    def tela_admin(self, botao):
        
        self.janelaADM = Toplevel()
        self.janelaADM.title('Login Administração')
        self.janelaADM.iconbitmap('img/icone2.ico')
        self.janelaADM.resizable(False, False)
        self.janelaADM.configure(background='white')
        
        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(500, 500, self.janelaADM)
        
        #Adcionando Logo na Janela ADM
        imgAdm = PhotoImage(file="img/icone1.png")

        imagemPricipalAdm = Label(self.janelaADM, image=imgAdm, bg='white')
        imagemPricipalAdm.place(x=170,y=10)

        admLabelPrincipal = Label(self.janelaADM, text='Senha Admin', fg='#3e8e94', font=('arial', 12, 'bold'), bg='white')
        admLabelPrincipal.place(x=40,y=210)

        self.valorBotao = botao

        self.admSenhaPrincipal = Entry(self.janelaADM, width=30, border=2, show='*')
        self.admSenhaPrincipal.place(x=160,y=210)
        self.admSenhaPrincipal.focus_force()
        self.admSenhaPrincipal.bind("<Return>", self.transicao)
        
        admBotaoPrincipal = Button(self.janelaADM, text='Continuar', bg='#3e8e94', fg='white', border=0, font=('arial', 12), width=10, command = lambda: self.verificar_adm(botao, self.admSenhaPrincipal.get()))
        admBotaoPrincipal.place(x=210,y=300)
        admBotaoPrincipal.bind("<Return>", self.transicao)

        self.janelaADM.mainloop()        
    
    def transicao(self, event):
        
        a = self.valorBotao
        b = self.admSenhaPrincipal.get()
        
        self.verificar_adm(a, b)
    
    def verificar_adm(self, contV, senha):
        
        if str(senha).isnumeric():
            
            # Se a senha for numérica irá verificar no banco de dados
            try:
                banco = mysql.connector.connect(
                    host = '10.0.0.65',
                    user = 'multimoldesClient',
                    password = 'multimoldes'
                )
                cursor = banco.cursor()
                cursor.execute('use empresa_funcionarios')
                cursor.execute('select * from supervisor_admin where senha ='+str(senha))
                valido = cursor.fetchall()     
                
                #Se (valido) == 1 significa que encontrou resultado
                if len(valido) == 1:
                    
                    senhaAdm = valido[0][0]
                    
                    # Confirmando se senha for verdadeira, se (contV) for igual a 1, abrir tela de cadastro
                    if senhaAdm == str(senha) and contV == 1:
                        self.janelaADM.destroy()
                        self.tela_cadastrar()
                    
                    # Confirmando se senha for verdadeira, se (contV) for igual a 2, abrir tela de tempo extra
                    elif senhaAdm == str(senha) and contV == 2:
                        self.janelaADM.destroy()
                        self.tempo_extra()      

                else:
                    self.labelErro2 = Label(self.janelaADM, text='Senha Incorreta. Tente Novamente!', bg='white', fg='#bf0606')
                    self.labelErro2.place(x=157, y=233)
                                                    
            except:
                self.alerta_erro_servidor('01-Error-Servidor: Não acesso ao servidor')
                
        elif senha == '':
            self.labelErro1 = Label(self.janelaADM, text='Preencha o campo!', bg='white', fg='#bf0606', width=26)
            self.labelErro1.place(x=160, y=233)
        else:
            self.labelErro2 = Label(self.janelaADM, text='Senha Incorreta. Tente Novamente!', bg='white', fg='#bf0606')
            self.labelErro2.place(x=157, y=233)
        

    #------------------------------- (Login Funcionário) - FUNÇÃO 1º A SER INICIADA --------------------------                
    def __init__(self):
        
        self.janelaFuncio = Tk()
        self.janelaFuncio.title('Login Funcionário')
        self.janelaFuncio.iconbitmap('img/icone2.ico')
        self.janelaFuncio.configure(background='white')
        self.janelaFuncio.resizable(False, False)
        
        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(500, 500, self.janelaFuncio)
        
        #Adcionando Logo na Janela de Funcionário
        self.imgFun = PhotoImage(file="img/trabalho1.png")

        self.imagemPricipalFun = Label(self.janelaFuncio, image=self.imgFun, bg='white')
        self.imagemPricipalFun.place(x=200,y=15)

        self.labelLogin = Label(self.janelaFuncio, text='Usuário', bg='white', fg='#3e8e94', font=('arial',11,'bold'))
        self.labelLogin.place(x=80, y=200)

        self.campoLogin = Entry(self.janelaFuncio, width=30)
        self.campoLogin.place(x=150, y=200)
        self.campoLogin.focus_force()
        self.campoLogin.bind("<Return>", self.confirmar_tela_funcionario)

        self.labelSenha = Label(self.janelaFuncio, text='Senha', bg='white', fg='#3e8e94', font=('arial',11,'bold'))
        self.labelSenha.place(x=80, y=250)

        self.campoSenha = Entry(self.janelaFuncio, width=30, show='*')
        self.campoSenha.place(x=150, y=250)
        self.campoSenha.bind("<Return>", self.confirmar_tela_funcionario)

        self.botao = Button(self.janelaFuncio, text='Confirmar', fg='white', bg='#3e8e94', border=0, font=('arial', 10, 'bold'), width=10, command = lambda: self.confirmar_tela_funcionario(self.confirmar_tela_funcionario))
        self.botao.place(x=200, y=300)
        self.botao.bind("<Return>", self.confirmar_tela_funcionario)

        self.lbCadastrar = Label(self.janelaFuncio, text='Cadastrar Funcionário', bg='white', fg='#3e8e94',font=('arial',10,'bold'))
        self.lbCadastrar.place(x=340, y=410)
        
        self.botCadastrar = Button(self.janelaFuncio, text='Cadastrar',fg='white', bg='#3e8e94', border=0, font=('arial', 10, 'bold'), width=10, command = lambda: self.tela_admin(1))
        self.botCadastrar.place(x=370, y=440)
        
        self.janelaFuncio.mainloop()
        
    #------------------------------- (Janela de Tempo Extra) - FUNÇÃO 2--------------------------
    def tempo_extra(self):
        
        self.janelaTempExtra = Tk()
        self.janelaTempExtra.title('Tela Operativa')
        self.janelaTempExtra.iconbitmap('img/icone2.ico')
        self.janelaTempExtra.configure(background='#870000')
        self.janelaTempExtra.geometry('550x350+200+100')

        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(550, 350, self.janelaTempExtra)
        
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
        
        bc = Button(self.janelaTempExtra, text='Confirmar', font=('arial',15,'bold'), bg='orange', fg='white', command = self.verificar_tempo_extra)
        bc.place(x=225,y=260)
        
        self.janelaTempExtra.mainloop()

    #------------------------------- (Janela de Verificação de Tempo Extra) - FUNÇÃO 3 --------------------------
    def verificar_tempo_extra(self):
        
        if self.ll.get() == '' or self.mm.get() == '':
            
            messagebox.showwarning('Alerta', 'Verifique os Campos.')
        
        elif str(self.ll.get()).isnumeric() == False or str(self.mm.get()).isnumeric() == False:
            
            messagebox.showwarning('Alerta', 'Verifique os Campos.')

        elif int(self.mm.get()) < 5 or int(self.ll.get()) < 0:
            
            messagebox.showwarning('Alerta', 'Valor Min: 0 Horas\nValor Min: 5 Minutos')
            
        elif int(self.mm.get()) > 59 or int(self.ll.get()) > 24:
            
            messagebox.showwarning('Alerta', 'Valor Max: 24 Horas\nValor Max: 59 Minutos')
        
        else:
            self.configurar_tempo_extra()

    #Transformando a hora, minuto e segundo em decimal para exibir no label o tempo extra
    def transformar_tempo_decimal(self, thora, tminu, tsegu):
        if int(thora) > 0 and int(thora) < 10:
            A = int(thora) / 100
            B = str(A)
            final1 = B[2:]
        elif int(thora) == 0:
            final1 = '00'
        else: 
            final1 = str(thora)
            
        if int(tminu) > 0 and int(tminu) < 10:
            A = int(tminu) / 100
            B = str(A)
            final2 = B[2:]
        elif int(tminu) == 0:
            final2 = '00'
        else: 
            final2 = str(tminu)
            
        if int(tsegu) > 0 and int(tsegu) < 10:
            A = int(tsegu) / 100
            B = str(A)
            final3 = B[2:]
        elif int(tsegu) == 0:
            final3 = '00'
        else: 
            final3 = str(tsegu)
        
        return final1+':'+final2+':'+final3
    
    def configurar_tempo_extra(self):
        ll = self.ll.get()
        mm = self.mm.get()
        
        self.janelaTempExtra.destroy()
        
        #Configurando tempo Extra gasto caso o operador precise de mais tempo mais de uma vez
        self.chaveTempExtra += 1
        
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
        elif int(self.tempHora) > 1 and int(self.tempHora) % 2 != 0:
            self.ho = int(self.tempHora) // 2
            print(self.ho)
            a1 = int(self.tempHora)/2
            b2 = str(a1)
            c3 = int(b2[-1])
            d4 = (c3*10) - 20
            
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
        
        #Armazenando na variável já formatado
        self.tempProgExt = self.transformar_tempo_decimal(self.tempHora, self.tempMin, self.tempSeg)
        
        #Exibindo no label o horário adcionado após o tempo ser esgotado
        self.campoProExt = Label(self.frameLeft, text=self.tempProgExt, width=15, font=('arial', 15, 'bold'), bg='white', fg='red')
        self.campoProExt.place(x=300, y=400)
        
        #Invocando o botão sair(login) após o horário ser adcionado
        self.sair = Button(self.frameTop, text='Sair', font=('arial',14,'bold'), fg='white', bg='red', activebackground='red', activeforeground='white', border=1, width=5, command=lambda:self.sairTela())
        self.sair.place(x=1180,y=20)
        
        #Botão inciar a contagem do cronômetro
        self.botaoInciarContador = Button(self.frameRight, text='INICIAR', bg='#035700', fg='white', activebackground='#035700', activeforeground='white', border=5, relief='ridge', font=('arial', 25, 'bold'), command = lambda:self.botao_iniciar())
        self.botaoInciarContador.place(x=205, y=200)
            
            
    #------------------------------- (Tela Cadastrar) - FUNÇÃO 4º A SER INVOCADA POR FUNÇÃO: verificar_adm() ------------------

    def tela_cadastrar(self):
        
        self.janelaCad = Toplevel()
        self.janelaCad.title('Cadastro')
        self.janelaCad.iconbitmap('img/icone2.ico')
        self.janelaCad.resizable(False, False)
        self.janelaCad.configure(background='white')

        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(500, 500, self.janelaCad)

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
        
        #CASO O CAMPO "NOME" MAIOR QUE 50 CARACTERES
        elif len(str(self.campNome.get())) > 50:
            self.error = Label(self.janelaCad, text='Valor máximo 50 caracteres', fg='red', bg='white')
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
            host="10.0.0.65",
            user="multimoldesClient",
            password="multimoldes")
            
            cursor = banco.cursor()
            cursor.execute('USE empresa_funcionarios')
            cursor.execute('select * from funcionarios where cpf = '+str(cpf))
            valido = cursor.fetchall()
            
            #VERIFICANDO SE O CPF DO FUNCIONÁRIO JÁ ESTÁ CADASTRADO
            if len(valido) == 1:
                
                #SE O CPF JÁ FOI CADASTRO APARECERÁ UM ALERTA
                #self.alerta_mensagem('CPF já Cadastrado!', 10, 65, 20)
                messagebox.showerror('Alerta','CPF já Cadastrado!')
            
            #CADASTRANDO ENVIANDO DADOS DO FUNCIONÁRIO PRO BANCO DE DADOS
            else:
                    
                cursor.execute("INSERT INTO funcionarios VALUES(id,'"+nome+"','"+cpf+"','"+senha+"')")
                banco.commit()
                comando = 1
                
                self.janelaCad.destroy()    
                
                messagebox.showinfo('Alerta','Funcionário Cadastrado!')
        
        #CASO O A LIGAÇÃO OU AS CONDIÇÕES NÃO TENHAM SIDO EXECUTADAS COM ÊXITOS
        except:
            self.alerta_erro_servidor('02-Error-Servidor: Não acesso ao servidor')
        
    #------------------------------- (Banco de Dados) - FUNÇÃO 7º A SER INVOCADA POR: botao ------------------------------- 
    def confirmar_tela_funcionario(self, event):
        
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
                        host = "10.0.0.65",
                        user = "multimoldesClient",
                        password = "multimoldes")
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
                        messagebox.showerror('Alerta','Login não Existe!')
                        
                #mensaem de erro caso ocorra alguma excessão ao tentar logar
                except:
                    self.alerta_erro_servidor('03-Error-Servidor: Não acesso ao servidor')
            
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
        self.janelaOper.iconbitmap('img/icone2.ico')
        self.janelaOper.configure(background='black')
        self.janelaOper.geometry('500x500+200+100')
        self.janelaOper.state('zoomed')

        #(Tela Operativa) - FRAMES DA TELA DE OPERAÇÃO

        self.frameTop = Frame(self.janelaOper, width=1400, height=130, bg='#001333',highlightthickness=3,highlightcolor='black')
        self.frameTop.config(highlightbackground='black')
        self.frameTop.pack(side=TOP)

        self.frameLeft = Frame(self.janelaOper, width=800, bg='#001333', height=570,highlightthickness=3,highlightcolor='black')
        self.frameLeft.config(highlightbackground='black')
        self.frameLeft.pack(side=LEFT)

        self.frameRight = Frame(self.janelaOper, width=550, height=570, bg='#001333',highlightthickness=3,highlightcolor='black') ##c4c0c0
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
        
        self.sair = Button(self.frameTop, text='Sair', font=('arial',14,'bold'), fg='white', bg='red', activebackground='red', activeforeground='white', border=1, width=5, command=lambda:self.sairTela())
        self.sair.place(x=1180,y=20)
        
        #(Tela Operativa) - LABELS E CAMPOS DE ENTRADA DA TELA DE OPERAÇÃO - FOMULÁRIO

        self.ordemServico = Label(self.frameLeft, text='Ordem de Serviço:', font=('arial', 16, 'bold'), bg='#001333', fg='red')
        self.ordemServico.place(x=70, y=100)
        self.campoServico = Entry(self.frameLeft, width=25, font=('arial', 15), bg='white')
        self.campoServico.place(x=300, y=100)
        self.campoServico.focus_force()
        self.campoServico.bind("<Return>", self.confirmarCampos)
        
        self.codigoPeca = Label(self.frameLeft, text='Código da Peça:', font=('arial', 16, 'bold'), bg='#001333', fg='red')
        self.codigoPeca.place(x=90, y=200)
        self.campoPeca = Entry(self.frameLeft, width=25, font=('arial', 15))
        self.campoPeca.place(x=300, y=200)
        self.campoPeca.bind("<Return>", self.confirmarCampos)
        
        def ok():

            if self.os1.get() == 1 or self.os2.get() == 1:
                if self.os1.get() == 0:
                    self.novoOS['state'] = DISABLED
                else:
                    self.tipo = 'Nova OS'
                    self.novoOS['selectcolor'] = 'green'
                    self.novoOS.bind("<Return>", self.confirmarCampos)
                
                if self.os2.get() == 0:
                    self.retrabalhoOS['state'] = DISABLED
                else:
                    self.tipo = 'Retrabalhar OS'
                    self.retrabalhoOS['selectcolor'] = 'green'
                    self.retrabalhoOS.bind("<Return>", self.confirmarCampos)
            else:
                self.novoOS['state'] = ACTIVE
                self.retrabalhoOS['state'] = ACTIVE
                self.novoOS['selectcolor'] = '#001333'
                self.retrabalhoOS['selectcolor'] = '#001333'
                self.tipo = ''

        self.os1 = IntVar()
        self.novoOS = Checkbutton(self.frameLeft, text='Nova OS', font=('arial',10,'bold'), bg='#001333', fg='white', activebackground='#001333', activeforeground='white', variable = self.os1, command=lambda:ok())
        self.novoOS.place(x=320, y=250)
        
        self.os2 = IntVar()
        self.retrabalhoOS = Checkbutton(self.frameLeft, text='Retrabalhar OS', font=('arial',10,'bold'),bg='#001333', fg='white', activebackground='#001333', activeforeground='white', variable = self.os2, command=lambda:ok())
        self.retrabalhoOS.place(x=450, y=250)
        
        self.botConfirmar = Button(self.frameLeft, text='Confirmar', fg='white', activebackground='orange', activeforeground='white', border=0, width=10, font=('arial', 15,'bold'), bg='orange', command=lambda:self.confirmarCampos(self.confirmarCampos))
        self.botConfirmar.place(x=370, y=350)
        self.botConfirmar.bind("<Return>", self.confirmarCampos)
        
        #(Tela Operativa) - LABELS QUE IMPRIMEM O CRONÔMETRO - CRONÔMETRO

        self.seconds = Label(self.frameRight, text='00', font=('arial',30), fg=('red'), width=2)
        self.seconds.place(x=315, y=50)
        self.minutes = Label(self.frameRight, text='00', font=('arial',30), fg=('red'), width=2)
        self.minutes.place(x=260, y=50)
        self.hours = Label(self.frameRight, text='00', font=('arial',30), fg=('red'), width=2)
        self.hours.place(x=205, y=50)

        '''Chave de controle, responsável de quando ser TRUE, informar que o botão INICIAR iniciou a contagem e em seguida
        destrui-lo fazendo o botão FINALIZAR 0S aparecer'''
        self.chaveControle = False

        '''Chave finalizar, responsável de quando TRUE, informar que o botão FINALIZAR OS foi acionado, e destrui-lo, mostrando um label que o OS foi finalizado.'''
        self.chaveFinalizar = False
        
        '''tempoEsgotado, responsável de quando a janela de pause estiver abertar e o tempo esgotar, não poderá mais pausar'''
        self.tempoEsgotado = False
        self.resultPausa = ''
        
        #variaveis que tornaram possiveis a contagem do cronômetro
        self.sec = None
        self.minu = None
        self.hou = None     
        
        self.secOperacao = None
        self.minuOperacao = None
        self.houOperacao = None        
        
        self.chaveFinalizar2 = False
        self.chaveControle2 = False
        
        self.janelaOper.mainloop()
        
    def confirmarCampos(self, event):
        if self.campoServico.get() == '' or self.campoPeca.get() == '':
            
            self.alerta_mensagem('Verifique os Campos!', 15, 75, 20)
        
        elif self.os1.get() == 0 and self.os2.get() == 0:
            
            self.alerta_mensagem('Marque uma Opção!', 15, 75, 20)
            
        else:
            self.botaoConfirmarOS()
            
        
    def botaoConfirmarOS(self):
        if self.os1.get() == 1:
            self.novoOS['state'] = DISABLED

        else:
            self.retrabalhoOS['state'] = DISABLED
        
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
                
                #Variáveis responsáveis caso o "tempo gasto" ultrapasse o "tempo programado"
                self.chaveTempExtra = 0
                self.tempExtraGastoA = 0
                self.tempExtraGastoB = 0
                self.tempExtraGastoC = 0
                self.backup = str(self.tempHora)+':'+str(self.tempMin)+':'+str(self.tempSeg)
                
                #Formatando as varíaveis para encaixar no label - Tempo Programado
                self.tempProg = self.tempHora+':'+self.tempMin+':'+self.tempSeg
                self.codP = str(valido[0][2])

                #Mostrando o tempo Programado através do label
                self.tempoProgramado = Label(self.frameLeft, text='Tempo Programado:', font=('arial', 16, 'bold'), bg='#001333', fg='red')
                self.tempoProgramado.place(x=60, y=300)
                
                self.campoProgramado = Label(self.frameLeft, width=15, font=('arial', 15, 'bold'), bg='white')
                self.campoProgramado.place(x=300, y=300)
                
                self.campoProgramado['text'] = self.tempProg
                
                self.botConfirmar.destroy()
                
                #Mudando os campos Entry para Labels para exibir na tela
                self.campoServico = Label(self.frameLeft, text=self.campoServico.get(), width=25, font=('arial', 15), bg='white')
                self.campoServico.place(x=300, y=100)

                self.campoPeca = Label(self.frameLeft, text=self.campoPeca.get(), width=25, font=('arial', 15))
                self.campoPeca.place(x=300, y=200)
                
                #Labals que imprimem o cronômetro que totaliza o tempo de operação do funcionário
                self.segundos = Label(self.frameLeft, text='00', font=('arial',12,'bold'), width=2, fg='#023300')
                self.segundos.place(x=167, y=450)
                self.minutos = Label(self.frameLeft, text='00', font=('arial',12,'bold'), width=2, fg='#023300')
                self.minutos.place(x=140, y=450)
                self.horas = Label(self.frameLeft, text='00', font=('arial',12,'bold'), width=2, fg='#023300')
                self.horas.place(x=113, y=450)
                
                self.tempOperando = '00:00:00'
                
                self.botaoInciarContador = Button(self.frameRight, text='INICIAR', bg='#035700', fg='white', activebackground='#035700', activeforeground='white', border=5, relief='ridge', font=('arial', 25, 'bold'), command = lambda:self.botao_iniciar())
                self.botaoInciarContador.place(x=205, y=200)
            
            else:

                #Caso o código não exista no banco de dados
                self.alerta_mensagem('Código não Encontrado!', 15, 65, 20)
                    
        except:
            self.alerta_erro_servidor('04-Error-Servidor: Não acesso ao servidor')            

    #(Tela Operativa) - FUNÇÃO 1º A SER INVOCADA POR BOTÃO: botaoInciarContador - TEMPORIZADOR----------------------------
    def objetos_cores(self, cor1, cor2):
        
        self.frameTop['bg'] = cor1
        self.frameLeft['bg'] = cor1
        self.frameRight['bg'] = cor1
        self.operadorNome['bg'] = cor1
        self.operadorNomeUser['bg'] = cor1
        self.horaInicialLb['bg'] = cor1
        self.multimolde['bg'] = cor1
        self.ordemServico['bg'] = cor1
        self.codigoPeca['bg'] = cor1
        self.tempoProgramado['bg'] = cor1
        
        self.novoOS['bg'] = cor1
        self.retrabalhoOS['bg'] = cor1
        
        self.operadorNome['fg'] = cor2
        self.operadorNomeUser['fg'] = cor2
        self.horaInicialLb['fg'] = cor2
        self.multimolde['fg'] = cor2
        self.ordemServico['fg'] = cor2
        self.codigoPeca['fg'] = cor2
        self.tempoProgramado['fg'] = cor2
                
    def botao_iniciar(self):
        
        if self.chaveControle2 == True:
            self.iniciarContOper()
                    
        if self.chaveControle == False:
            
            self.botFinalizar = Button(self.frameRight, text='FINALIZAR.OS', bg='red', fg='white',border=5, relief='ridge', font=('arial', 22, 'bold'), width=15, command = lambda: self.contagemFinalizada())
            self.botFinalizar.place(x=140, y=160)
            
            self.botPausar = Button(self.frameRight, text='PAUSAR.OS', bg='#035700', fg='white',border=5, relief='ridge', font=('arial', 22, 'bold'), width=15, command = lambda: self.tentativa_pausar())
            self.botPausar.place(x=140, y=260)            
            
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
            
            self.objetos_cores('green', 'red')
            
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
                if self.hou > 0 and self.hou < 10:
                    houA = self.hou / 100
                    houB = str(houA)
                    self.houC = houB[2:]
                else:
                    houB = str(self.hou)

        h = int(self.houC)
        m = int(self.minuC)
        s = int(self.secC)
        
        if self.se == s and self.mi == m and h == self.ho:
            if int(self.tempMin) > 10 or int(self.tempHora) >= 1:
                
                self.objetos_cores('yellow', 'red')
        
        def telaVermelha2():
            
            self.objetos_cores('red', 'white')
            print('vezes')
            self.imgRelogio = PhotoImage(file="img/relogio.png")

            self.imagemTempRel = Label(self.frameRight, image=self.imgRelogio, bg='red')
            self.imagemTempRel.place(x=20,y=5)
        
        self.ativ = 0     
        if int(self.tempHora) > 1:
            #para contagens a partir de uma hora
            for c in range(1, 6):
                if m + c == int(self.tempMin) and m == 0 and h == int(self.tempHora) and s == 0 and int(self.tempMin) <= 5:
                    print('Parte 1 A')
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Restam '+str(c)+' Minutos!!', bg='red', fg='white', font=('arial', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                
                elif m + c == int(self.tempMin) and h == int(self.tempHora) and int(self.tempMin) <= 5:
                    
                    for i in range(1, 6):
                        if i + m == int(self.tempMin):
                            self.mensag['text'] = 'Restam '+str(i)+' Minutos!!'       

                if m + c == int(self.tempMin) and c == 5 and h == int(self.tempHora) and s == 0 and int(self.tempMin) >= 6 and int(self.tempMin) <= 59:
                    print('Parte 2 A')
                    telaVermelha2()
                    self.mensag2 = Label(self.frameRight, text='Restam '+str(c)+' Minutos!!', bg='red', fg='white', font=('arial', 20, 'bold'))
                    self.mensag2.place(x=160, y=400)
                    self.ativ = 1
                
                elif m + c == int(self.tempMin) and h == int(self.tempHora) and int(self.tempMin) >= 6 and int(self.tempMin) <= 59:
                    
                    for i in range(0,6):
                        if i + m == int(self.tempMin):
                            self.mensag2['text'] = 'Restam '+str(i)+' Minutos!!'                                                 
                
                #PRECISA DAR A CONDIÇÃO PARA ESTE CASO AINDA
                if c == 5 and h == int(self.tempHora) - 1 and int(self.tempMin) == 0 and m + 5 == 60  and s == 0:
                    print('Parte 3 A')
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Restam '+str(c)+' Minutos!!', bg='red', fg='white', font=('arial', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1                  
                
                elif h == int(self.tempHora) - 1 and int(self.tempMin) == 0 and m + c == 60:
                    for i in range(1, 6):
                        if i + m == 60:
                            self.mensag['text'] = 'Restam '+str(i)+' Minutos!!'
                    
        elif int(self.tempHora) == 1:
            for c in range(1, 6):
                
                if c == 5 and int(self.tempMin) == 0 and m + 5 == 60 and s == 0:
                    print('Parte 1 B')
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Restam '+str(c)+' Minutos!!', bg='red', fg='white', font=('arial', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                    
                elif int(self.tempMin) == 0 and m + c == 60:
                    for i in range(1,6):
                        if i + m == 60:
                            self.mensag['text'] = 'Restam '+str(i)+' Minutos!!'
                
                if h == int(self.tempHora) and m + c == int(self.tempMin) and m == 0 and s == 1 and int(self.tempMin) <= 5:
                    print('Parte 2 B')
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Restam '+str(c)+' Minutos!!', bg='red', fg='white', font=('arial', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                    
                elif h == int(self.tempHora) and m + c == int(self.tempMin) and int(self.tempMin) <= 5 and int(self.tempMin) >= 1:
                    
                    for i in range(1,6):
                        if i + m == int(self.tempMin):
                            self.mensag['text'] = 'Restam '+str(i)+' Minutos!!'

                if h == int(self.tempHora) and c == 5 and m + c == int(self.tempMin) and s == 0 and int(self.tempMin) >=6 and int(self.tempMin) <= 59:
                    print('Parte 3 B')
                    telaVermelha2()
                    self.mensag2 = Label(self.frameRight, text='Restam '+str(c)+' Minutos!!', bg='red', fg='white', font=('arial', 20, 'bold'))
                    self.mensag2.place(x=160, y=400)
                    self.ativ = 1
                    
                elif h == int(self.tempHora) and m + c == int(self.tempMin) and int(self.tempMin) >= 6:
                    
                    for i in range(0,6):
                        if i + m == int(self.tempMin):
                            self.mensag2['text'] = 'Restam '+str(i)+' Minutos!!'
                     
        elif int(self.tempHora) == 0:

            for c in range(1, 6):
                
                if m + c == int(self.tempMin) and m == 0 and s == 1 and int(self.tempMin) <= 5:
                    print('Parte 1 C')
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Restam '+str(c)+' Minutos!!', bg='red', fg='white', font=('arial', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                    
                elif m + c == int(self.tempMin) and int(self.tempMin) <= 5:

                    for i in range(1,6):
                        if i + m == int(self.tempMin):
                            self.mensag['text'] = 'Restam '+str(i)+' Minutos!!'

                if c == 5 and m + c == int(self.tempMin) and s == 0 and int(self.tempMin) >= 6 and int(self.tempMin) <= 59:
                    print('Parte 2 Co')
                    telaVermelha2()
                    self.mensag2 = Label(self.frameRight, text='Restam '+str(c)+' Minutos!!', bg='red', fg='white', font=('arial', 20, 'bold'))
                    self.mensag2.place(x=160, y=400)
                    self.ativ = 1
                    
                elif m + c == int(self.tempMin) and int(self.tempMin) >= 6:
                    
                    for i in range(1,6):
                        if i + m == int(self.tempMin):
                            self.mensag2['text'] = 'Restam '+str(i)+' Minutos!!'
                            
        if self.ativ == 1:
            self.ativaMensagem = 2
                
        if s == int(self.tempSeg) and m == int(self.tempMin) and h == int(self.tempHora):
            self.tempoEsgotado = True
            
            if self.ativaMensagem == 2 and int(self.tempMin) >= 6:
                self.mensag2.destroy()
            
            elif int(self.tempMin) <= 5:
                self.mensag.destroy()
            
                    
            if self.chaveTempExtra >= 1:
                self.tempExtraGastoA += int(self.tempHora)
                self.tempExtraGastoB += int(self.tempMin)
                self.tempExtraGastoC += 0
                print('exemplo 1: tempgastoAB', self.tempExtraGastoB, self.tempExtraGastoC)
                print('exemplo 1: tempos', self.tempHora, self.tempMin)
            
            self.objetos_cores('#870000', 'white')
            self.imagemTempRel.destroy()                      
            self.botFinalizar.destroy()
            self.botPausar.destroy()
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
            
    def iniciarContOper(self):

        #configurando os segundos para aparecer no label
        if self.secOperacao == None:
            self.secOperacao = 0
            self.sC = '00'
            self.mC = '00'
            self.hC = '00'
        self.secOperacao = self.secOperacao + 1
        if self.secOperacao > 0 and self.secOperacao <10:
            sA = self.secOperacao / 100
            sB = str(sA)
            self.sC = sB[2:]
        else:
            self.sC = str(self.secOperacao)
        if self.secOperacao > 59:
            self.secOperacao = 0
            self.sC = '00'

            #configurando os minutos para aparecer no label
            if self.minuOperacao == None:
                self.minuOperacao = 0
            self.minuOperacao = self.minuOperacao + 1

            if self.minuOperacao > 0 and self.minuOperacao <10:
                mA = self.minuOperacao / 100
                mB = str(mA)
                self.mC = mB[2:]
            else:
                self.mC = str(self.minuOperacao)            

            if self.minuOperacao > 59:
                self.minuOperacao = 0
                self.minuC = '00'

                #configurando a hora do temporizador
                if self.houOperacao == None:
                    self.houOperacao = 0
                self.houOperacao = self.houOperacao + 1

                if self.houOperacao > 0 and self.houOperacao < 10:
                    hA = self.houOperacao / 100
                    hB = str(hA)
                    self.hC = hB[2:]
                else:
                    hC = str(self.houOperacao)
        
        self.segundos['text'] = self.sC
        self.minutos['text'] = self.mC
        self.horas['text'] = self.hC

        self.tempOperando = self.hC+':'+self.mC+':'+self.sC 
        
        '''if self.chaveFinalizar2 == False:
            self.segundos.after(1000, self.iniciarContOper)'''

#------------------------------- (Tela Operativa) - FUNÇÃO xº A SER INVOCADA POR: botReinciar -----------------            
    def contagemFinalizada(self):
        '''Função rensponsável por finalizar a contagem, informando
        que o tempo foi atingido dentro do limite.'''
            
        self.chaveFinalizar = True
        
        #Se o cahveFinalizar foir verdadeira, o crobômetro para a contagem
        if self.chaveFinalizar == True:
            self.botFinalizar.destroy()
            self.botPausar.destroy()
            
            self.labFinalizar =  Label(self.frameRight, text='Processesso Finalizado!',  bg='red', fg='white', font=('arial', 25, 'bold'))
            self.labFinalizar.place(x=100, y=160)
            
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
            if self.chaveTempExtra == 0:
                self.tempGasto = self.houC+':'+self.minuC+':'+self.secC
                self.tempExtraGasto = '00:00:00'
            else:
                self.tempGasto = self.backup
            
            if self.chaveTempExtra >= 1:
                
                print(f'self.tempExtraGastoB {self.tempExtraGastoB} | self.minuC: {int(self.minuC)}')
                if int(self.minuC) + self.tempExtraGastoB >= 60:
                    self.tempExtraGastoA += 1
                    self.tempExtraGastoB -= int(self.minuC)
                else:
                    self.tempExtraGastoA += int(self.houC)
                    self.tempExtraGastoB += int(self.minuC)    
                    self.tempExtraGastoC += int(self.secC)
                print(f'self.tempExtraGastoB {self.tempExtraGastoB} | self.minuC: {int(self.minuC)}')
                
                self.tempExtraGasto = self.transformar_tempo_decimal(self.tempExtraGastoA, self.tempExtraGastoB, self.tempExtraGastoC)
                print(self.tempExtraGasto)
                
            #Botão caso o operado queira realizar outra S.O
            self.botReiniciar = Button(self.frameRight, text='NOVO.OS', bg='#035700', fg='white', activebackground='#035700', activeforeground='white', border=5, relief='ridge', font=('arial', 20, 'bold'), width=15, command = lambda: self.nova_tela_operacao())
            self.botReiniciar.place(x=150, y=230)
            
            #Enviando todos os dados ao banco
            try:
                self.cursor.execute('use empresa_funcionarios')
                self.cursor.execute("insert into monitoria_funcionarios VALUES('id','"
                                    +str(self.operador)+"','"
                                    +str(self.horaLogin)+"','"
                                    +str(self.horaInicial)+"','"
                                    +str(horaFinal)+"','"
                                    +self.tempGasto+"','"
                                    +str(self.tempProg)+"','"
                                    +self.codP+"','"
                                    +self.numOS+"','"
                                    +str(self.tempExtraGasto)+"','"
                                    +str(self.chaveTempExtra)+"','"
                                    +self.tempOperando+"','"
                                    +self.tipo+"')")
                                    
                self.banco.commit()
            #Excessão caso ocorra de não conseguir salvar
            except:
                self.alerta_erro_servidor('05-Error-Servidor: Não acesso ao servidor')

    #------------------------------- (Tela Operativa) - FUNÇÃO xº A SER INVOCADA POR: botReinciar -----------------
    def tentativa_pausar(self):
        self.janelaPause = Toplevel()
        self.janelaPause.title('Relatório de Pausa')
        self.janelaPause.iconbitmap('img/icone2.ico')
        self.janelaPause.resizable(False, False)
        self.janelaPause.configure(background='white')

        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(500, 500, self.janelaPause)
        
        def ok():
            if marcado1.get() == 1 or marcado2.get() == 1 or marcado3.get() == 1:
                if marcado1.get() == 0:
                    mot1['state'] = DISABLED
                else:
                    self.resultPausa = 'Horário de Almoço'
                
                if marcado2.get() == 0:
                    mot2['state'] = DISABLED
                else:
                    self.resultPausa = 'Outras OS'
                    
                if marcado3.get() == 0:
                    mot3['state'] = DISABLED
                else:
                    self.resultPausa = 'Final de Expediente'
            else:
                mot1['state'] = ACTIVE
                mot2['state'] = ACTIVE
                mot3['state'] = ACTIVE

        motivo = Label(self.janelaPause, text='Motivo de Pausa:', font=('arial', 20, 'bold'), bg='white', fg='#3e8e94')
        motivo.place(x=20, y=20)
        
        marcado1 = IntVar()
        mot1 = Checkbutton(self.janelaPause, text='Horário de Almoço', variable=marcado1, activebackground='white', activeforeground='#3e8e94', bg='white', fg='#3e8e94', command=ok, font=('arial',14,'bold'))
        mot1.place(x=30, y=100)
        
        marcado2 = IntVar()
        mot2 = Checkbutton(self.janelaPause, text='Outra OS', variable=marcado2, command=ok, font=('arial',14,'bold'), activebackground='white', activeforeground='#3e8e94', bg='white', fg='#3e8e94')
        mot2.place(x=30, y=200)                
        
        marcado3 = IntVar()
        mot3 = Checkbutton(self.janelaPause, text='Final de Expediente', variable=marcado3, command=ok, font=('arial',14,'bold'), activebackground='white', activeforeground='#3e8e94', bg='white', fg='#3e8e94')
        mot3.place(x=30, y=300)
        
        confirmar = Button(self.janelaPause, text='Confirmar', bg='#3e8e94', fg='white', border=0, font=('arial', 12), width=10, command = lambda:self.analisar_pausa())
        confirmar.place(x=210,y=400)
        
        self.janelaPause.mainloop()
        
    def analisar_pausa(self):        
        
        if self.tempoEsgotado == True:

            self.alerta_erro_servidor('Tempo Esgotado! Impossível Pausar')
        
        elif self.resultPausa == '':
            
            self.alerta_mensagem('Marque uma Opção!', 15, 75, 20)
            
        else:
            self.contagem_pausada()
        
    def contagem_pausada(self):
        
        self.janelaPause.destroy()
        self.chaveFinalizar = True
        self.botFinalizar.destroy()
        self.botPausar.destroy()
        self.sair.destroy()
        
        try:
            time = datetime.now().time()
            lista = [str(time)]
            recebe = ''
            for c in lista:
                for i in c:
                    if i == '.':
                        break
                    else:
                        recebe += i
            self.horaPause = recebe                        
            
            self.cursor.execute('use empresa_funcionarios')
            self.cursor.execute("insert into pausa_funcionarios VALUES('id','"+str(self.operador)+"','"+self.codP+"','"+self.numOS+"','"+self.resultPausa+"','"+self.horaPause+"','0')")
            self.banco.commit()     
            
        except:
            self.alerta_erro_servidor('06-Error-Servidor: Não acesso ao servidor')            
        
        self.botDespausar = Button(self.frameRight, text='RETOMAR.OS', bg='green', fg='white',border=5, relief='ridge', font=('arial', 22, 'bold'), width=15, command = lambda: self.contagem_despausar())
        self.botDespausar.place(x=140, y=220)        
    
    def contagem_despausar(self):
        try:
            time = datetime.now().time()
            lista = [str(time)]
            recebe = ''
            for c in lista:
                for i in c:
                    if i == '.':
                        break
                    else:
                        recebe += i
            self.horaRetomada = recebe
            print(self.horaRetomada)
            self.cursor.execute('use empresa_funcionarios')
            self.cursor.execute("update pausa_funcionarios set horaRetomada = '"+self.horaRetomada+"' where operador = '"+self.operador+"' and codigoPeca = '"+self.codP+"' and OS = '"+self.numOS+"' and horaPause = '"+self.horaPause+"' and horaRetomada = 0 ")
            self.banco.commit()     
            
        except:
            self.alerta_erro_servidor('07-Error-Servidor: Não acesso ao servidor')            
            
        self.botDespausar.destroy()
        if self.chaveFinalizar == True:
            self.chaveFinalizar = False
            
            self.sair = Button(self.frameTop, text='Sair', font=('arial',14,'bold'), fg='white', bg='red', activebackground='red', activeforeground='white', border=1, width=5, command=lambda:self.sairTela())
            self.sair.place(x=1180,y=20)            
            
            self.botFinalizar = Button(self.frameRight, text='FINALIZAR.OS', bg='red', fg='white',border=5, relief='ridge', font=('arial', 22, 'bold'), width=15, command = lambda: self.contagemFinalizada())
            self.botFinalizar.place(x=140, y=160)
            
            self.botPausar = Button(self.frameRight, text='PAUSAR.OS', bg='green', fg='white',border=5, relief='ridge', font=('arial', 22, 'bold'), width=15, command = lambda: self.tentativa_pausar())
            self.botPausar.place(x=140, y=260)
            
            self.botao_iniciar()
            
    
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
            
            messagebox.showwarning('Alerta', 'Sistema em Operação Ainda.')

instancia = LoginAdmnistracao()
