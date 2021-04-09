#Pogramador: Misael Jesus
#Date: 18/08/2020

#Importando Módulos
from datetime import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import nametofont
from platform import *
import mysql.connector
import sqlite3
import threading
import Script_Database_Local

#import RPi.GPIO as gpio

class AplicacaoBack():
    

    def enviar_dados(self):
        try:
            
            #Procurando Registros no Banco de Dados Local, e em seguida enviando-os para o Banco Servidor
            self.cursorLocal.execute('select * from OS_Pausadas')
            registro = self.cursorLocal.fetchall()
            
            if len(registro) >= 0:
            
                for linha in range(len(registro)):
                    
                    self.cursorServer.execute('insert into pausa_funcionarios VALUES'+str(registro[linha]))
                    self.bancoServer.commit()
                    
                self.cursorLocal.execute('DELETE FROM OS_Pausadas')
                self.bancoLocal.commit()
            
            
            #Procurando Registros no Banco de Dados Local, e em seguida enviando-os para o Banco Servidor
            self.cursorLocal.execute('select * from OS_Finalizadas')
            registro = self.cursorLocal.fetchall()
            
            if len(registro) >= 0:
                
                for linha in range(len(registro)):
                    
                    self.cursorServer.execute('insert into monitoria_funcionarios VALUES'+str(registro[linha]))
                    self.bancoServer.commit()
                
                self.cursorLocal.execute('DELETE FROM OS_Finalizadas')
                self.bancoLocal.commit()
                
        except Exception as erro:
            print(erro)
            print('erro ao enviar dados do banco de dados local')
            
    def verificar_conexao(self):

        if self.bancoCriado == True and self.bancoConect == True:

            if self.bancoServer.is_connected() == True:
                self.enviar_dados()
            else:
                self.botao.after(1000, self.verificar_conexao)
        else:
            self.botao.after(1000, self.verificar_conexao)
    
    def conection_database_local(self):
        try:

            print('BANCO DE DADOS LOCAL CONECTADO')

            self.bancoLocal = sqlite3.connect('Multimoldes_Database_Local')
            self.cursorLocal = self.bancoLocal.cursor()
            
        except Exception as erro:
            print(erro)
    
    def verifica_banco(self):
        #print('Rodando verificação ...')
        try:
            if self.bancoCriado == False:
                #print('Variável banco não foi criado: chamando função')
                threading.Thread(target=self.conection_database,).start()
            
            elif self.bancoCriado == True and self.bancoConect == True:
                if self.bancoServer.is_connected() != True:
                    #print('Variável chaveBanco não está conectado: chamando função')
                    threading.Thread(target=self.conection_database,).start()
            
        except Exception as erro:
            print('Erro na função verifica_banco:', erro.__class__)
            print(erro)
        
        #Chamando função constantemente a cada 2 segundos
        self.botao.after(2000, self.verifica_banco)

    def conection_database(self):
        
        #Tentando conexão com o banco de dados
        try:
            
            self.bancoServer = mysql.connector.connect(
                
                host = "localhost",
                user = "MultimoldesClient",
                password = "",
                database="empresa_funcionarios")
            
            #verificando se usuário existe no banco de dados
            self.cursorServer = self.bancoServer.cursor()
            
            self.bancoCriado = True
            self.bancoConect = self.bancoServer.is_connected()
        
        except:
            print('Ocorreu um erro ao tentar conectar-se ao banco de dados')

    def conection_database_close(self):
        
        self.bancoServer.close()
        self.cursorServer.close()

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

    def transicao(self, event):
        
        a = self.valorBotao
        b = self.admSenhaPrincipal.get()
        
        self.verificar_adm(a, b)
    
    def verificar_adm(self, direcionar, senha):
        
        #Verificando se o campo de senha está vazio
        if senha == '':
            
            self.labelError2['text'] = 'Preencha o campo!'
            
            return 0
        
        #Verificando se a senha digitada não é numérica
        elif not str(senha).isnumeric():
            
            self.labelError2['text'] = 'Senha Incorreta. Tente Novamente!'
            
            return 0
            
        #Se a senha for numérica irá verificar no banco de dados se existe
        try:
            
            self.cursorServer.execute('select * from supervisor_admin where senha ='+str(senha))
            valido = self.cursorServer.fetchall()
            
        except Exception as erro:
        
            print(erro)
            return messagebox.showerror(parent=self.janelaADM, title='01-Error-Servidor', message='01-Error: Não acesso ao servidor.')
            
        #Se (valido) == 1 significa que encontrou resultado
        if len(valido) == 1:
            
            #Se (direcionar) for igual a 1, irá abrir a tela de tempo extra
            if direcionar == 1:
                self.janelaADM.destroy()
                self.tempo_extra()

        else:
            
            self.labelError2['text'] = 'Senha Incorreta. Tente Novamente!'
            
            return 0

    def verificar_tempo_extra(self, event):
        
        #Verificando se os campos não estão em brancos
        if self.ll.get() == '' or self.mm.get() == '':
            
            messagebox.showwarning(parent=self.janelaTempExtra, title='Alerta', message='Verifique os Campos.')
        
        #Verificando se os caracteres dos campos são inteiros
        elif str(self.ll.get()).isnumeric() == False or str(self.mm.get()).isnumeric() == False:
            
            messagebox.showwarning(parent=self.janelaTempExtra, title='Alerta', message='Verifique os Campos.')

        #Verificando se nos campos o minutoExtra não é menor que 5, enquanto a horaExtra for igual a 0
        elif int(self.mm.get()) < 5 and int(self.ll.get()) == 0:
            
            messagebox.showwarning(parent=self.janelaTempExtra, title='Alerta', message='Valor Min: 0 Horas\nValor Min: 5 Minutos')
        
        #Verificando se nos campos o minutoExtra não é maior que 59 ou a horaExtra não é maior que 24
        elif int(self.mm.get()) > 59 or int(self.ll.get()) > 24:
            
            messagebox.showwarning(parent=self.janelaTempExtra, title='Alerta', message='Valor Max: 24 Horas\nValor Max: 59 Minutos')
        
        else:
            self.configurar_tempo_extra()

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
        
        #Pegando a hora e o minuto da janela de tempo extra
        ll = self.ll.get()
        mm = self.mm.get()
        
        #Destruindo a janela de tempo extra
        self.janelaTempExtra.destroy()
        
        #Destruindo Frame que contem o botão Finalizar OS
        self.botFrameFinalizar.destroy()
        
        #Variável que armazenará o último tempo adcionado
        self.UltimoTempAdd = self.transformar_tempo_decimal(ll, mm, 0)
        print(f'Hora Extra Adicionada: {self.UltimoTempAdd}')
        
        self.bteste = 5
        
        #Configurando tempo Extra gasto caso o operador precise de mais tempo mais de uma vez
        self.chaveTempExtra += 1
        
        #Regularizando os valores do cronômetro para o valor inicial 00:00:00
        self.seconds['text'] = '00'
        self.minutes['text'] = '00'
        self.hours['text'] = '00'
        
        #Estabilizando as variáveis necessárias para não dá conflito
        self.tempoPausado = False
        self.chaveControle = False
        self.chaveFinalizar = False

        self.sec = None

        self.minu = None

        self.hou = None

        self.frameBotReabilitar.destroy()
        
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
        
        self.vezes = Label(self.frameLeft, text='x'+str(self.chaveTempExtra), width=2, font=('arial', 15, 'bold'), bg='#870000', fg='white')
        self.vezes.place(relx=0.950, rely=0.700)
        
        #Exibindo no label o horário adcionado após o tempo ser esgotado
        self.campoProExt = Label(self.frameLeft, text=self.tempProgExt, width=8, font=('arial', 15, 'bold'), bg='white', fg='red')
        self.campoProExt.place(relx=0.810, rely=0.700)
        
        self.frameBotIniciar = Frame(self.frameRight, highlightbackground='black', highlightthickness=2)
        self.frameBotIniciar.place(x=220, y=200)        
        
        #Botão inciar a contagem do cronômetro
        self.botaoInciarContador = Button(self.frameBotIniciar, text='INICIAR', bg='#035700', fg='white', activebackground='#035700', activeforeground='white', relief='flat', font=('arial', 25, 'bold'), command = lambda:self.botao_iniciar(1))
        self.botaoInciarContador.pack()

    def confirmar_tela_funcionario(self, event):
        
        self.labelError = Label(self.frameLogin, text='', fg='#bf0606', bg='white', width=40, font=('arial', 12))
        self.labelError.place(relx=0.200, rely=0.610)
        
        #verificando se o campo "login" é numérico e possui 11 caracteres
        if str(self.campoLogin.get()).isnumeric() and len(self.campoLogin.get()) == 11:
            self.user = self.campoLogin.get()

            #verificando se a senha é númerica e possui 4 caracteres
            if str(self.campoSenha.get()).isnumeric() and len(self.campoSenha.get()) == 8:
                self.password = self.campoSenha.get()

                try:
                                        
                    #Tentando buscar usuário que se enquadre ao CPF e SENHA digitado e armazenado nas variáveis a seguir
                    self.cursorServer.execute("select Nome from funcionarios where CPF = '"+self.user+"' and Senha = '"+self.password+"'")
                    valido = self.cursorServer.fetchall()
                    
                except Exception as erro:
                    
                    print(erro)
                    return messagebox.showerror(parent=self.janelaFuncio, title='03-Error-Servidor', message='03-Error: Não acesso ao servidor.')

                #pegando hora atual de login caso encontrar resultado na busca
                if len(valido) == 1:
                    
                    self.operador = valido[0][0]
                    time = datetime.now().time().strftime('%H:%M:%S')
                    self.horaLogin = time
                    self.janelaFuncio.withdraw()
                    self.tela_de_operacao()
                
                #alerta caso o usuário não seja encontrado
                else:
                    return messagebox.showerror(parent=self.janelaFuncio, title='Alerta', message='Login não Existe!')
            
            #caso o campo "senha" esteja vazio
            elif self.campoSenha.get() == '':
                self.labelError['text'] = 'Preencha o campo!'
            
            #caso o campo "senha" diferentee de 11 caracteres
            else:
                self.labelError['text'] = 'Usuário ou Senha Incorreta!'
        
        #caso o campo "login" esteja vazio
        elif self.campoSenha.get() == '':
            self.labelError['text'] = 'Preencha o campo!'
        
        #se caso o campo "login" seja diferente de 11 caracteres
        else:
            self.labelError['text']= 'Usuário ou Senha Incorreta!'

    def confirmarCampos(self, event):
        
        a = self.campoServico.get()
        b = self.campoPeca.get()
        c = self.campQuantidadePeca.get()
        d = self.campoOperacao.get()
        
        #Verificando se algum campo está em branco
        if a == '' or b == '' or c == '' or int(c) <= 0 or d == '':
            
            return messagebox.showerror(parent=self.janelaOper, title='Alerta', message='Verifique os Campos!')
        
        #Verificando se os caracteres digitados nos campos são de valor numérico
        elif self.campoServico.get().isnumeric() == False or self.campoPeca.get().isnumeric() == False or self.campQuantidadePeca.get().isnumeric() == False or self.campoOperacao.get().isnumeric() == False:

            return messagebox.showerror(parent=self.janelaOper, title='Alerta', message='Os Campos Precisam ser Numéricos!')
        
        #Buscando o Código de Peça no banco de dados
        self.cursorServer.execute("select codigo from pecas_codigo where codigo = "+self.campoPeca.get())
        valido = self.cursorServer.fetchall()
        
            
        #Se ao ler a variável valido o valor for igual a 0, provavelmente não existe no banco de dados
        if len(valido) == 0:
            
            #Exibindo mensagem alertando que o Código de Peça não foi encontrado
            return messagebox.showerror(parent=self.janelaOper, title='Alerta', message='Código não Encontrado!')
        
        
        #Buscando no banco de dados se existe a OS digitada e o Código de Peça em modo pausado
        self.cursorServer.execute('select * from pausa_funcionarios where OS ='+self.campoServico.get()+' and codigoPeca = '+self.campoPeca.get()+' and CodigoOperacao = '+self.campoOperacao.get()+' and horaRetomada = 0 and dataRetomada = 0')
        checar = self.cursorServer.fetchall()
        
        #Se ao ler a variável "checar" o valor for maior ou igual a 1, provavelmente existe no banco de dados
        if len(checar) >= 1:
            
            #Exibindo mensagem que a OS e o Código de Peça estão pausados, e se deseja abrir a janela de OS Pendente
            perguntar = messagebox.askquestion(parent=self.janelaOper, title='Alerta', message='OS e Nº de Peça pausados. Abrir janela de OS Pendentes?')
            
            #Se for sim, irá abrir a janela
            if perguntar == 'yes':
                
                return self.verificação_de_OS()
            
            else: return ''
        
        #Verificando se o funcionário está apto para fazer a peça
        self.cursorServer.execute('select Processo_Usinagem from operacao_codigo where Codigo_Operacao = '+ self.campoOperacao.get())
        checaOperacao = self.cursorServer.fetchall()
        
        if len(checaOperacao) == 0:
            
            return messagebox.showerror(parent=self.janelaOper, title='Alerta', message='Código de Operação Não Encontrado!')
        
        #Armazenando nome da Operação extraída do banco de dados
        ProcessoUninagem = checaOperacao[0][0]
        
        self.cursorServer.execute('select '+ProcessoUninagem+' from habilidade_funcionarios where CPF = '+self.user)
        checaOperacao = self.cursorServer.fetchall()
        
        #Armazenando valor relacionado à habilidade do funcionário extraída do banco de dados
        habilidadeFuncionario = checaOperacao[0][0]
        
        if habilidadeFuncionario == 0:
            
            #Exibindo alerta que não é possível o funcionário cumprir a operação
            return messagebox.showinfo(parent=self.janelaOper, title='Alerta', message=f'Capacitação específica insuficiente para o comprimento desta tarefa.\n\nProcesso de Usinagem: {ProcessoUninagem}\nHabilidade do Funcionário: {habilidadeFuncionario}')
            
        else:
            
            #Buscando a OS digitada no banco de dados
            self.cursorServer.execute('select * from monitoria_funcionarios where OS ='+ self.campoServico.get()+' and CodigoPeca ='+self.campoPeca.get()+' and CodigoOperacao ='+self.campoOperacao.get())
            valido = self.cursorServer.fetchall()
                   
            self.checkSelect = PhotoImage(file='img/verifica.png')
            
            #Se o resultado da busca for igual a 0, então é uma Nova OS
            if len(valido) == 0:
                
                self.novoSelect['image'] = self.checkSelect
                self.tipo = 'Nova OS'
                
                #Quando o parâmetro for 1, o preenchimento dos campos está sendo feito pessoalmente e não automático
                self.botaoConfirmarOS(1)
            
            #Senão se o resultado da buscar for diferente de 0, então já existe uma OS digitada
            else:
                
                self.retrabalhoSelect['image'] = self.checkSelect
                self.tipo = 'Retrabalhar OS'
                
                #Quando o parâmetro for 1, o preenchimento dos campos está sendo feito pessoalemnte e não automático
                self.botaoConfirmarOS(1)

    def botaoConfirmarOS(self, opcao):
        
        self.logoMarcaRight.destroy()
        
        #Pegando o número de OS digitada no campo e armazenando na variável
        self.numOS = str(self.campoServico.get())
        
        #Pegando o código de Peca no campo e armazenando na variável
        self.codP = str(self.campoPeca.get())
        
        #Pegando a quantidade de peças e armazenando na variável
        self.quant = str(self.campQuantidadePeca.get())
        
        #Pegando o número de Operação no campo e armazenando na variável
        self.numOper = str(self.campoOperacao.get())
    
        try:
                        
            self.cursorServer.execute("select hora, minuto from pecas_codigo where codigo = "+self.codP)
            tempo_pecas = self.cursorServer.fetchall()
        
            self.mi = 0
            self.se = 0
            self.tempHora = tempo_pecas[0][0]
            self.tempMin = tempo_pecas[0][1]
            self.tempSeg = '00'
            
            #Formatando as varíaveis para encaixar no label - Tempo Programado
            self.tempProg = self.tempHora+':'+self.tempMin+':'+self.tempSeg
            
            #Se a função foi invocada pelo parâmetro 2, #Quando pausado, se o tempo adcionado era tempo extra, então ao retomar irá continuar sendo tempo extra e o último tempo Adcionado
            if opcao == 2:
                
                #Selecionando do banco de dados onde o id for igual ao número de is da lista já separada igual a 10
                self.cursorServer.execute('select * from pausa_funcionarios where ID = '+self.tuplaSelect[0])
                valido = self.cursorServer.fetchall()
                
                if len(valido) == 1:
                    
                    #Recebendo cor da tela de quando foi pausada
                    self.corTelaAtual = valido[0][17]
                    
                    li = ''
                    listaNum = ''
                    #Recebendo o número de vezes tempo extra do banco de dados
                    verificandoTempExtra = valido[0][14]
                    
                    #Se for maior ou igual a 1 significa que o tempo que será adcionado e contado será do Tempo Extra restante
                    if int(verificandoTempExtra) >= 1:
                        
                        #Desfragmentando Tempo Extra já gasto pelo funcionário
                        tempo = valido[0][13]
                        for v in tempo:
                            if v != ':':
                                listaNum += v
                            else:
                                listaNum += ' '
                        listaNum.split()
                        listaNumSeparada = listaNum.split()
                        
                        self.tempExtraGastoA += int(listaNumSeparada[0])
                        self.tempExtraGastoB += int(listaNumSeparada[1])
                        self.tempExtraGastoC += 0
                        
                        #Desfragmentando o Último Tempo Adicionado tempo extra do banco de dados
                        t = valido[0][15]
                        for num in t:
                            if num != ':':
                                li += num
                            else:
                                li += ' '
                        liDesfragment = li.split()
                        
                        #Quando pausado, se o tempo adcionado era tempo extra, então as variáveis vão armazenar o tempo exigido
                        self.mi = 0
                        self.se = 0
                        self.tempHora = liDesfragment[0]
                        self.tempMin = liDesfragment[1]
                        self.tempSeg = liDesfragment[2]
                        
                        #Quando pausado, se o tempo adcionado era tempo extra, então ao retomar irá continuar sendo tempo extra e o último tempo Adcionado
                        self.UltimoTempAdd = valido[0][15]

                        #Quando pausado, se o tempo adcionado era tempo extra, então ao retomar o contador de vezes irá retomar com o valor de onde parou
                        self.chaveTempExtra = int(valido[0][14])
                        
                        self.vezes = Label(self.frameLeft, text='x'+str(self.chaveTempExtra), width=2, font=('arial', 15, 'bold'), bg='#135565', fg='white')
                        self.vezes.place(x=750, y=400)
                                
                        #Exibindo no label o horário adcionado após o tempo ser esgotado
                        self.campoProExt = Label(self.frameLeft, text=self.UltimoTempAdd, width=8, font=('arial', 15, 'bold'), bg='white', fg='red')
                        self.campoProExt.place(x=640, y=400)
                    
                    #Armazenando na variável o tempo marcado quando pausado
                    marcaTemp = valido[0][11]
                    
                    #Criando variável para obter o tempo marcado sem ser na forma de horário 00: 00: 00
                    self.tempoDePauseObtido = ''
                    
                    #Lógica para obter o tempo marcado sem os pontos : :
                    for c in marcaTemp:
                        if c != ':':
                            self.tempoDePauseObtido += c
                        else:
                            self.tempoDePauseObtido +=' '
                    
                    self.backup = valido[0][16]
                
                    
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
            
            if opcao == 1:
                self.backup = str(self.tempHora)+':'+str(self.tempMin)+':'+str(self.tempSeg)

            #Mostrando o tempo Programado através do label
            self.tempoProgramado = Label(self.frameLeft, text='Tempo Programado:', font=('arial', 17, 'bold'), bg='#135565', fg='white')
            self.tempoProgramado.place(relx=0.070, rely=0.700)
            
            self.campoProgramado = Label(self.frameLeft, width=15, font=('arial', 15, 'bold'), bg='white')
            self.campoProgramado.place(relx=0.380, rely=0.700)
            
            self.campoProgramado['text'] = self.tempProg
            
            #Deletando botão confirmar após preencher os campos e confirmar
            self.botConfirmar.destroy()
            
            #Deletando campos de preenchimento para criação dos mesmos, porém em formato de Labels
            self.campoServico.destroy()
            self.campoPeca.destroy()
            self.campQuantidadePeca.destroy()
            self.campoOperacao.destroy()
            
            #Mudando os campos Entry para Labels para exibir na tela
            self.campoServico = Label(self.frameLeft, text=self.numOS, width=20, font=('arial', 19), bg='white')
            self.campoServico.place(relx=0.455, rely=0.170)

            self.campoPeca = Label(self.frameLeft, text=self.codP, width=20, font=('arial', 19), bg='white')
            self.campoPeca.place(relx=0.455, rely=0.340)
            
            self.campoOperacao = Label(self.frameLeft, text=self.numOper, width=20, font=('arial', 19), bg='white')
            self.campoOperacao.place(relx=0.455, rely=0.510)
            
            self.campQuantidadePeca = Label(self.frameLeft, text=self.quant, font=('arial', 19), bg='white')
            self.campQuantidadePeca.place(relx=0.880, rely=0.340, relwidth=0.085)
            
            #Labals que imprimem o cronômetro que totaliza o tempo de operação do funcionário
            self.segundos = Label(self.frameLeft, text='00', font=('alarm clock',12,'bold'), width=2, fg='#023300')
            self.segundos.place(relx=0.212, rely=0.880)
            self.minutos = Label(self.frameLeft, text='00', font=('alarm clock',12,'bold'), width=2, fg='#023300')
            self.minutos.place(relx=0.176, rely=0.880)
            self.horas = Label(self.frameLeft, text='00', font=('alarm clock',12,'bold'), width=2, fg='#023300')
            self.horas.place(relx=0.140, rely=0.880)
            
            self.tempOperando = '00:00:00'
            
            #Se a opcao for igual a 1: A OS está sendo criada e não é uma OS Pendente
            if opcao == 1:
            
                self.frameBotIniciar = Frame(self.frameRight, highlightbackground='black', highlightthickness=2)
                self.frameBotIniciar.place(x=220, y=200)
                
                #Se o parâmetro for 1: A OS está sendo criada e não é uma OS Pendente
                self.botaoInciarContador = Button(self.frameBotIniciar, text='INICIAR', bg='#035700', fg='white', activebackground='#035700', activeforeground='white', relief='flat', font=('arial', 25, 'bold'), command = lambda:self.botao_iniciar(1))
                self.botaoInciarContador.pack()
            
            #Se a opcao for igual a 2: A OS está sendo retomada pois é uma OS Pendente
            elif opcao == 2:
                
                #Configurando contagem de operagem com os dados salvos da pausagem
                tempoOperador = ''
                self.tempOperando = valido[0][21]
                
                #Formatando o dado extraído do banco de dados
                for elemento in self.tempOperando:
                    
                    if elemento == ':':
                        tempoOperador += ' '
                    else:
                        tempoOperador += elemento
                
                #Armazenando nas variáveis no tipo caracter para exibir no contador
                self.sC = tempoOperador.split()[2]
                self.mC = tempoOperador.split()[1]
                self.hC = tempoOperador.split()[0]
                
                self.segundos['text'] = self.sC
                self.minutos['text'] = self.mC
                self.horas['text'] = self.hC
                
                #Armazenando nas variáveis no tipo inteiro para fazer os calculos de contagem
                self.secOperacao = int(self.sC)
                self.minuOperacao = int(self.mC)
                self.houOperacao = int(self.hC)
                
                
                #Configurando o tempo do cronômetro para o tempo exato de uma OS Pausada em pendência caso a função tenha sido chamada pela janela de OS pausadas ainda pendente
                
                vetor = self.tempoDePauseObtido.split()
                self.hours['text'] = vetor[0]
                self.minutes['text'] = vetor[1]
                self.seconds['text'] = vetor[2]
                
                self.chaveFinalizar = True
                
                self.botFrameRetomar = Frame(self.frameRight, highlightbackground='black', highlightthickness=2)
                self.botFrameRetomar.place(x=172, y=220)
                
                #Ao criar botão para retomar OS o parâmetro 2, significa OS Pendente e deve ser feitas as demais configurações
                self.botDespausar = Button(self.botFrameRetomar, text='RETOMAR.OS', bg='#035700', fg='white',activebackground='#035700', activeforeground='white', relief='flat', font=('arial', 22, 'bold'), width=13, command = lambda: self.contagem_despausar(2))
                self.botDespausar.pack()
                
        except Exception as erro:
            print(erro)
            messagebox.showerror(parent=self.janelaOper, title='05-Error-Servidor', message='05-Error: Não acesso ao servidor.')

    def piscar_led(self):
        
        #Variável que irá realizar a contagem do LED Ligar e Desligar
        self.Led_OFF_ON +=1
        
        #Se a variável Led_OFF_ON == 1 o led irá desligar, pois abrirá a porta da GPIO
        if self.Led_OFF_ON == 1 and self.desligarfuncaoLed == False and self.tempoEsgotado == False:
            pass
            #gpio.output(8, gpio.LOW)
            #gpio.output(12, gpio.LOW)
            #gpio.output(18, gpio.LOW)
        
        #Se a variável Led_OFF_ON == 2 o led irá ligar, pois abrirá a porta da GPIO
        elif self.Led_OFF_ON == 2 and self.desligarfuncaoLed == False and self.tempoEsgotado == False:
            pass
            #gpio.output(8, gpio.LOW)
            #gpio.output(12, gpio.LOW)
            #gpio.output(18, gpio.HIGH)
            self.Led_OFF_ON = 0
        
        #Se a variável Led_OFF_ON == 1 o led irá desligar, pois abrirá a porta da GPIO
        elif self.Led_OFF_ON == 1 and self.desligarfuncaoLed == False and self.tempoEsgotado == True:
            pass
            #gpio.output(8, gpio.LOW)
            #gpio.output(12, gpio.LOW)
            #gpio.output(18, gpio.LOW)
        
        #Se a variável Led_OFF_ON == 2 o led irá ligar, pois abrirá a porta da GPIO
        elif self.Led_OFF_ON == 2 and self.desligarfuncaoLed == False and self.tempoEsgotado == True:
            pass
            #gpio.output(8, gpio.HIGH)
            #gpio.output(12, gpio.HIGH)
            #gpio.output(18, gpio.HIGH)
            self.Led_OFF_ON = 0
        
        if self.desligarfuncaoLed == False:
            
            #Quando a variável ledPiscando for True significa que a função já está ativa
            self.ledPiscando = True
            
            self.frameRight.after(500, self.piscar_led)
 
    def objetos_cores(self, cor1, cor2):
        
        #Se a cor1(cor que será o background da tela) for GREEN e não for tempo extra, acenderá só o led verde
        if cor1 == 'green' and self.chaveTempExtra == 0:
            pass
            #gpio.output(8, gpio.HIGH)
            #gpio.output(12, gpio.LOW)
            #gpio.output(18, gpio.LOW)
        
        #Se a cor1(cor que será o background da tela) for YELLOW e não for tempo extra, acenderá só o led amarelo
        elif cor1 == 'yellow' and self.chaveTempExtra == 0:
            pass
            #gpio.output(8, gpio.LOW)
            #gpio.output(12, gpio.HIGH)
            #gpio.output(18, gpio.LOW)
        
        #Se a cor1(cor que será o background da tela) for RED e não for tempo extra, acenderá só o led vermelho
        elif cor1 == 'red' and self.chaveTempExtra == 0:
            pass
            #gpio.output(8, gpio.LOW)
            #gpio.output(12, gpio.LOW)
            #gpio.output(18, gpio.HIGH)
        
        #Senão significa que está janela para tempo extra, então o led vermelho irá ficar piscando
        else:
            
            #Se ledPiscando for False então a função que fará o LED piscar não está ativa
            if self.ledPiscando == False:
                
                self.Led_OFF_ON = 0
                self.piscar_led()
        
        self.frameTop['bg'] = cor1
        self.frameLeft['bg'] = cor1
        self.frameRight['bg'] = cor1
        self.operadorNome['bg'] = cor1
        self.operadorNomeUser['bg'] = cor1
        self.horaInicialLb['bg'] = cor1
        self.multimolde['bg'] = cor1
        self.ordemServico['bg'] = cor1
        self.codigoPeca['bg'] = cor1
        self.lbQuantidadePeca['bg'] = cor1
        self.codigoOperacao['bg'] = cor1
        self.tempoProgramado['bg'] = cor1
        
        self.framenovoOS['bg'] = cor1
        self.novoOS['bg'] = cor1
        self.novoSelect['bg'] = cor1
        
        self.frameRetrabalho['bg'] = cor1
        self.retrabalhoOS['bg'] = cor1
        self.retrabalhoSelect['bg'] = cor1
        
        if self.chaveTempExtra >= 1:
            self.vezes['bg'] = cor1
            self.vezes['fg'] = cor2
        
        self.operadorNome['fg'] = cor2
        self.operadorNomeUser['fg'] = cor2
        self.horaInicialLb['fg'] = cor2
        self.multimolde['fg'] = cor2
        self.ordemServico['fg'] = cor2
        self.codigoPeca['fg'] = cor2
        self.lbQuantidadePeca['fg'] = cor2
        self.codigoOperacao['fg'] = cor2
        self.tempoProgramado['fg'] = cor2

    def botao_iniciar(self, iniciaCont):
        
        #if gpio.input(32) == gpio.HIGH:
        #    self.iniciarContOper()
            
        if self.chaveControle == False:
            
            #self.TempoEsgotado recebe False após clicado pelo botão iniciar, indicando dentro do prazo
            self.tempoEsgotado = False
            
            self.botFrameFinalizar = Frame(self.frameRight, highlightbackground='black', highlightthickness=2)
            self.botFrameFinalizar.place(x=182, y=160)
            
            self.botFinalizar = Button(self.botFrameFinalizar, text='FINALIZAR.OS', bg='#b30000', activebackground='#b30000', fg='white', activeforeground='white', relief='flat', font=('arial', 22, 'bold'), width=12, command = lambda: self.contagemFinalizada())
            self.botFinalizar.pack()
            
            self.botFramePausar = Frame(self.frameRight, highlightbackground='black', highlightthickness=2)
            self.botFramePausar.place(x=182, y=260)
            
            self.botPausar = Button(self.botFramePausar, text='PAUSAR.OS', bg='#035700', activebackground='#035700', fg='white', activeforeground='white', relief='flat', font=('arial', 22, 'bold'), width=12, command = lambda: self.tentativa_pausar())
            self.botPausar.pack()

            if iniciaCont == 1:
                
                #Escondendo o botão sair ao iniciar operação
                try:
                    self.frameBotSair.place_forget()
                except: pass
                
                self.frameBotIniciar.destroy()
                
                #Atribuindo a Hora Incial atual e a Data Inicial atual nas respectivas variáveis
                self.horaInicial = time = datetime.now().time().strftime('%H:%M:%S')
                self.dateInicial = datetime.now().date().strftime('%d/%m/%Y')
                
                self.objetos_cores('green', 'white')
                
                self.horaInit = 0
                self.minuInit = 0
                self.seguInit = 0
            
            elif iniciaCont == 2:
                
                #Escondendo o botão sair ao iniciar operação
                try:
                    self.frameBotSair.place_forget()
                except: pass
                
                vetor = self.tempoDePauseObtido.split()
                self.horaInit = vetor[0]
                self.minuInit = vetor[1]
                self.seguInit = vetor[2]

                self.objetos_cores(str(self.corTelaAtual), 'white')
            
            self.chaveControle = True
            
            #Variável que irá habilitar a porta para pode executar a máquina
            #gpio.output(24, gpio.HIGH)
            
        #Congfigurando os segundos do temporizador
        
        #Iniciando contagem do 0 e se iniciaCont == 1 a OS não é Pendente (Configuração dos Segundos)
        if self.sec == None and iniciaCont == 1:
            self.sec = 0
            self.secC = '00'
            self.minuC = '00'
            self.houC = '00'
        
        #Iniciando contagem de onde foi pausada e se iniciaCont == 2 a OS é Pendente (Configuração dos Segundos)
        elif self.sec == None and iniciaCont == 2:
            self.sec = int(self.seguInit)
            self.secC = str(self.seguInit)
            self.minuC = str(self.minuInit)
            self.houC = str(self.horaInit)        
        
        #Verificando se foi solicitado parada do tempo, senão o segundo irá continuar a contagem (Configuração dos Segundos)
        if self.chaveFinalizar == False:
            self.sec = self.sec + 1
        
        #Configurando para o segundo ser exibido em duas casas caso seja > 0 e < 10 (Configuração dos Segundos)
        if self.sec > 0 and self.sec < 10:
            secA = self.sec / 100
            secB = str(secA)
            self.secC = secB[2:]
        else: 
            self.secC = str(self.sec)

        #Caso o segundo seja > 59 irá ser configurado para voltar a ser 0 e o minuto ser 1 (Mintuos e Segundos)
        if self.sec > 59:
            self.sec = 0
            self.secC = '00'
            
            #Iniciando contagem do 0 e se iniciaCont == 1 a OS não é Pendente (Configuração dos Minutos)
            if self.minu == None and iniciaCont == 1:
                self.minu = 0
            
            #Iniciando contagem de onde foi pausada e se iniciaCont == 2 a OS é Pendente (Configuração dos Minutos)
            elif self.minu == None and iniciaCont == 2:
                self.minu = int(self.minuInit)
            
            #Verificando se foi solicitado parada do tempo, senão o minuto irá continuar a contagem (Configuração dos Minutos)
            if self.chaveFinalizar == False:
                self.minu = self.minu + 1
            
            #Configurando para o minuto ser exibido em duas casas caso seja > 0 e < 10 (Configuração dos Minutos)
            if self.minu > 0 and self.minu < 10:
                minuA = self.minu / 100
                minuB = str(minuA)
                self.minuC = minuB[2:]
            else:
                self.minuC = str(self.minu)
            
            #Caso o Minuto seja > 59 irá ser configurado para voltar a ser 0 e a hora ser 1 (Mintuos e Hora)
            if self.minu > 59:
                self.minu = 0
                self.minuC = '00'
                
                #Iniciando contagem do 0 e se iniciaCont == 1 a OS não é Pendente (Configuração das Horas)
                if self.hou == None and iniciaCont == 1:
                    self.hou = 0
                
                #Iniciando contagem de onde foi pausada e se iniciaCont == 2 a OS é Pendente (Configuração das Horas)
                if self.hou == None and iniciaCont == 2:
                    self.hou = int(self.horaInit)
                
                #Verificando se foi solicitado parada do tempo, senão a hora irá continuar a contagem (Configuração das Horas)
                if self.chaveFinalizar == False:
                    self.hou = self.hou + 1
                
                #Configurando para o hora ser exibido em duas casas caso seja > 0 e < 10 (Configuração das Horas)
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
                
                self.objetos_cores('yellow', 'white')
        
        def telaVermelha2():
            
            self.objetos_cores('red', 'white')

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
                    self.mensag = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                
                elif m + c == int(self.tempMin) and h == int(self.tempHora) and int(self.tempMin) <= 5:
                    
                    for i in range(1, 6):
                        if i + m == int(self.tempMin):
                            self.mensag['text'] = 'Resta '+str(i)+' Minuto'       

                if m + c == int(self.tempMin) and c == 5 and h == int(self.tempHora) and s == 0 and int(self.tempMin) >= 6 and int(self.tempMin) <= 59:
                    print('Parte 2 A')
                    telaVermelha2()
                    self.mensag2 = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag2.place(x=160, y=400)
                    self.ativ = 1
                
                elif m + c == int(self.tempMin) and h == int(self.tempHora) and int(self.tempMin) >= 6 and int(self.tempMin) <= 59:
                    
                    for i in range(0,6):
                        if i + m == int(self.tempMin):
                            self.mensag2['text'] = 'Resta '+str(i)+' Minuto'                                                 
                
                #PRECISA DAR A CONDIÇÃO PARA ESTE CASO AINDA
                if c == 5 and h == int(self.tempHora) - 1 and int(self.tempMin) == 0 and m + 5 == 60  and s == 0:
                    print('Parte 3 A')
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1                  
                
                elif h == int(self.tempHora) - 1 and int(self.tempMin) == 0 and m + c == 60:
                    for i in range(1, 6):
                        if i + m == 60:
                            self.mensag['text'] = 'Resta '+str(i)+' Minuto'
        
        #Se a hora programada for == 1 entrará nessa condição para aparecer a mensagem com precedênciares, resta 5 minutos
        elif int(self.tempHora) == 1:
            
            #Caso a OS seja despausada pela janela de OS Pendentes, onde parâmetro de iniciaCont == 2
            if iniciaCont == 2:
                
                '''Evitando conflito caso número pausado for == 59, pois ao inciar contagem já soma +1 então daria 60
                e a verificação de minutos restantes falharia, com esta condição verifica antes se os segundos pausados é igual 59
                se for igual a 59 recebe -1, para dar 0 como em um relógio normal ao terminar em 59 volta a ser 0'''
                if self.seguInit == '59':
                    valueS = -1
                    valueM = int(self.minuInit) + 1
                    if valueM == 60:
                        valueM = 0
                #Senão continuar a receber +1 normalemnte
                else:
                    valueS = int(self.seguInit)
                    valueM = int(self.minuInit)
                    valueH = int(self.horaInit)
                    
            elif iniciaCont == 1:
                valueS = 0
                valueM = 0            
            
            
            for c in range(1, 6):
                
                #Se a hora for == 1 e os minutos programado for == 0 ex: (01:00:00)
                if c == 5 and int(self.tempMin) == 0 and m + 5 == 60 and s == 0 or c+valueM==60 and int(self.tempMin) == 0 and m == valueM and s == valueS +1 and iniciaCont == 2:
                    print('Parte 1 B')
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                
                #Condição responsável por verificar a cada segundo quantos minutos falta
                elif int(self.tempMin) == 0 and m + c == 60:
                    for i in range(1,6):
                        if i + m == 60:
                            self.mensag['text'] = 'Resta '+str(i)+' Minuto'
                
                #Se a hora for == 1 e os minutos programado for == 1 ex: (01:01:00) ----------------------------
                if h == 0 and int(self.tempMin) == 1 and m == 56 and s == 0 and c == 5 or h == 0 and int(self.tempMin) == 1 and c+valueM==61 and m == valueM and s == valueS+1 and iniciaCont == 2:
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                    if iniciaCont == 2:
                        self.bteste = c
                
                #Condição responsável por verificar a cada segundo quantos minutos falta
                elif h == 0 and int(self.tempMin) == 1 and m >= 56 and c == 5 or h == 1 and int(self.tempMin) == 1 and m >= 0 and m <= 1 and c == 5:
                    if s == 0:
                        self.bteste -= 1
                        self.mensag['text'] = 'Resta '+str(self.bteste)+' Minuto'

                #Se a hora for == 1 e os minutos programado for == 2 ex: (01:02:00) ----------------------------
                if h == 0 and int(self.tempMin) == 2 and m == 57 and s == 0 and c == 5 or h == 0 and int(self.tempMin) == 2 and c+valueM==62 and m == valueM and s == valueS+1 and iniciaCont == 2:
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                    if iniciaCont == 2:
                        self.bteste = c
                
                #Condição responsável por verificar a cada segundo quantos minutos falta
                elif h == 0 and int(self.tempMin) == 2 and m >= 57 and c == 5 or h == 1 and int(self.tempMin) == 2 and m >= 0 and m <= 2 and c == 5:
                    if s == 0:
                        self.bteste -= 1
                        self.mensag['text'] = 'Resta '+str(self.bteste)+' Minuto'                        
                        
                #Se a hora for == 1 e os minutos programado for == 3 ex: (01:03:00) ----------------------------
                if h == 0 and int(self.tempMin) == 3 and m == 58 and s == 0 and c == 5 or h == 0 and int(self.tempMin) == 3 and c+valueM==63 and m == valueM and s == valueS+1 and iniciaCont == 2:
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                    if iniciaCont == 2:
                        self.bteste = c
                
                #Condição responsável por verificar a cada segundo quantos minutos falta
                elif h == 0 and int(self.tempMin) == 3 and m >= 58 and c == 5 or h == 1 and int(self.tempMin) == 3 and m >= 0 and m <= 3 and c == 5:
                    if s == 0:
                        self.bteste -= 1
                        self.mensag['text'] = 'Resta '+str(self.bteste)+' Minuto'                        
                
                #Se a hora for == 1 e os minutos programado for == 4 ex: (01:04:00)
                if h == 0 and int(self.tempMin) == 4 and m == 59 and s == 0 and c == 5 or h == 0 and int(self.tempMin) == 4 and c+valueM==64 and m == valueM and s == valueS+1 and iniciaCont == 2:
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                    if iniciaCont == 2:
                        self.bteste = c
                
                #Condição responsável por verificar a cada segundo quantos minutos falta
                elif h == 0 and int(self.tempMin) == 4 and m == 59 and c == 5 or h == 1 and int(self.tempMin) == 4 and m >= 0 and m <= 4 and c == 5:
                    if s == 0:
                        self.bteste -= 1
                        self.mensag['text'] = 'Resta '+str(self.bteste)+' Minuto'
                
                #Se a hora for == 1 e os minutos programado for == 5 ex: (01:05:00)
                if h == int(self.tempHora) and m + c == int(self.tempMin) and m == 0 and s == 0 and int(self.tempMin) == 5 or h == int(self.tempHora) and m + c == int(self.tempMin) and m == valueM and s == valueS+1 and int(self.tempMin) == 5 and iniciaCont == 2:
                    print('Parte 2 B')
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                    
                #Condição responsável por verificar a cada segundo quantos minutos falta
                elif h == int(self.tempHora) and m + c == int(self.tempMin) and int(self.tempMin) == 5 :
                    
                    for i in range(1,6):
                        if i + m == int(self.tempMin):
                            self.mensag['text'] = 'Resta '+str(i)+' Minuto'
                
                #Se a hora for == 1 e os minutos programado for > ou == 6 ex: (01:06:00)
                if h == int(self.tempHora) and c == 5 and m + c == int(self.tempMin) and s == 0 and int(self.tempMin) >=6 and int(self.tempMin) <= 59 or h == int(self.tempHora) and m + c == int(self.tempMin) and m == valueM and s == valueS+1 and int(self.tempMin) >= 6 and int(self.tempMin) <= 59 and iniciaCont == 2:
                    print('Parte 3 B')
                    telaVermelha2()
                    self.mensag2 = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag2.place(x=160, y=400)
                    self.ativ = 1
                
                #Condição responsável por verificar a cada segundo quantos minutos falta
                elif h == int(self.tempHora) and m + c == int(self.tempMin) and int(self.tempMin) >= 6:
                    
                    for i in range(0,6):
                        if i + m == int(self.tempMin):
                            self.mensag2['text'] = 'Resta '+str(i)+' Minuto'
                     
        elif int(self.tempHora) == 0:
            
            #Caso a OS seja despausada pela janela de OS Pendentes, onde parâmetro de iniciaCont == 2
            if iniciaCont == 2:
                
                '''Evitando conflito caso número pausado for == 59, pois ao inciar contagem já soma +1 então daria 60
                e a verificação de minutos restantes falharia, com esta condição verifica antes se os segundos pausados é igual 59
                se for igual a 59 recebe -1, para dar 0 como em um relógio normal ao terminar em 59 volta a ser 0'''
                if self.seguInit == '59':
                    valueS = -1
                    valueM = int(self.minuInit) + 1
                    if valueM == 60:
                        valueM = 0
                #Senão continuar a receber +1 normalemnte
                else:
                    valueS = int(self.seguInit)
                    valueM = int(self.minuInit)
            elif iniciaCont == 1:
                valueS = 0
                valueM = 0
            
            #Verificando se resta 5 minutos antes do tempo acabar, caso for verdade acender tela vermelha e exibir mensagem
            for c in range(1, 6):
                
                #Verificando se o tempo definido se encaixa entre >= 0 e <= 5, caso seja irá criar o objeto com a mensagem
                if m + c == int(self.tempMin) and m == 0 and s == 1 and int(self.tempMin) <= 5 and iniciaCont == 1 or m + c == int(self.tempMin) and m == valueM and s == valueS+1 and int(self.tempMin) <= 5 and iniciaCont == 2:
                    print('Parte 1 C')
                    telaVermelha2()
                    self.mensag = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag.place(x=160, y=400)
                    self.ativ = 1
                
                #Condição que ficará responsável de atualizar o tempo depois que o objeto com a mensagem for criada
                elif m + c == int(self.tempMin) and int(self.tempMin) <= 5:

                    for i in range(1,6):
                        if i + m == int(self.tempMin):
                            self.mensag['text'] = 'Resta '+str(i)+' Minuto'

                #Verificando se o tempo definido se encaixa entre >= 6 e <= 59, caso seja irá criar o objeto com a mensagem
                if c == 5 and m + c == int(self.tempMin) and s == 0 and int(self.tempMin) >= 6 and int(self.tempMin) <= 59 or m + c == int(self.tempMin) and m == valueM and s == valueS+1 and int(self.tempMin) >= 6 and int(self.tempMin) <= 59 and iniciaCont == 2:
                    print('Parte 2 C')
                    telaVermelha2()
                    self.mensag2 = Label(self.frameRight, text='Resta '+str(c)+' Minuto', bg='red', fg='white', font=('F25 Bank Printer', 20, 'bold'))
                    self.mensag2.place(x=160, y=400)
                    self.ativ = 1
                
                #Condição que ficará responsável de atualizar o tempo depois que o objeto com a mensagem for criada
                elif m + c == int(self.tempMin) and int(self.tempMin) >= 6:
                    
                    for i in range(1,6):
                        if i + m == int(self.tempMin):
                            self.mensag2['text'] = 'Resta '+str(i)+' Minuto'
                            
        if self.ativ == 1:
            self.ativaMensagem = 2
        
        #Verificando se o tempo cronômetrado é igual ao tempo programado, caso for True, o tempo se excederá.
        if s == int(self.tempSeg) and m == int(self.tempMin) and h == int(self.tempHora):
            
            self.tempoEsgotado = True
            
            #Variável que irá habilitar a porta para pode executar a máquina
            #gpio.output(24, gpio.LOW)
            
            if self.ativaMensagem == 2 and int(self.tempMin) >= 6:
                self.mensag2.destroy()
            
            elif int(self.tempMin) <= 5:
                self.mensag.destroy()
            
                    
            if self.chaveTempExtra >= 1:
                self.tempExtraGastoA += int(self.tempHora)
                
                if self.tempExtraGastoB + int(self.tempMin) >= 60:
                    self.tempExtraGastoA += 1
                    self.tempExtraGastoB = (int(self.tempExtraGastoB) + int(self.tempMin)) - 60
                else:
                    self.tempExtraGastoB += int(self.tempMin)
                    self.tempExtraGastoC += 0
                
                print(f'Tempo Configurado Para: {self.tempHora }:{self.tempMin}')
                print(f'Hora Extra Gasta 100%: {self.tempExtraGastoA}:{self.tempExtraGastoB}')
                print('')
            
            self.objetos_cores('#870000', 'white')
            self.imagemTempRel.destroy()
            self.botFramePausar.destroy()
            
            self.labFinalizar = Label(self.frameRight, text='Tempo excedido!!',  bg='#870000', fg='white', font=('arial', 25, 'bold'))
            self.labFinalizar.place(x=150, y=400)
            
            self.frameBotReabilitar = Frame(self.frameRight, highlightbackground='black', highlightthickness=2)
            self.frameBotReabilitar.place(x=180, y=260)
            
            self.botaoReabilitar = Button(self.frameBotReabilitar, text='REABILITAR', bg='orange', activebackground='orange', fg='white', activeforeground='white', relief='flat', font=('arial', 22, 'bold'), width=12, command = lambda: self.tela_admin(1))
            self.botaoReabilitar.pack()
            
            self.foco = None
            
            self.chaveFinalizar = True
            
        self.seconds['text'] = self.secC
        self.minutes['text'] = self.minuC
        self.hours['text'] = self.houC    
        
        #Amarzenado tempo caso der pausa no cronômetro, os dados serão enviados ao banco para tabela pausa_funcionarios
        self.tempoMarcado = self.houC+':'+self.minuC+':'+self.secC
        
        
        #Sub-função: Caso o usuário tente fechar o programa no X enquanto o mesmo ainda estiver executando, ou quando o tempo estiver esgotado. Porém se ele tiver finalizado a OS ele poderá sair e fechar o programa.
        def close():
            
            #Se o tempoesgotado for == True significa que o tempo esgotou, se chavefinalizar for == False ainda está em operação
            '''if self.tempoEsgotado == True or self.chaveFinalizar == False:

                messagebox.showwarning('Alerta', 'Sistema em Operação.')'''
            
            #Se o tempoesgotado for == False significa que o tempo não esgotou, se chavefinalizar for == True não está mais em operação
            if self.tempoEsgotado == False and self.chaveFinalizar == True and self.tempoPausado == False:
                
                if messagebox.askokcancel(parent=self.janelaOper, title='Alerta', message='Deseja Realmente Sair?'):
                    
                    self.janelaOper.destroy()
                    self.__init__()
            else:
                print('TESTE 2')
                messagebox.showwarning(parent=self.janelaOper, title='Alerta', message='Sistema em Operação.')
            
        self.janelaOper.protocol('WM_DELETE_WINDOW', close)        
        
        
        #Se a chave for false significar que ainda está em operação
        if self.chaveFinalizar == False:
            self.seconds.after(1000, self.botao_iniciar, iniciaCont)

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

    def contagemFinalizada(self):
        '''Função rensponsável por finalizar a contagem, informando
        que o tempo foi atingido dentro do limite.'''
        self.tempoPausado = False
        self.chaveFinalizar = True
        self.osfinalizada = True
        
        #Variável que irá habilitar a porta para pode executar a máquina
        #gpio.output(24, gpio.LOW)
        
        #Mostrando o botão sair ao iniciar operação
        self.frameBotSair.place(x=1180, y=20)
        
        #Se a chaveFinalizar for verdadeira, o cronômetro para com a contagem
        if self.chaveFinalizar == True:
            self.botFrameFinalizar.destroy()
            self.botFramePausar.destroy()
            
            #Se OS foi finalizada enquanto o tempo excedeu, será destruido o label e o botão Reabilitar
            if self.tempoEsgotado == True:
                
                self.frameBotReabilitar.destroy()
                self.labFinalizar.destroy()            
            
            #Se a função de piscar o led estiver ligada ela será desligada com a variável de controle "desligarfuncaoLed"
            if self.ledPiscando == True and self.desligarfuncaoLed == False:
                
                self.desligarfuncaoLed = True
                self.ledPiscando = False
            
            #Ligando todos as portas com os leds, informando que a máquina está liberada
            #gpio.output(8, gpio.HIGH)
            #gpio.output(12, gpio.HIGH)
            #gpio.output(18, gpio.HIGH)
            
            corJanela = self.frameRight['bg']
            self.labFinalizar =  Label(self.frameRight, text='Operação Finalizada!',  bg=corJanela, fg='white', font=('arial', 25, 'bold'))
            self.labFinalizar.place(x=120, y=160)
            
            #Pegando a hora atual em que o processo foi finalizado
            time = datetime.now().time().strftime('%H:%M:%S')
            
            #Atribuindo a Hora Final atual e a Data Final atual nas respectivas variáveis
            horaFinal = time
            dateFinal = datetime.now().date().strftime('%d/%m/%Y')
            
            #Se self.chaveTempExtra for 0, então não houve adcionamento de tempo extra
            if self.chaveTempExtra == 0:
                
                #Formatando tempo gasto e o tempo extra caso não foi feito o requerimento de tempo extra
                self.tempGasto = self.houC+':'+self.minuC+':'+self.secC
                self.tempExtraGasto = '00:00:00'
                
            else:
                
                #Adcionando o próprio valor programado ao tempGasto
                self.tempGasto = self.backup
            
                if self.tempExtraGastoB + int(self.minuC) >= 60:
                    self.tempExtraGastoA += 1
                    self.tempExtraGastoB = (int(self.tempExtraGastoB) + int(self.minuC)) - 60
                else:
                    self.tempExtraGastoA += int(self.houC)
                    self.tempExtraGastoB += int(self.minuC)
                    self.tempExtraGastoC = int(self.secC)
                
                #Adcionando o tempo extra gasto e formatando através de uma função
                self.tempExtraGasto = self.transformar_tempo_decimal(self.tempExtraGastoA, self.tempExtraGastoB, self.tempExtraGastoC)
                
            #Botão caso o operado queira realizar outra S.O
            self.frameBotReiniciar = Frame(self.frameRight, highlightbackground='black', highlightthickness=2)
            self.frameBotReiniciar.place(x=187, y=230)
            
            self.botReiniciar = Button(self.frameBotReiniciar, text='NOVO.OS', bg='#035700', fg='white', activebackground='#035700', activeforeground='white', relief='flat', font=('arial', 20, 'bold'), width=12, command = lambda: self.nova_tela_operacao())
            self.botReiniciar.pack()
            
            
            #Enviando todos os dados ao banco
            try:
                self.cursorServer.execute('use empresa_funcionarios')
                self.cursorServer.execute("insert into monitoria_funcionarios VALUES('id','"
                                    +str(self.operador)+"','"
                                    +str(self.user)+"','"
                                    +str(self.horaLogin)+"','"
                                    +str(self.horaInicial)+"','"
                                    +str(self.dateInicial)+"','"
                                    +str(horaFinal)+"','"
                                    +str(dateFinal)+"','"
                                    +self.tempGasto+"','"
                                    +str(self.tempProg)+"','"
                                    +self.numOS+"','"
                                    +self.codP+"','"
                                    +self.numOper+"','"
                                    +str(self.tempExtraGasto)+"','"
                                    +str(self.chaveTempExtra)+"','"
                                    +self.tempOperando+"','"
                                    +self.tipo+"')")
                                    
                self.bancoServer.commit()
                
                messagebox.showinfo(parent=self.janelaOper, title='DATABASE SERVER', message='O.S Finalizada! Operação salva.')
                
            #Excessão caso ocorra de não conseguir salvar
            except Exception as erro:
                
                if messagebox.showerror(parent=self.janelaOper, title='06-Error-Servidor', message='06-Error: Não acesso ao servidor.'):
            
                    try:
                        
                        self.cursorLocal.execute("insert into OS_Finalizadas VALUES(NULL,'"
                                        +str(self.operador)+"','"
                                        +str(self.user)+"','"
                                        +str(self.horaLogin)+"','"
                                        +str(self.horaInicial)+"','"
                                        +str(self.dateInicial)+"','"
                                        +str(horaFinal)+"','"
                                        +str(dateFinal)+"','"
                                        +self.tempGasto+"','"
                                        +str(self.tempProg)+"','"
                                        +self.numOS+"','"
                                        +self.codP+"','"
                                        +self.numOper+"','"
                                        +str(self.tempExtraGasto)+"','"
                                        +str(self.chaveTempExtra)+"','"
                                        +self.tempOperando+"','"
                                        +self.tipo+"')")
                        
                        self.bancoLocal.commit()
                        
                        messagebox.showinfo(parent=self.janelaOper, title='DATABASE LOCAL', message='O.S Finalizada! Operação salva.')
                        
                    except:
                        messagebox.showerror(parent=self.janelaOper, title='06-Error-Local', message='06-Error: Não acesso a Database Local.')

    def tentativa_pausar(self):
        
        def ok():
            if marcado1.get() == 1 or marcado2.get() == 1 or marcado3.get() == 1 or marcado4.get() == 1 or marcado5.get() == 1:
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
                    
                if marcado4.get() == 0:
                    mot4['state'] = DISABLED
                else:
                    self.resultPausa = 'Intervalo Rápido'
                
                if marcado5.get() == 0:
                    mot5['state'] = DISABLED
                else:
                    self.resultPausa = 'Falta Matéria Prima'
                    
            else:
                mot1['state'] = ACTIVE
                mot2['state'] = ACTIVE
                mot3['state'] = ACTIVE
                mot4['state'] = ACTIVE
                mot5['state'] = ACTIVE
                self.resultPausa = ''
        
        
        self.janelaPause = Toplevel()
        self.janelaPause.title('Relatório de Pausa')
        self.janelaPause.resizable(False, False)
        self.janelaPause.configure(background='white')
        
        sistemaOperacional = system()
        if sistemaOperacional == 'Windows':
            self.janelaPause.iconbitmap('img/multimoldes-icon.ico')

        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(600, 600, self.janelaPause)
        
        motivo = Label(self.janelaPause, text='Motivo de Pausa:', font=('arial', 25, 'bold'), bg='white', fg='#3e8e94')
        motivo.place(x=20, y=20)
        
        marcado1 = IntVar()
        mot1 = Checkbutton(self.janelaPause, text='Horário de Almoço', variable=marcado1, activebackground='white', activeforeground='#3e8e94', bg='white', fg='#3e8e94', command=ok, font=('arial',18,'bold'))
        mot1.place(x=30, y=120)
        
        marcado2 = IntVar()
        mot2 = Checkbutton(self.janelaPause, text='Outra OS', variable=marcado2, command=ok, font=('arial',18,'bold'), activebackground='white', activeforeground='#3e8e94', bg='white', fg='#3e8e94')
        mot2.place(x=30, y=200)                
        
        marcado3 = IntVar()
        mot3 = Checkbutton(self.janelaPause, text='Final de Expediente', variable=marcado3, command=ok, font=('arial',18,'bold'), activebackground='white', activeforeground='#3e8e94', bg='white', fg='#3e8e94')
        mot3.place(x=30, y=280)
        
        marcado4 = IntVar()
        mot4 = Checkbutton(self.janelaPause, text='Intervalo Rápido', variable=marcado4, command=ok, font=('arial',18,'bold'), activebackground='white', activeforeground='#3e8e94', bg='white', fg='#3e8e94')
        mot4.place(x=30, y=350)
        
        marcado5 = IntVar()
        mot5 = Checkbutton(self.janelaPause, text='Parada (Falta de Matéria Prima)', variable=marcado5, command=ok, font=('arial', 18, 'bold'), activebackground='white', activeforeground='#3e8e94', bg='white', fg='#3e8e94')
        mot5.place(x=30, y=430)
        
        confirmar = Button(self.janelaPause, text='Confirmar', bg='#3e8e94', activebackground='#3e8e94', fg='white', activeforeground='white', border=0, relief='flat', font=('arial', 20), width=10, command = lambda:self.analisar_pausa())
        confirmar.place(x=210,y=520)
        
        self.janelaPause.transient(self.janelaOper)
        self.janelaPause.focus_force()
        self.janelaPause.grab_set()
                
        self.janelaPause.mainloop()
        
    def analisar_pausa(self):        
        
        if self.tempoEsgotado == True:

            messagebox.showerror(parent=self.janelaPause, title='Alerta', message='Tempo Esgotado. Impossível Pausar!')
            self.janelaPause.destroy()
        
        elif self.resultPausa == '':
            
            if messagebox.showerror(parent=self.janelaPause, title='Alerta', message='Marque uma Opção!'):
                self.janelaPause.lift()
                self.janelaPause.focus_force()
            
        else:
            self.contagem_pausada()
        
    def contagem_pausada(self):
        
        self.janelaPause.destroy()
        
        corTela = self.frameTop['bg']
        
        self.tempoPausado = True
        self.chaveFinalizar = True
        self.botFrameFinalizar.destroy()
        self.botFramePausar.destroy()
        
        #Mostrando o botão sair ao iniciar operação
        self.frameBotSair.place(x=1180, y=20)
        
        #Variável que irá habilitar a porta para pode executar a máquina (True=Ligado, False=Desligado)
        #gpio.output(24, gpio.LOW)
        
        #Se a função de piscar o led estiver ligada ela será desligada com a variável de controle "desligarfuncaoLed"
        if self.ledPiscando == True and self.desligarfuncaoLed == False:
            
            self.desligarfuncaoLed = True
            self.ledPiscando = False
            
        #Ligando todos as portas com os leds, informando que a máquina está liberada
        #gpio.output(8, gpio.HIGH)
        #gpio.output(12, gpio.HIGH)
        #gpio.output(18, gpio.HIGH)
                
        
        #Capturando a hora inicial e a data atual em que o modo pause foi iniciado, em seguida inserir no banco de dados
        horaPause = datetime.now().time().strftime('%H:%M:%S')
        datePause = datetime.now().date().strftime('%d/%m/%Y')
        
        #Se self.chaveTempExtra for 0, então não houve adcionamento de tempo extra
        if self.chaveTempExtra == 0:
            
            #Formatando tempo gasto e o tempo extra caso não foi feito o requerimento de tempo extra
            self.tempGasto = self.houC+':'+self.minuC+':'+self.secC
            self.tempExtraGasto = '00:00:00'
        
        #Portando se o requerimento de tempo extra for adicionado o tempo gasto será excedido com seu próprio valor
        else:
            
            #Adcionando o próprio valor programado ao tempGasto
            self.tempGasto = self.backup
            
            if self.tempExtraGastoB+ int(self.minuC) >= 60:
                self.tempExtraGastoA += 1
                self.tempExtraGastoB -= (int(self.tempExtraGastoB) + int(self.minuC)) - 60
            else:
                self.tempExtraGastoA += int(self.houC)
                self.tempExtraGastoB += int(self.minuC)
                self.tempExtraGastoC = int(self.secC)
            
            #Adcionando o tempo extra gasto e formatando através de uma função
            self.tempExtraGasto = self.transformar_tempo_decimal(self.tempExtraGastoA, self.tempExtraGastoB, self.tempExtraGastoC)
            
        self.botFrameRetomar = Frame(self.frameRight, highlightbackground='black', highlightthickness=2)
        self.botFrameRetomar.place(x=172, y=220)
        
        self.botDespausar = Button(self.botFrameRetomar, text='RETOMAR.OS', bg='#035700', fg='white', activebackground='#035700', activeforeground='white', relief='flat', font=('arial', 22, 'bold'), width=13, command = lambda: self.contagem_despausar(1))
        self.botDespausar.pack()            
            
        try:
            self.cursorServer.execute("insert into pausa_funcionarios VALUES('id','"
                                      +str(self.operador)+"','"
                                      +self.user+"','"
                                      +self.codP+"','"
                                      +self.numOper+"','"
                                      +self.numOS+"','"
                                      +self.resultPausa+"','"
                                      +horaPause+"','"
                                      +str(datePause)+"','0','0','"
                                      +self.tempoMarcado+"','"
                                      +self.tempGasto+"','"
                                      +self.tempExtraGasto+"','"
                                      +str(self.chaveTempExtra)+"','"
                                      +str(self.UltimoTempAdd)+ "','"
                                      +str(self.tempProg)+"','"
                                      +corTela+"','"
                                      +str(self.horaLogin)+"','"
                                      +str(self.horaInicial)+"','"
                                      +str(self.dateInicial)+"','"
                                      +self.tempOperando+"','"
                                      +self.tipo+"')")
            
            self.bancoServer.commit()
            
            messagebox.showinfo(parent=self.janelaOper, title='DATABASE SERVER', message='O.S Pausada! Operação salva.')
            
        except Exception as erro:
            
            self.cursorLocal.execute("insert into OS_Pausadas VALUES('id','"
                                     +str(self.operador)+"','"
                                     +self.user+"','"
                                     +self.codP+"','"
                                     +self.numOper+"','"
                                     +self.numOS+"','"
                                     +self.resultPausa+"','"
                                     +horaPause+"','"
                                     +str(datePause)+"','0','0','"
                                     +self.tempoMarcado+"','"
                                     +self.tempGasto+"','"
                                     +self.tempExtraGasto+"','"
                                     +str(self.chaveTempExtra)+"','"
                                     +str(self.UltimoTempAdd)+ "','"
                                     +str(self.tempProg)+"','"
                                     +corTela+"','"
                                     +str(self.horaLogin)+"','"
                                     +str(self.horaInicial)+"','"
                                     +str(self.dateInicial)+"','"
                                     +self.tempOperando+"','"
                                     +self.tipo+"')")
            
            self.bancoLocal.commit()
            
            messagebox.showinfo(parent=self.janelaOper, title='DATABASE LOCAL', message='O.S Pausada! Operação salva.')
    
    def contagem_despausar(self, despause):
        try:
            
            #Capturando a hora e a data atual em que a OS foi despausada, em seguida inserir no banco de dados
            horaRetomada = datetime.now().time().strftime('%H:%M:%S')
            dateFinal = datetime.now().date().strftime('%d/%m/%Y')

            #Atualizando Banco de Dados Local com data e hora retomada após função despausar for invocada
            self.cursorLocal.execute("update OS_Pausadas set DataRetomada = '"+dateFinal+"' where CPF = '"+self.user+"' and CodigoPeca = '"+self.codP+"' and OS = '"+self.numOS+"' and DataRetomada = 0 ")
            self.bancoLocal.commit()
            
            self.cursorLocal.execute("update OS_Pausadas set HoraRetomada = '"+horaRetomada+"' where CPF = '"+self.user+"' and CodigoPeca = '"+self.codP+"' and OS = '"+self.numOS+"' and HoraRetomada = 0 ")
            self.bancoLocal.commit()
            
            #Atualizando Banco de Dados Server com data e hora retomada após função despausar for invocada
            self.cursorServer.execute("update pausa_funcionarios set DataRetomada = '"+dateFinal+"' where CPF = '"+self.user+"' and CodigoPeca = '"+self.codP+"' and OS = '"+self.numOS+"' and DataRetomada = 0 ")
            self.bancoServer.commit()
            
            self.cursorServer.execute("update pausa_funcionarios set HoraRetomada = '"+horaRetomada+"' where CPF = '"+self.user+"' and CodigoPeca = '"+self.codP+"' and OS = '"+self.numOS+"' and HoraRetomada = 0 ")
            self.bancoServer.commit()
            
        #Excessão carro algum erro ocorra um mensagebox aparecerá informando o corrido
        except Exception as erro:
            print(erro)
            return messagebox.showerror(parent=self.janelaOper, title='08-Error-Servidor', message='08-Error: Não acesso ao servidor.')
        
        #Destruindo botão despausar devido a função despausar foi invocada
        self.botFrameRetomar.destroy()
        
        #Enquanto a chaveFinalizar estiver True significa que o tempo está parado
        if self.chaveFinalizar == True:
            
            #com a função despausar invocada, chaveFinalizar fica True e o tempo pode continuar cronometrando
            self.chaveFinalizar = False
            
            #Variável que irá habilitar a porta para pode executar a máquina
            #gpio.output(24, gpio.HIGH)
            
            if self.chaveTempExtra != 0:
                
                self.desligarfuncaoLed = False
                self.ledPiscando = False
                self.Led_OFF_ON = 0
                
                #Ligando todos as portas com os leds, informando que a máquina está liberada
                #gpio.output(8, gpio.LOW)
                #gpio.output(12, gpio.LOW)
                #gpio.output(18, gpio.LOW)
                
                #Invocando função responsável por determinar funções aos Leds
                self.piscar_led()
            
            #Se o parâmetro passado for 1: irá criar antecipadamente os botões FINALIZAR E PAUSAR
            if despause == 1:
                
                #Escondendo o botão sair ao iniciar operação
                try:
                    self.frameBotSair.place_forget()
                except: pass
                
                #Criando frame para fazer uma borda pro botão botFinalizar
                self.botFrameFinalizar = Frame(self.frameRight, highlightbackground='black', highlightthickness=2)
                self.botFrameFinalizar.place(x=182, y=160)            
                
                #Criando botão Finalizar para concluir a OS
                self.botFinalizar = Button(self.botFrameFinalizar, text='FINALIZAR.OS', bg='#b30000', activebackground='#b30000', fg='white', activeforeground='white', relief='flat', font=('arial', 22, 'bold'), width=12, command = lambda: self.contagemFinalizada())
                self.botFinalizar.pack()
                
                #Criando frame para fazer uma borda pro botão botPausar
                self.botFramePausar = Frame(self.frameRight, highlightbackground='black', highlightthickness=2)
                self.botFramePausar.place(x=182, y=260)            
                
                #Criando botão Pausar para parar a OS 
                self.botPausar = Button(self.botFramePausar, text='PAUSAR.OS', bg='#035700', activebackground='#035700', fg='white', activeforeground='white', relief='flat', font=('arial', 22, 'bold'), width=12, command = lambda: self.tentativa_pausar())
                self.botPausar.pack()
                
                #Recebendo cor de fundo da tela para acender o led respectivo, ou se for tempo extra irá piscar.
                corTela = self.frameRight['bg']
                self.objetos_cores(corTela, 'white')
            
            if despause == 2:
                
                #Buscando dados no banco com o id selecionado 
                self.cursorServer.execute('select Hora_Login, Hora_Inicial, Data_Inicial from pausa_funcionarios where id ='+self.tuplaSelect[0])
                valido = self.cursorServer.fetchall()
                
                #Armazenando os dados capturados nas variáveis
                self.horaLogin = valido[0][0]
                self.horaInicial = valido[0][1]
                self.dateInicial = valido[0][2]
            
            #Varável que indica quando cronômetro parar, se é parou porque finalizou ou por pausa, usada nas funções mais abaixo
            self.tempoPausado = False
            
            #Invocando função para iniciar a contagem e monitoração
            self.botao_iniciar(2)         
    
    def nova_tela_operacao(self):
        '''Função responsável por apertar o botão "NOVO.OS" após finalizar a 
        operação, caso o operador deseje executar uma nova tarefa'''
        
        self.janelaOper.destroy()
        self.tela_de_operacao()
        
    def sairTela(self):
        '''Função responsavel por ao apertar o botão "Sair" no lado superior
        direito o cronômetro estiver em contagem, abrirá automaticamente um 
        alerta informando que o programa ainda está sendo executado, e só 
        permitira sair ao encerrar a operação, '''
            
        #Se a chaveFinalizar for True e osfinalizada for True significa que o operário conclui/finalizou a peça e poderá sair
        if self.chaveFinalizar == True and self.osfinalizada == True:
            
            if messagebox.askokcancel(parent=self.janelaOper, title='Alerta', message='Deseja Realmente Sair?'):
                
                self.janelaOper.destroy()
                #self.__init__()
                self.janelaFuncio.deiconify()
                self.campoSenha.delete(0, END)
                self.campoLogin.focus_force()

                if self.sistemaOperacional == 'Windows':
                    self.janelaFuncio.state('zoomed')
                else:
                    self.janelaFuncio.attributes('-zoomed', True)

                #Verificando se já existe conexão com banco servidor para enviar dados do banco local se tiver algum
                self.verificar_conexao()
        
        #Se a chaveFinalizar and tempoPausado for True significa que o tempo foi pausado, e operário poderá sair
        elif self.chaveFinalizar == True and self.tempoPausado == True:
            
            if messagebox.askokcancel(parent=self.janelaOper, title='Alerta', message='Deseja Realmente Sair?'):
                
                self.janelaOper.destroy()
                #self.__init__()
                self.janelaFuncio.deiconify()
                self.campoSenha.delete(0, END)
                self.campoLogin.focus_force()

                if self.sistemaOperacional == 'Windows':
                    self.janelaFuncio.state('zoomed')
                else:
                    self.janelaFuncio.attributes('-zoomed', True)                

                #Verificando se já existe conexão com banco servidor para enviar dados do banco local se tiver algum
                self.verificar_conexao()
        
        #Se chaveControle for False e tempoEsgotado for False, poderá sair da janela mesmo tendo confirmado a OS após logar
        elif self.chaveControle == False and self.tempoEsgotado == False:
            
            if messagebox.askokcancel(parent=self.janelaOper, title='Alerta', message='Deseja Realmente Sair?'):
                
                self.janelaOper.destroy()
                #self.__init__()
                self.janelaFuncio.deiconify()
                self.campoSenha.delete(0, END)
                self.campoLogin.focus_force()

                if self.sistemaOperacional == 'Windows':
                    self.janelaFuncio.state('zoomed')
                else:
                    self.janelaFuncio.attributes('-zoomed', True)

                #Verificando se já existe conexão com banco servidor para enviar dados do banco local se tiver algum
                self.verificar_conexao()
        
        #Senão significa que o cronômetro ainda está em execução
        else:
            
            messagebox.showwarning(parent=self.janelaOper, title='Alerta', message='Sistema em Operação.')


class AplicacaoFront(AplicacaoBack):
   
    def __init__(self):
        
        self.janelaFuncio = Tk()
        self.janelaFuncio.title('Login Funcionário')
        self.janelaFuncio.configure(background='white')
        self.janelaFuncio.minsize(500, 400)
        
        self.sistemaOperacional = system()
        
        if self.sistemaOperacional == 'Windows':
            self.janelaFuncio.iconbitmap('img/multimoldes-icon.ico')
            self.janelaFuncio.state('zoomed')
        else:
            self.janelaFuncio.attributes('-zoomed', True)
        
        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(900, 600, self.janelaFuncio)
        
        #Adcionando Logo na Janela de Funcionário
        self.imgFun = PhotoImage(file="img/logo-multimoldes.png")
        
        self.frameLogin = Frame(self.janelaFuncio, width=500, height=600, bg='white')
        self.frameLogin.pack()

        self.imagemPricipalFun = Label(self.frameLogin, image=self.imgFun, bg='white')
        self.imagemPricipalFun.place(relx=0.400, rely=0.05)

        self.labelLogin = Label(self.frameLogin, text='Usuário', bg='white', fg='#3e8e94', font=('arial',22,'bold'))
        self.labelLogin.place(relx=0, rely=0.440)

        #Função local que verificará os campos de login colocando limites de capacidade
        
        def limite_campos_login(*args):
            
            varCPF = cLogin.get()
            varSenha = cSenha.get()
            
            if len(varCPF) > 11:
                cLogin.set(varCPF[:-1])
            if not varCPF.isnumeric():
                cLogin.set(varCPF[:-1])
            
            if len(varSenha) > 8:
                cSenha.set(varSenha[:-1])
            if not varSenha.isnumeric():
                cSenha.set(varSenha[:-1])
        
        #Configurando caracteres quando estiverem inserido nos campos
        
        cLogin = StringVar()
        cLogin.trace('w', limite_campos_login)
        
        cSenha = StringVar()
        cSenha.trace('w', limite_campos_login)
        
        self.campoLogin = Entry(self.frameLogin, width=26, font=('arial', 16), textvariable=cLogin, border=2, relief=GROOVE)
        self.campoLogin.place(relx=0.25, rely=0.450)
        self.campoLogin.focus_force()
        self.campoLogin.bind("<Return>", self.confirmar_tela_funcionario)

        self.labelSenha = Label(self.frameLogin, text='Senha', bg='white', fg='#3e8e94', font=('arial',22,'bold'))
        self.labelSenha.place(relx=0, rely=0.540)

        self.campoSenha = Entry(self.frameLogin, width=13, show='l', font=('wingdings', 16, 'bold'), textvariable=cSenha, border=2, relief=GROOVE)
        self.campoSenha.place(relx=0.25, rely=0.550)
        self.campoSenha.bind("<Return>", self.confirmar_tela_funcionario)

        self.botao = Button(self.frameLogin, text='Confirmar', fg='white', activeforeground='white', bg='#3e8e94', activebackground='#3e8e94', border=0, font=('arial', 18, 'bold'), width=10, command = lambda: self.confirmar_tela_funcionario(self.confirmar_tela_funcionario))
        self.botao.place(relx=0.370, rely=0.700)
        self.botao.bind("<Return>", self.confirmar_tela_funcionario)
        
        self.bancoConect = False
        
        self.bancoCriado = False
        
        threading.Thread(target=self.verifica_banco,).start()
        
        #Chamando função para conectar-se ao banco de dados local
        self.conection_database_local()
        
        #Verificando se já existe conexão com banco servidor para enviar dados do banco local se tiver algum
        threading.Thread(target=self.verificar_conexao,).start()

        #Configurando portas da GPIO do RESPBERRY PI para saída dos LED'S de automação
        #gpio.setmode(gpio.BOARD)
        #gpio.setup(8, gpio.OUT)
        #gpio.setup(12, gpio.OUT)
        #gpio.setup(18, gpio.OUT)
        #gpio.setup(40, gpio.OUT)
        
        #Ligando todos as portas com os leds, informando que a máquina está liberada
        #gpio.output(8, gpio.HIGH)
        #gpio.output(12, gpio.HIGH)
        #gpio.output(18, gpio.HIGH)
        
        #Configurando porta da GPIO do RESPBERRY PI para entrada de corrente
        #gpio.setup(32, gpio.IN)        
        
        #Porta que habilitará a máquina à operar, só irá ligar quando o operador iniciar 
        #gpio.output(40, gpio.LOW)
        
        self.foco = None
        
        self.janelaFuncio.mainloop()
        
    def tela_admin(self, botao):
                    
        self.janelaADM = Toplevel()
        self.janelaADM.title('Login Administração')
        self.janelaADM.resizable(False, False)
        self.janelaADM.configure(background='white')
        
        sistemaOperacional = system()
        if sistemaOperacional == 'Windows':
            self.janelaADM.iconbitmap('img/multimoldes-icon.ico')
        
        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(600, 600, self.janelaADM)
        
        #Adcionando Logo na Janela ADM
        imgAdm = PhotoImage(file="img/admin.png")

        imagemPricipalAdm = Label(self.janelaADM, image=imgAdm, bg='white')
        imagemPricipalAdm.place(x=240,y=10)

        admLabelPrincipal = Label(self.janelaADM, text='Senha', fg='#282873', font=('arial', 18, 'bold'), bg='white')
        admLabelPrincipal.place(x=75,y=263)

        self.valorBotao = botao

        self.admSenhaPrincipal = Entry(self.janelaADM, width=12, show='l', font=('wingdings', 15, 'bold'), border=2, relief=GROOVE)
        self.admSenhaPrincipal.place(x=170,y=266)
        self.admSenhaPrincipal.focus_force()
        self.admSenhaPrincipal.bind("<Return>", self.transicao)
        
        self.labelError2 = Label(self.janelaADM, bg='white', fg='#bf0606', width=30, font=('arial', 12))
        self.labelError2.place(relx=0.290, rely=0.495)
        
        admBotaoPrincipal = Button(self.janelaADM, text='Continuar', bg='#282873', activebackground='#282873', fg='white', activeforeground='white', border=0, font=('arial', 18), width=10, command = lambda: self.verificar_adm(botao, self.admSenhaPrincipal.get())) ##0c0052
        admBotaoPrincipal.place(x=235,y=420)
        admBotaoPrincipal.bind("<Return>", self.transicao)
        
        self.janelaADM.transient(self.janelaOper)
        self.janelaADM.focus_force()
        self.janelaADM.grab_set()        
        
        self.janelaADM.mainloop()
    
    def tempo_extra(self):
    
        def fechar_tempo_extra():
            self.janelaTempExtra.destroy()
            self.foco = None
        
        self.janelaTempExtra = Toplevel()
        self.janelaTempExtra.title('Tela Operativa')
        self.janelaTempExtra.configure(background='#870000')
        self.janelaTempExtra.geometry('550x350+200+100')
        self.janelaTempExtra.resizable(False, False)
        self.janelaTempExtra.protocol('WM_DELETE_WINDOW', fechar_tempo_extra)

        sistemaOperacional = system()
        if sistemaOperacional == 'Windows':
            self.janelaTempExtra.iconbitmap('img/multimoldes-icon.ico')
        
        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(550, 350, self.janelaTempExtra)
        
        lt = Label(self.janelaTempExtra, text='Tempo Extra', font=('arial',20,'bold'), bg='#870000', fg='white')
        lt.place(x=195, y=10)
        
        lh = Label(self.janelaTempExtra, text='Horas:', font=('arial',20,'bold'), bg='#870000', fg='white')
        lh.place(x=70, y=135)
        
        #Função local que verificará os campos colocando limites de capacidade
        
        def limite_campos_temp_extra(*args):
            
            varll = cll.get()
            varmm = mm.get()
            
            if len(varll) > 2:
                cll.set(varll[:-1])
            if not varll.isnumeric():
                cll.set(varll[:-1])
        
            if len(varmm) > 2:
                mm.set(varmm[:-1])
            if not varmm.isnumeric():
                mm.set(varmm[:-1])
        
        #Configurando caracteres quando estiverem inserido nos campos
        
        cll = StringVar()
        cll.trace('w', limite_campos_temp_extra)
        
        mm = StringVar()
        mm.trace('w', limite_campos_temp_extra)
        
        self.ll = Entry(self.janelaTempExtra, font=('arial',15,'bold'), textvariable=cll, width=5)
        self.ll.place(x=170, y=140)
        self.ll.focus_force()
        self.ll.bind('<Return>', self.verificar_tempo_extra)
        
        lm = Label(self.janelaTempExtra, text='Minutos:', font=('arial',20,'bold'), bg='#870000', fg='white')
        lm.place(x=270,y=135)
        
        self.mm = Entry(self.janelaTempExtra, font=('arial',15,'bold'), textvariable=mm, width=5)
        self.mm.place(x=400,y=140)
        self.mm.bind('<Return>', self.verificar_tempo_extra)
        
        bc = Button(self.janelaTempExtra, text='Confirmar', font=('arial',15,'bold'), bg='orange', activebackground='orange', fg='white', activeforeground='white', command = lambda: self.verificar_tempo_extra(self.verificar_tempo_extra))
        bc.place(x=225,y=260)
        bc.bind('<Return>', self.verificar_tempo_extra)
        
        self.janelaTempExtra.transient(self.janelaOper)
        self.janelaTempExtra.grab_set()
        
        self.janelaTempExtra.mainloop()

    def tela_de_operacao(self):

        self.janelaOper = Toplevel()
        self.janelaOper.configure(background='black')
        self.janelaOper.resizable(False, False)
        self.janelaOper.attributes('-fullscreen', True)
        
        #Obtendo medidas da tela
        largura = self.janelaOper.winfo_screenwidth()
        altura = self.janelaOper.winfo_screenheight()
        
        #self.janelaOper.geometry(str(largura)+'x'+str(altura))
        self.janelaOper.geometry(str(largura)+'x'+str(altura))
        
        #Centralizando janela
        self.centraliza_tela(largura, altura, self.janelaOper)
        
        #Configurando a largura dos frames esquerdo e direito
        largLeft = largura / 1.6
        largRight = largura / 2.324

        #Configurando a Altura dos frames esquerdo e direito
        altTop = altura / 5.0
        altLeft = altura / 1.261
        altRight = altura / 1.261
        
        #(Tela Operativa) - FRAMES DA TELA DE OPERAÇÃO

        self.frameTop = Frame(self.janelaOper, bg='#135565',highlightthickness=3,highlightcolor='black') #135565
        self.frameTop.config(highlightbackground='black')
        self.frameTop.place(relx=0, rely=0, relwidth=1, relheight=0.200)
        
        self.frameLeft = Frame(self.janelaOper, bg='#135565', highlightthickness=3,highlightcolor='black')
        self.frameLeft.config(highlightbackground='black')
        self.frameLeft.place(relx=0, rely=0.200, relwidth=0.625, relheight=0.800)

        self.frameRight = Frame(self.janelaOper, bg='#135565',highlightthickness=3,highlightcolor='black') ##c4c0c0
        self.frameRight.config(highlightbackground='black')
        self.frameRight.place(relx=0.625, rely=0.200, relwidth=0.375, relheight=0.800)
        

        #(Tela Operativa) - LABELS E CAMPOS DE ENTRADA DA TELA DE OPERAÇÃO - DADOS DO OPERADOR 

        self.operadorNome = Label(self.frameTop, text='Operador:', font=('arial', 15,'bold'), fg='white', bg='#135565')
        self.operadorNome.place(relx=0.010, rely=0.130)
        
        self.operadorAlto = self.operador.upper()
        
        self.operadorNomeUser = Label(self.frameTop, text=self.operadorAlto,font=('arial', 15,'bold'), fg='white', bg='#135565')
        self.operadorNomeUser.place(relx=0.100, rely=0.130)

        self.horaInicialLb = Label(self.frameTop, text='Horário de Login:', font=('arial', 15,'bold'), fg='white', bg='#135565')
        self.horaInicialLb.place(relx=0.010, rely=0.420)
        
        self.horaAtualUser = Label(self.frameTop, text=self.horaLogin, font=('arial', 15,'bold'), fg='black', bg='white')
        self.horaAtualUser.place(relx=0.160, rely=0.420)

        self.multimolde = Label(self.frameTop, text='MULTIMOLDES', font=('play pretend', 40), fg='white', bg='#135565', width=15)
        self.multimolde.place(relx=0.350, rely=0.220)
        
        self.frameBotSair = Frame(self.frameTop, highlightbackground='black', highlightthickness=2, width=50, height=50)
        self.frameBotSair.place(relx=0.920, rely=0.130)
        
        self.sair = Button(self.frameBotSair, text='Sair', font=('arial',14,'bold'), fg='white', bg='red', activebackground='red', activeforeground='white', relief='flat', width=5, command=lambda:self.sairTela())
        self.sair.pack()
        
        #Função local que verificará os campos colocando limites de capacidade

        def limite_campos_operacao(*args):
            
            varOS = cOS.get()
            varPeca = cPeca.get()
            varQuant = cQuant.get()
            varOper = cOper.get()
            
            if len(varOS) > 13:
                cOS.set(varOS[:-1])
            if not varOS.isnumeric():
                cOS.set(varOS[:-1])
            
            if len(varPeca) > 13:
                cPeca.set(varPeca[:-1])
            if not varPeca.isnumeric():
                cPeca.set(varPeca[:-1])
            
            if len(varQuant) > 4:
                cQuant.set(varQuant[:-1])
            if not varQuant.isnumeric():
                cQuant.set(varQuant[:-1])
            
            if len(varOper) > 3:
                cOper.set(varOper[:-1])
            if not varOper.isnumeric():
                cOper.set(varOper[:-1])
        
        #Configurando caracteres quando estiverem inserido nos campos
        
        cOS = StringVar()
        cOS.trace('w', limite_campos_operacao)
        
        cPeca = StringVar()
        cPeca.trace('w', limite_campos_operacao)
        
        cOper = StringVar()
        cOper.trace('w', limite_campos_operacao)
        
        cQuant = StringVar()
        cQuant.trace('w', limite_campos_operacao)
        
        #(Tela Operativa) - LABELS E CAMPOS DE ENTRADA DA TELA DE OPERAÇÃO - FOMULÁRIO

        self.ordemServico = Label(self.frameLeft, text='Ordem de Serviço:', font=('arial', 20, 'bold'), bg='#135565', fg='white')
        self.ordemServico.place(relx=0.075, rely=0.170)
        
        self.campoServico = Entry(self.frameLeft, width=20, font=('arial', 19), textvariable=cOS, bg='white')
        self.campoServico.place(relx=0.455, rely=0.170)
        self.campoServico.focus_force()
        self.campoServico.bind("<Return>", self.confirmarCampos)
        
        self.codigoPeca = Label(self.frameLeft, text='Código da Peça:', font=('arial', 20, 'bold'), bg='#135565', fg='white')
        self.codigoPeca.place(relx=0.110, rely=0.340)
        
        self.campoPeca = Entry(self.frameLeft, width=20, font=('arial', 19), textvariable=cPeca)
        self.campoPeca.place(relx=0.455, rely=0.340)
        self.campoPeca.bind("<Return>", self.confirmarCampos)
        
        self.lbQuantidadePeca = Label(self.frameLeft, text='nº', font=('Arial', 20, 'bold'), bg='#135565', fg='white')
        self.lbQuantidadePeca.place(relx=0.830, rely=0.340)
        
        self.campQuantidadePeca = Entry(self.frameLeft, font=('arial', 19), textvariable=cQuant)
        self.campQuantidadePeca.place(relx=0.880, rely=0.340, relwidth=0.085)
        
        self.checkVazio = PhotoImage(file='img/verificaVazio.png')
        
        self.framenovoOS = Frame(self.frameLeft, bg='#135565', width=110, height=25)
        self.framenovoOS.place(relx=0.445, rely=0.430)
        
        self.novoOS = Label(self.framenovoOS, text='Nova OS', font=('arial',14,'bold'), bg='#135565', fg='white')
        self.novoOS.place(x=0, y=0)
        
        self.novoSelect = Label(self.framenovoOS, image=self.checkVazio, bg='#135565', fg='white')
        self.novoSelect.place(x=88, y=5)
        
        self.frameRetrabalho = Frame(self.frameLeft, bg='#135565', width=170, height=25)
        self.frameRetrabalho.place(relx=0.635, rely=0.430)
        
        self.retrabalhoOS = Label(self.frameRetrabalho,  text='Retrabalhar OS', font=('arial',14,'bold'),bg='#135565', fg='white')
        self.retrabalhoOS.place(x=0, y=0)
        
        self.retrabalhoSelect = Label(self.frameRetrabalho, image=self.checkVazio, bg='#135565', fg='white')
        self.retrabalhoSelect.place(x=148, y=5)
        
        
        self.codigoOperacao = Label(self.frameLeft, text='Operação:', font=('arial', 20, 'bold'), bg='#135565', fg='white')
        self.codigoOperacao.place(relx=0.205, rely=0.510)
        self.campoOperacao = Entry(self.frameLeft, width=20, font=('arial', 19), textvariable=cOper)
        self.campoOperacao.place(relx=0.455, rely=0.510)
        self.campoOperacao.bind("<Return>", self.confirmarCampos)
        
        self.botConfirmar = Button(self.frameLeft, text='Confirmar', fg='white', activebackground='orange', activeforeground='white', border=0, width=10, font=('arial', 15,'bold'), bg='orange', command=lambda:self.confirmarCampos(self.confirmarCampos))
        self.botConfirmar.place(relx=0.455, rely=0.790)
        self.botConfirmar.bind("<Return>", self.confirmarCampos)
        
        #(Tela Operativa) - LABELS QUE IMPRIMEM O CRONÔMETRO - CRONÔMETRO

        self.seconds = Label(self.frameRight, text='00', font=('alarm clock',35, 'bold'), fg=('red'), width=2)
        self.seconds.place(x=328, y=50)
        self.minutes = Label(self.frameRight, text='00', font=('alarm clock',35, 'bold'), fg=('red'), width=2)
        self.minutes.place(x=260, y=50)
        self.hours = Label(self.frameRight, text='00', font=('alarm clock',35, 'bold'), fg=('red'), width=2)
        self.hours.place(x=192, y=50)
        
        logoMarca = PhotoImage(file='img/logoAzul.png')
        
        self.logoMarcaRight = Label(self.frameRight, image=logoMarca, bg='#135565')
        self.logoMarcaRight.place(x=215, y=200)

        '''Chave de controle, responsável de quando ser TRUE, informar que o botão INICIAR iniciou a contagem e em seguida
        destrui-lo fazendo o botão FINALIZAR 0S aparecer'''
        self.chaveControle = False

        '''Chave finalizar, responsável de quando TRUE, informar que o botão FINALIZAR OS foi acionado, e destrui-lo, mostrando um label que o OS foi finalizado.'''
        self.chaveFinalizar = False
        
        '''tempoEsgotado, responsável de quando a janela de pause estiver abertar e o tempo esgotar, não poderá mais pausar'''
        self.tempoEsgotado = False
        self.resultPausa = ''
        
        #Variável responsável por indicar se a função que faz o Led piscar está ativa ou não
        self.ledPiscando = False
        
        #Variável responsável por desligar a função que faz o Led piscar
        self.desligarfuncaoLed = False
        
        #variaveis que tornaram possiveis a contagem do cronômetro
        self.sec = None
        self.minu = None
        self.hou = None     
        
        self.secOperacao = None
        self.minuOperacao = None
        self.houOperacao = None        
        
        self.chaveFinalizar2 = False
        self.chaveControle2 = False
        self.tempoPausado = False
        self.osfinalizada = False
        
        #Variáveis responsáveis caso o "tempo gasto" ultrapasse o "tempo programado"
        self.chaveTempExtra = 0
        self.tempExtraGastoA = 0
        self.tempExtraGastoB = 0
        self.tempExtraGastoC = 0       
        
        self.UltimoTempAdd = 0 
        
        self.bteste = 5
        
        def close():
            
            if self.sec == None:
                
                if messagebox.askokcancel(parent=self.janelaOper, title='Alerta', message='Deseja Realmente Sair?'):
                        
                    self.janelaOper.destroy()
                    self.__init__()
                
        self.janelaOper.protocol('WM_DELETE_WINDOW', close)
        
        
        self.cursorServer.execute("use empresa_funcionarios")
        self.cursorServer.execute("select * from pausa_funcionarios where cpf ="+self.user+" and horaRetomada = 0")
        valido = self.cursorServer.fetchall()
        
        if len(valido) >= 1:
            if messagebox.askyesno(parent=self.janelaOper, title='OS Pendente', message='Você tem OS pendente, Deseja Ver?'):
                self.verificação_de_OS()
        
        self.janelaOper.mainloop()
    
    def verificação_de_OS(self):
        
        #Criando janela e configurando
        self.janelaOsPendente = Toplevel()
        self.janelaOsPendente.title('OS Pausadas')
        self.janelaOsPendente.configure(background='white')
        self.janelaOsPendente.minsize(780, 400)
        
        #Invocando função para centralizar a janela ao centro
        self.centraliza_tela(900, 600, self.janelaOsPendente)
        
        '''#criando um list box onde irá ficar armazenado as OS com pendências
        lista = Listbox(self.janelaOsPendente, font=('arial', 14, 'bold'), width=46)
        lista.pack(side='right', fill='y')
        '''
        
        #titulo central da janela
        titulo = Label(self.janelaOsPendente, text='OS Pendentes', bg='white', fg='#135565', font=('arial', 22, 'bold'))
        titulo.place(relx=0.03, rely=0.05)
        
        #armazenando logo da empresa em uma variável
        image = PhotoImage(file='img/logo-multimoldes.png')
        
        #exibindo label com a imagem já carregada
        logo = Label(self.janelaOsPendente, image=image, bg='white')
        logo.place(relx=0.07, rely=0.3)
        
        #criando lista onde irá capturar as os e numéros de pelas para exibir na list box
        pendente = []
        
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('arial', 12, 'bold'))
        
        style2 = ttk.Style()
        style2.configure('Treeview', font=('arial', 13))
        
        lista = ttk.Treeview(self.janelaOsPendente, column=("1","2","3","4","5","6"), show='headings')
        
        lista.heading("1", text='ID')
        lista.heading("2", text='O.S')
        lista.heading("3", text='Nº de Peça')
        lista.heading("4", text='Operação')
        lista.heading("5", text='Pausado')
        lista.heading("6", text='Data')
        
        lista.column("1", width=-50, anchor='n')
        lista.column("2", width=-30, anchor='n')
        lista.column("3", width=10, anchor='n')
        lista.column("4", width=13, anchor='n')
        lista.column("5", width=50, anchor='n')
        lista.column("6", width=20, anchor='n')
        
        lista.place(relx=0.300, rely=0, relwidth=0.670, relheight=1)
        
        scrollbar = Scrollbar(self.janelaOsPendente, orient='vertical')
        lista.configure(yscroll=scrollbar.set)
        scrollbar.place(relx=0.970, rely=0, width=25, relheight=1)   
        
        self.cursorServer.execute('use empresa_funcionarios')
        
        #executando cursor com o banco de dados para verificar novamente se existe os pausadas não finalizadas
        self.cursorServer.execute("select id, OS, codigoPeca, CodigoOperacao, motivoPause, DataPause from pausa_funcionarios where cpf ="+str(self.user)+" and horaRetomada = 0")
        valido = self.cursorServer.fetchall()
        
        #se valido for igual a 1 ou mais, significa que o funcionário possui
        if len(valido) >= 1:        
            for c in valido:

                #adcionando à lista após obter as informações e tê-las armazenado no banco de dados
                pendente.append(c)
                
            #utilizando estrutura de repetição para inserir os dados obtidos já armazenado na lista pendente para o list box
            for i in range (len(pendente)):
                
                #extraindo do banco de dados as informações e armazenando nas variáveis
                idd = pendente[i][0]
                os = pendente[i][1]
                peca = pendente[i][2]
                operacao = pendente[i][3]
                motivoPause = pendente[i][4]
                data = pendente[i][5]
                
                lista.insert("", "end", values=(idd, os, peca, operacao, motivoPause, data))

        def os_select():
            
            #Lógica para pegar a OS selecionada
            try:
                
                self.listaAtiva = lista.selection()[0]
                self.tuplaSelect = lista.item(self.listaAtiva, 'values')

            except: return messagebox.showerror(parent=self.janelaOsPendente, title='Erro', message="Selecione uma OS antes de confirmar")
            
            #Limpando o campo antes de inserir o número de Os e o Código de Peça
            self.campoServico.delete(0, END)
            self.campoPeca.delete(0, END)
            self.campoOperacao.delete(0, END)
            
            #Armazenando a OS selecionada numa variável e inserindo em um campo de texto
            self.campoServico.insert(0, self.tuplaSelect[1])
            
            #Armazenando o Código da Peça selecionado em uma variável e inserindo em um campo de texto
            self.campoPeca.insert(0, self.tuplaSelect[2])
            
            #Armazenando o Código de Operação selecionado em uma variável e inserindo em um campo de texto
            self.campoOperacao.insert(0, self.tuplaSelect[3])
            
            #Buscando o tipo de OS no Banco de Dados, se é Nova ou Retrabalho
            self.cursorServer.execute('select Tipo from pausa_funcionarios where ID ='+self.tuplaSelect[0])
            valido = self.cursorServer.fetchall()

            #Armazenando imagem com visto - Imagem de Selecionado
            self.checkSelect = PhotoImage(file='img/verifica.png')
            
            if len(valido) == 1:
                
                #Verificando se o tipo de OS armazenada no Banco de Dados é Nova OS ou Retrabalho
                if valido[0] == 'Nova OS':
                
                    self.novoSelect['image'] = self.checkSelect
                    self.tipo = 'Nova OS'

                else:
                            
                    self.retrabalhoSelect['image'] = self.checkSelect
                    self.tipo = 'Retrabalhar OS'

            #Quando o parâmetro for 2, o preenchimento dos campos está sendo feito de modo automático e a OS é pendente
            #Depois de adcionado os dados nos campos, irá chamar função para confirmar
            self.botaoConfirmarOS(2)
            
            self.janelaOsPendente.destroy()
            
            
        
        #botão onde irá confirmar que o funcionário desejará retormar a OS pausada
        botaoConfirmar = Button(self.janelaOsPendente, text='Retomar OS', relief='flat', border=0, bg='#135565', fg='white', font=('arial', 19, 'bold'), command=os_select, activebackground='#135565', activeforeground='white')
        botaoConfirmar.place(relx=0.06, rely=0.800)
        
        self.janelaOsPendente.transient(self.janelaOper)
        self.janelaOsPendente.focus_force()
        self.janelaOsPendente.grab_set()
        
        #finalizando o loop da janela
        self.janelaOsPendente.mainloop()

instancia = AplicacaoFront()
