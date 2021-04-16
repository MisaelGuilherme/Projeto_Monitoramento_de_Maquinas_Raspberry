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
import base64

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
            
            self.cursorServer.execute('select Senha from supervisor_admin where senha ='+str(senha))
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
            print(f'Metade Hora Extra {self.ho}:', end='')
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
                print(f'{self.mi}:{self.se}')
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                self.mi = int(self.tempMin) // 2
                self.se = 0
                print(f'{self.mi}:{self.se}')
            elif int(self.tempMin) == 1:
                self.mi = 0
                self.se = (int(self.tempMin) * 60 ) // 2
                print(f'{self.mi}:{self.se}')
            #============================ ANALISAR O CODIGO =======================
            '''elif int(self.tempMin) == 2:
                self.mi = 1
                self.se = 0
                print(self.mi)
                print(self.se)'''
        
        elif int(self.tempHora) == 1:
            self.ho = 0
            print(f'Metade Hora Extra {self.ho}', end='')
            if int(self.tempMin) == 0:
                self.mi = (int(self.tempHora) * 60) // 2
                self.se = 0
                print(f'{self.mi}:{self.se}')
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                self.mi = ((int(self.tempHora) * 60) // 2) + (int(self.tempMin) // 2)
                a = int(self.tempMin)/2
                b = str(a)
                c = int(b[-1])
                d = (c*10) - 20
                self.se = d
                print(f'{self.mi}:{self.se}')
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                self.mi = ((int(self.tempHora) * 60) // 2) + (int(self.tempMin) // 2)
                self.se = 0
                print(f'{self.mi}:{self.se}')
            elif int(self.tempMin) == 1:
                self.mi = (int(self.tempHora) * 60) // 2 
                self.se = (int(self.tempMin) * 60) // 2
                print(f'{self.mi}:{self.se}')
        
        elif int(self.tempHora) > 1 and int(self.tempHora) % 2 == 0:
            self.ho = int(self.tempHora) // 2
            print(f'Metade Hora Extra {self.ho}', end='')
            if int(self.tempMin) == 0:
                self.mi = 0
                self.se = 0
                print(f'{self.mi}:{self.se}')
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                self.mi = int(self.tempMin) // 2
                a = int(self.tempMin)/2
                b = str(a)
                c = int(b[-1])
                d = (c*10) - 20
                self.se = d
                print(f'{self.mi}:{self.se}')
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                self.mi = int(self.tempMin) // 2
                self.se = 0
                print(f'{self.mi}:{self.se}')
            elif int(self.tempMin) == 1:
                self.mi = 0
                self.se = (int(self.tempMin) * 60) // 2
                print(f'{self.mi}:{self.se}')
        elif int(self.tempHora) > 1 and int(self.tempHora) % 2 != 0:
            self.ho = int(self.tempHora) // 2
            print(f'Metade Hora Extra {self.ho}', end='')
            a1 = int(self.tempHora)/2
            b2 = str(a1)
            c3 = int(b2[-1])
            d4 = (c3*10) - 20
            
            if int(self.tempMin) == 0:
                self.mi = d4
                self.se = 0
                print(f'{self.mi}:{self.se}')
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                self.mi = (d4) + (int(self.tempMin) // 2)
                a = int(self.tempMin)/2
                b = str(a)
                c = int(b[-1])
                d = (c*10) - 20
                self.se = d
                print(f'{self.mi}:{self.se}')
            elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                self.mi = (d4) + (int(self.tempMin) // 2)
                self.se = 0
                print(f'{self.mi}:{self.se}')
            elif int(self.tempMin) == 1:
                self.mi = d4
                self.se = (int(self.tempMin) * 60) // 2        
                print(f'{self.mi}:{self.se}')
        
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
        self.cursorServer.execute('select ID from pausa_funcionarios where OS ='+self.campoServico.get()+' and codigoPeca = '+self.campoPeca.get()+' and CodigoOperacao = '+self.campoOperacao.get()+' and horaRetomada = 0 and dataRetomada = 0')
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
            self.cursorServer.execute('select ID from monitoria_funcionarios where OS ='+ self.campoServico.get()+' and CodigoPeca ='+self.campoPeca.get()+' and CodigoOperacao ='+self.campoOperacao.get())
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
            
            #Atribuindo a quantidade de peça já convertido para inteiro
            quantidadePeca = int(self.quant)
            
            self.tempHora = int(tempo_pecas[0][0]) * quantidadePeca
            self.tempMin = 0
            self.tempSeg = 0
            
            #Minutos recebendo carga horária de acordo com a quantidade de peças digitadas
            
            for q in range(int(self.quant)):
                
                self.tempMin += int(tempo_pecas[0][1])
                
                #Convertendo minutos em horas caso os minutos passarem de 60    
                
                if self.tempMin >= 60:
                    self.tempHora += 1
                    self.tempMin = self.tempMin - 60
            
            #Formatando as varíaveis para encaixar no label - Tempo Programado
            self.tempProg = self.transformar_tempo_decimal(self.tempHora, self.tempMin, self.tempSeg)
            
            print('Hora Programada é:', self.tempProg)
            
            #Se a função foi invocada pelo parâmetro 2, #Quando pausado, se o tempo adcionado era tempo extra, então ao retomar irá continuar sendo tempo extra e o último tempo Adcionado
            if opcao == 2:
                
                #Selecionando do banco de dados onde o id for igual ao número de is da lista já separada igual a 10
                self.cursorServer.execute('select CorTela, VezTempExt, TempGastoExt, UltimTempAdd, TempMarcadoCron, TempProg, TempOperando from pausa_funcionarios where ID = '+self.tuplaSelect[0])
                valido = self.cursorServer.fetchall()
                
                if len(valido) == 1:
                    
                    #Recebendo cor da tela de quando foi pausada
                    self.corTelaAtual = valido[0][0]
                    
                    li = ''
                    listaNum = ''
                    #Recebendo o número de vezes tempo extra do banco de dados
                    verificandoTempExtra = valido[0][1]
                    
                    #Se for maior ou igual a 1 significa que o tempo que será adcionado e contado será do Tempo Extra restante
                    if int(verificandoTempExtra) >= 1:
                        
                        #Desfragmentando Tempo Extra já gasto pelo funcionário
                        tempo = valido[0][2]
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
                        t = valido[0][3]
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
                        self.UltimoTempAdd = valido[0][3]

                        #Quando pausado, se o tempo adcionado era tempo extra, então ao retomar o contador de vezes irá retomar com o valor de onde parou
                        self.chaveTempExtra = int(valido[0][1])
                        
                        self.vezes = Label(self.frameLeft, text='x'+str(self.chaveTempExtra), width=2, font=('arial', 15, 'bold'), bg='#135565', fg='white')
                        self.vezes.place(x=750, y=400)
                                
                        #Exibindo no label o horário adcionado após o tempo ser esgotado
                        self.campoProExt = Label(self.frameLeft, text=self.UltimoTempAdd, width=8, font=('arial', 15, 'bold'), bg='white', fg='red')
                        self.campoProExt.place(x=640, y=400)
                    
                    #Armazenando na variável o tempo marcado quando pausado
                    marcaTemp = valido[0][4]
                    
                    #Criando variável para obter o tempo marcado sem ser na forma de horário 00: 00: 00
                    self.tempoDePauseObtido = ''
                    
                    #Lógica para obter o tempo marcado sem os pontos : :
                    for c in marcaTemp:
                        if c != ':':
                            self.tempoDePauseObtido += c
                        else:
                            self.tempoDePauseObtido +=' '
                    
                    self.backup = valido[0][5]
                
                    
            if int(self.tempHora) == 0:
                self.ho = 0
                print(f'Metade de tempo1: {self.ho}:', end='')
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
                    print(f'{self.mi}:{self.se}')
                elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                    self.mi = int(self.tempMin) // 2
                    self.se = 0
                    print(f'{self.mi}:{self.se}')
                elif int(self.tempMin) == 1:
                    self.mi = 0
                    self.se = (int(self.tempMin) * 60 ) // 2
                    print(f'{self.mi}:{self.se}')
            
            elif int(self.tempHora) == 1:
                self.ho = 0
                print(f'Metade de tempo2: {self.ho}:', end='')
                if int(self.tempMin) == 0:
                    self.mi = (int(self.tempHora) * 60) // 2
                    self.se = 0
                    print(f'{self.mi}:{self.se}')
                elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                    self.mi = ((int(self.tempHora) * 60) // 2) + (int(self.tempMin) // 2)
                    a = int(self.tempMin)/2
                    b = str(a)
                    c = int(b[-1])
                    d = (c*10) - 20
                    self.se = d
                    print(f'{self.mi}:{self.se}')
                elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                    self.mi = ((int(self.tempHora) * 60) // 2) + (int(self.tempMin) // 2)
                    self.se = 0
                    print(f'{self.mi}:{self.se}')
                elif int(self.tempMin) == 1:
                    self.mi = (int(self.tempHora) * 60) // 2 
                    self.se = (int(self.tempMin) * 60) // 2
                    print(f'{self.mi}:{self.se}')
            
            elif int(self.tempHora) > 1 and int(self.tempHora) % 2 == 0:
                self.ho = int(self.tempHora) // 2
                print(f'Metade de tempo3: {self.ho}:', end='')
                if int(self.tempMin) == 0:
                    self.mi = 0
                    self.se = 0
                    print(f'{self.mi}:{self.se}')
                elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                    self.mi = int(self.tempMin) // 2
                    a = int(self.tempMin)/2
                    b = str(a)
                    c = int(b[-1])
                    d = (c*10) - 20
                    self.se = d
                    print(f'{self.mi}:{self.se}')
                elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                    self.mi = int(self.tempMin) // 2
                    self.se = 0
                    print(f'{self.mi}:{self.se}')
                elif int(self.tempMin) == 1:
                    self.mi = 0
                    self.se = (int(self.tempMin) * 60) // 2
                    print(f'{self.mi}:{self.se}')
            elif int(self.tempHora) > 1 and int(self.tempHora % 2 != 0):
                self.ho = int(self.tempHora) // 2
                print(f'Metade de tempo4: {self.ho}:', end='')
                a1 = int(self.tempHora)/2
                b2 = str(a1)
                c3 = int(b2[-1])
                d4 = (c3*10) - 20
                
                if int(self.tempMin) == 0:
                    self.mi = d4
                    self.se = 0
                    print(f'{self.mi}:{self.se}')
                elif int(self.tempMin) > 1 and int(self.tempMin) % 2 != 0:
                    self.mi = (d4) + (int(self.tempMin) // 2)
                    a = int(self.tempMin)/2
                    b = str(a)
                    c = int(b[-1])
                    d = (c*10) - 20
                    self.se = d
                    print(f'{self.mi}:{self.se}')
                elif int(self.tempMin) > 1 and int(self.tempMin) % 2 == 0:
                    self.mi = (d4) + (int(self.tempMin) // 2)
                    self.se = 0
                    print(f'{self.mi}:{self.se}')
                elif int(self.tempMin) == 1:
                    self.mi = d4
                    self.se = (int(self.tempMin) * 60) // 2
                    print(f'{self.mi}:{self.se}')
            
            if opcao == 1:
                self.backup = self.transformar_tempo_decimal(self.tempHora, self.tempMin, self.tempSeg)

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
            
            #Se a opcao for igual a 1: A OS está sendo criada e não é uma OS Pendente
            if opcao == 1:
                
                self.tempOperando = '00:00:00'
            
                self.frameBotIniciar = Frame(self.frameRight, highlightbackground='black', highlightthickness=2)
                self.frameBotIniciar.place(x=220, y=200)
                
                #Se o parâmetro for 1: A OS está sendo criada e não é uma OS Pendente
                self.botaoInciarContador = Button(self.frameBotIniciar, text='INICIAR', bg='#035700', fg='white', activebackground='#035700', activeforeground='white', relief='flat', font=('arial', 25, 'bold'), command = lambda:self.botao_iniciar(1))
                self.botaoInciarContador.pack()
            
            #Se a opcao for igual a 2: A OS está sendo retomada pois é uma OS Pendente
            elif opcao == 2:
                
                #Configurando contagem de operagem com os dados salvos da pausagem
                tempoOperador = ''
                self.tempOperando = valido[0][6]
                
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
                elif not self.tempoEsgotado:
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
                                    +self.tipo+"','"
                                    +self.quant+"')")
                                    
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
                                        +self.tipo+"','"
                                        +self.quant+"')")
                        
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
            elif not self.tempoEsgotado:
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
                                      +self.tipo+"','"
                                      +self.quant+"')")
            
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
                                     +self.tipo+"','"
                                     +self.quant+"')")
            
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

    def imagens_codificadas_base64(self):
        
        #Imagem da logo multimoldes codificada em base64
        
        self.imagemLogoMultimoldesBase64 = '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'

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
        
        #Chamando imagens codificadas
        self.imagens_codificadas_base64()
        
        self.imgFun = PhotoImage(data=base64.b64decode(self.imagemLogoMultimoldesBase64))
        
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
        
        self.campoServico = Entry(self.frameLeft, width=20, font=('arial', 19), textvariable=cOS, bg='white', justify=CENTER)
        self.campoServico.place(relx=0.455, rely=0.170)
        self.campoServico.focus_force()
        self.campoServico.bind("<Return>", self.confirmarCampos)
        
        self.codigoPeca = Label(self.frameLeft, text='Código da Peça:', font=('arial', 20, 'bold'), bg='#135565', fg='white')
        self.codigoPeca.place(relx=0.110, rely=0.340)
        
        self.campoPeca = Entry(self.frameLeft, width=20, font=('arial', 19), textvariable=cPeca, justify=CENTER)
        self.campoPeca.place(relx=0.455, rely=0.340)
        self.campoPeca.bind("<Return>", self.confirmarCampos)
        
        self.lbQuantidadePeca = Label(self.frameLeft, text='nº', font=('Arial', 20, 'bold'), bg='#135565', fg='white')
        self.lbQuantidadePeca.place(relx=0.830, rely=0.340)
        
        self.campQuantidadePeca = Entry(self.frameLeft, font=('arial', 19), textvariable=cQuant, justify=CENTER)
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
        self.campoOperacao = Entry(self.frameLeft, width=20, font=('arial', 19), textvariable=cOper, justify=CENTER)
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
        self.cursorServer.execute("select ID from pausa_funcionarios where cpf ="+self.user+" and horaRetomada = 0")
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
        
        lista = ttk.Treeview(self.janelaOsPendente, column=("1","2","3","4","5","6","7"), show='headings')
        
        lista.heading("1", text='ID')
        lista.heading("2", text='O.S')
        lista.heading("3", text='Peça')
        lista.heading("4", text='Operação')
        lista.heading("5", text='Quant.')
        lista.heading("6", text='Pausado')
        lista.heading("7", text='Data')
        
        lista.column("1", width=-50, anchor='n')
        lista.column("2", width=-30, anchor='n')
        lista.column("3", width=10, anchor='n')
        lista.column("4", width=13, anchor='n')
        lista.column("5", width=-10, anchor='n')
        lista.column("6", width=50, anchor='n')
        lista.column("7", width=20, anchor='n')
        
        lista.place(relx=0.300, rely=0, relwidth=0.670, relheight=1)
        
        scrollbar = Scrollbar(self.janelaOsPendente, orient='vertical')
        lista.configure(yscroll=scrollbar.set)
        scrollbar.place(relx=0.970, rely=0, width=25, relheight=1)   
        
        self.cursorServer.execute('use empresa_funcionarios')
        
        #executando cursor com o banco de dados para verificar novamente se existe os pausadas não finalizadas
        self.cursorServer.execute("select id, OS, codigoPeca, CodigoOperacao, Quant, motivoPause, DataPause from pausa_funcionarios where cpf ="+str(self.user)+" and horaRetomada = 0")
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
                quantidade = pendente[i][4]
                motivoPause = pendente[i][5]
                data = pendente[i][6]
                
                lista.insert("", "end", values=(idd, os, peca, operacao, quantidade, motivoPause, data))

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
            self.campQuantidadePeca.delete(0, END)
            
            #Armazenando a OS selecionada numa variável e inserindo em um campo de texto
            self.campoServico.insert(0, self.tuplaSelect[1])
            
            #Armazenando o Código da Peça selecionado em uma variável e inserindo em um campo de texto
            self.campoPeca.insert(0, self.tuplaSelect[2])
            
            #Armazenando o Código de Operação selecionado em uma variável e inserindo em um campo de texto
            self.campoOperacao.insert(0, self.tuplaSelect[3])
            
            #Armazenando Quantidade de Peça selecionado em uma variável e inserindo em um campo de texto
            self.campQuantidadePeca.insert(0, self.tuplaSelect[4])
            
            #Buscando o tipo de OS no Banco de Dados, se é Nova ou Retrabalho
            self.cursorServer.execute('select Tipo from pausa_funcionarios where ID ='+self.tuplaSelect[0])
            valido = self.cursorServer.fetchall()

            #Armazenando imagem com visto - Imagem de Selecionado
            self.checkSelect = PhotoImage(file='img/verifica.png')
            
            if len(valido) == 1:
                
                #Verificando se o tipo de OS armazenada no Banco de Dados é Nova OS ou Retrabalho
                if valido[0][0] == 'Nova OS':
                
                    self.novoSelect['image'] = self.checkSelect
                    self.tipo = 'Nova OS'

                elif valido[0][0] == 'Retrabalhar OS':
                            
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
