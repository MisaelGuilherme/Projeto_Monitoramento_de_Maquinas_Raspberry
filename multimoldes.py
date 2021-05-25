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
                
                host = "10.0.0.65",
                user = "MultimoldesClient",
                password = "",
                database="empresa_funcionarios")
            
            #verificando se usuário existe no banco de dados
            self.cursorServer = self.bancoServer.cursor()
            
            self.bancoCriado = True
            self.bancoConect = self.bancoServer.is_connected()
        
        except Exception as erro:
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
        
        self.vezes['text'] = 'x'+str(self.chaveTempExtra)
        self.vezes['bg'] = '#870000'
        self.vezes.place(relx=0.950, rely=0.700)
        
        #Exibindo no label o horário adcionado após o tempo ser esgotado
        
        self.campoProExt['text'] = self.tempProgExt
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
                    self.horaLogin = str(time)
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
        self.cursorServer.execute("select codigo, hora, minuto from pecas_codigo where codigo = "+self.campoPeca.get())
        valido = self.cursorServer.fetchall()
        
            
        #Se ao ler a variável valido o valor for igual a 0, provavelmente não existe no banco de dados
        if len(valido) == 0:
            
            #Exibindo mensagem alertando que o Código de Peça não foi encontrado
            return messagebox.showerror(parent=self.janelaOper, title='Alerta', message='Código não Encontrado!')

        elif int(valido[0][1]) == 0 and int(valido[0][2]) == 0:
            
            #Exibindo mensagem alertando que o Código de Peça não foi encontrado
            return messagebox.showerror(parent=self.janelaOper, title='Alerta', message='Hora Programada Inválida para Operação!')
        
        #Buscando no banco de dados se existe a OS digitada e o Código de Peça em modo pausado
        self.cursorServer.execute('select ID from pausa_funcionarios where OS ='+self.campoServico.get()+' and codigoPeca = '+self.campoPeca.get()+' and CodigoOperacao = '+self.campoOperacao.get()+' and horaRetomada = 0 and dataRetomada = 0000-00-00')
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
            
            self.checkSelect = PhotoImage(data=base64.b64decode(self.imagemCheckBoxSelect))
            
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
                    if verificandoTempExtra >= 1:
                        
                        #Desfragmentando Tempo Extra já gasto pelo funcionário
                        tempo = str(valido[0][2])
                        
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
                        t = str(valido[0][3])
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
                        self.UltimoTempAdd = str(valido[0][3])

                        #Quando pausado, se o tempo adcionado era tempo extra, então ao retomar o contador de vezes irá retomar com o valor de onde parou
                        self.chaveTempExtra = valido[0][1]
                        
                        self.vezes['text'] = 'x'+str(self.chaveTempExtra)
                        self.vezes.place(relx=0.950, rely=0.700)
                        
                        self.campoProExt['text'] = self.UltimoTempAdd
                        self.campoProExt.place(relx=0.810, rely=0.700)
                        
                    
                    #Armazenando na variável o tempo marcado quando pausado
                    marcaTemp = str(valido[0][4])
                    
                    #Criando variável para obter o tempo marcado sem ser na forma de horário 00: 00: 00
                    self.tempoDePauseObtido = ''
                    
                    #Lógica para obter o tempo marcado sem os pontos : :
                    for c in marcaTemp:
                        if c != ':':
                            self.tempoDePauseObtido += c
                        else:
                            self.tempoDePauseObtido +=' '
                    
                    self.backup = str(valido[0][5])
                
                    
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
                self.tempOperando = str(valido[0][6])
                
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
        
        if self.chaveTempExtra >= 1:
            self.vezes['bg'] = cor1
            self.vezes['fg'] = cor2
            
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
                time = datetime.now().time().strftime('%H:%M:%S')
                date = datetime.now().date()
                
                self.horaInicial = str(time)
                self.dateInicial = str(date)
                
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
            #gpio.output(40, gpio.HIGH)
            
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

            self.imgRelogio = PhotoImage(data=base64.b64decode(self.imagemRelogioIlustrativoBase64))

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
            #gpio.output(40, gpio.LOW)
            
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
        #gpio.output(40, gpio.LOW)
        
        #Mostrando o botão sair ao iniciar operação
        self.frameBotSair.place(relx=0.920, rely=0.130)
        
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
            date = datetime.now().date()
            
            #Atribuindo a Hora Final atual e a Data Final atual nas respectivas variáveis
            horaFinal = str(time)
            dateFinal = str(date)
            
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
            
            #Convertendo para String para concatenação
            self.chaveTempExtra = str(self.chaveTempExtra)
            
            #Enviando todos os dados ao banco
            try:
                self.cursorServer.execute('use empresa_funcionarios')
                self.cursorServer.execute("insert into monitoria_funcionarios VALUES('id','"
                                    +str(self.operador)+"','"
                                    +str(self.user)+"','"
                                    +self.horaLogin+"','"
                                    +self.horaInicial+"','"
                                    +self.dateInicial+"','"
                                    +horaFinal+"','"
                                    +dateFinal+"','"
                                    +self.tempGasto+"','"
                                    +self.tempProg+"','"
                                    +self.numOS+"','"
                                    +self.codP+"','"
                                    +self.numOper+"','"
                                    +self.tempExtraGasto+"','"
                                    +self.chaveTempExtra+"','"
                                    +self.tempOperando+"','"
                                    +self.tipo+"','"
                                    +self.quant+"','"
                                    +self.nMaquina+"')")
                                    
                self.bancoServer.commit()
                
                messagebox.showinfo(parent=self.janelaOper, title='DATABASE SERVER', message='O.S Finalizada! Operação salva.')
                
            #Excessão caso ocorra de não conseguir salvar
            except Exception as erro:
                
                if messagebox.showerror(parent=self.janelaOper, title='06-Error-Servidor', message='06-Error: Não acesso ao servidor.'):
            
                    try:
                        
                        self.cursorLocal.execute("insert into OS_Finalizadas VALUES(NULL,'"
                                        +str(self.operador)+"','"
                                        +str(self.user)+"','"
                                        +self.horaLogin+"','"
                                        +self.horaInicial+"','"
                                        +self.dateInicial+"','"
                                        +horaFinal+"','"
                                        +dateFinal+"','"
                                        +self.tempGasto+"','"
                                        +self.tempProg+"','"
                                        +self.numOS+"','"
                                        +self.codP+"','"
                                        +self.numOper+"','"
                                        +self.tempExtraGasto+"','"
                                        +self.chaveTempExtra+"','"
                                        +self.tempOperando+"','"
                                        +self.tipo+"','"
                                        +self.quant+"','"
                                        +self.nMaquina+"')")
                        
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
            self.janelaPause.wm_iconphoto(True, self.icone)

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
        self.frameBotSair.place(relx=0.920, rely=0.130)
        
        #Variável que irá habilitar a porta para pode executar a máquina (True=Ligado, False=Desligado)
        #gpio.output(40, gpio.LOW)
        
        #Se a função de piscar o led estiver ligada ela será desligada com a variável de controle "desligarfuncaoLed"
        if self.ledPiscando == True and self.desligarfuncaoLed == False:
            
            self.desligarfuncaoLed = True
            self.ledPiscando = False
            
        #Ligando todos as portas com os leds, informando que a máquina está liberada
        #gpio.output(8, gpio.HIGH)
        #gpio.output(12, gpio.HIGH)
        #gpio.output(18, gpio.HIGH)
                
        
        #Capturando a hora inicial e a data atual em que o modo pause foi iniciado, em seguida inserir no banco de dados
        time = datetime.now().time().strftime('%H:%M:%S')
        date = datetime.now().date()
        
        horaPause = str(time)
        datePause = str(date)
        
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
            
        #Convertendo para String para concatenação
        self.chaveTempExtra = str(self.chaveTempExtra)
            
        try:
            self.cursorServer.execute("insert into pausa_funcionarios VALUES('id','"
                                      +str(self.operador)+"','"
                                      +self.user+"','"
                                      +self.codP+"','"
                                      +self.numOper+"','"
                                      +self.numOS+"','"
                                      +self.resultPausa+"','"
                                      +horaPause+"','"
                                      +datePause+"','0','0','"
                                      +self.tempoMarcado+"','"
                                      +self.tempGasto+"','"
                                      +self.tempExtraGasto+"','"
                                      +self.chaveTempExtra+"','"
                                      +self.UltimoTempAdd+ "','"
                                      +self.tempProg+"','"
                                      +corTela+"','"
                                      +self.horaLogin+"','"
                                      +self.horaInicial+"','"
                                      +self.dateInicial+"','"
                                      +self.tempOperando+"','"
                                      +self.tipo+"','"
                                      +self.quant+"','"
                                      +self.nMaquina+"')")
            
            self.bancoServer.commit()
            
            messagebox.showinfo(parent=self.janelaOper, title='DATABASE SERVER', message='O.S Pausada! Operação salva.')
            
        except Exception as erro:
            return print(erro)
            self.cursorLocal.execute("insert into OS_Pausadas VALUES('id','"
                                     +str(self.operador)+"','"
                                     +self.user+"','"
                                     +self.codP+"','"
                                     +self.numOper+"','"
                                     +self.numOS+"','"
                                     +self.resultPausa+"','"
                                     +horaPause+"','"
                                     +datePause+"','00:00:00','0000-00-00','"
                                     +self.tempoMarcado+"','"
                                     +self.tempGasto+"','"
                                     +self.tempExtraGasto+"','"
                                     +self.chaveTempExtra+"','"
                                     +self.UltimoTempAdd+ "','"
                                     +self.tempProg+"','"
                                     +corTela+"','"
                                     +self.horaLogin+"','"
                                     +self.horaInicial+"','"
                                     +self.dateInicial+"','"
                                     +self.tempOperando+"','"
                                     +self.tipo+"','"
                                     +self.quant+"','"
                                     +self.nMaquina+"')")
            
            self.bancoLocal.commit()
            
            messagebox.showinfo(parent=self.janelaOper, title='DATABASE LOCAL', message='O.S Pausada! Operação salva.')
    
    def contagem_despausar(self, despause):
        try:
            
            #Capturando a hora e a data atual em que a OS foi despausada, em seguida inserir no banco de dados
            time = datetime.now().time().strftime('%H:%M:%S')
            date = datetime.now().date()
            
            horaRetomada = str(time)
            dateRetomada = str(date)

            #Atualizando Banco de Dados Local com data e hora retomada após função despausar for invocada
            #self.cursorLocal.execute("update OS_Pausadas set DataRetomada = '"+dateFinal+"' where CPF = '"+self.user+"' and CodigoPeca = '"+self.codP+"' and OS = '"+self.numOS+"' and DataRetomada = 0000-00-00 ")
            #self.bancoLocal.commit()
            
            #self.cursorLocal.execute("update OS_Pausadas set HoraRetomada = '"+horaRetomada+"' where CPF = '"+self.user+"' and CodigoPeca = '"+self.codP+"' and OS = '"+self.numOS+"' and HoraRetomada = 0 ")
            #self.bancoLocal.commit()
            
            #Atualizando Banco de Dados Server com data e hora retomada após função despausar for invocada
            self.cursorServer.execute("update pausa_funcionarios set DataRetomada = '"+dateRetomada+"' where CPF = '"+self.user+"' and CodigoPeca = '"+self.codP+"' and OS = '"+self.numOS+"' and DataRetomada = '0000-00-00' ")
            self.bancoServer.commit()
            
            self.cursorServer.execute("update pausa_funcionarios set HoraRetomada = '"+str(horaRetomada)+"' where CPF = '"+self.user+"' and CodigoPeca = '"+self.codP+"' and OS = '"+self.numOS+"' and HoraRetomada = '00:00:00' ")
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
            #gpio.output(40, gpio.HIGH)
            
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
                
                #Convertendo para Inteiro
                self.chaveTempExtra = int(self.chaveTempExtra)
                
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
                self.horaLogin = str(valido[0][0])
                self.horaInicial = str(valido[0][1])
                self.dateInicial = str(valido[0][2])
            
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
        
        
        #Ícone da multimoldes
        
        
        self.iconeLogoMultimoldesBase64 = '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'
        
        
        #Imagem da logo Multimoldes codificada em base64
        
        self.imagemLogoMultimoldesBase64 = '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'
        
        
        #Imagem da Logo Multimoldes com borda azul
        
        
        self.imagemLogoAzulMultimoldesBase64 = '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'
        
        
        #Imagem de checkbox não selecionada
        
        
        self.imagemCheckBoxNoSelect = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAkgAAAJIB+bxJdAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAEaSURBVDiNrdOxLoRBFAXgb0SxhVJCYSv8HkDYgmdQiYSodJsoVjwEzUbnEVQSxSa8gHIli06i8ggaqqswv4w/u5o1yRRz7zln7j1zJ0WEcqWUKhxgHe0cfsMDriLi5RchImSRhB6G2EW7yLVzbJgx6SdXkAfoo1UnmxutjBnUInWih/4k4hihPnp1+1UubeLNGXiIvaKSIarZbNh5RHyYsFJKXexgLqX0HhF3KaVz7Mv9lIbNY6E4d3GLNTxjszB2AKMCvIQRnrBSkKsc2260NWoKHOEGG3jN5FU8NsmlQLOFC1xiEcsZNI7cxmDG94R1asMi4gSfOMM1jiPifoy3nfwS458Rp9j6Y6CGqKYfpH8Z5Wk+U5r2O38Bs+1gu0WzoMYAAAAASUVORK5CYII='
        
        
        #Imagem de checkbox selecionada
        
        
        self.imagemCheckBoxSelect = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAmgAAAJoB3TZBEQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAGiSURBVDiNjdOxT1NRFMfx77mtKWVAqhMSCRDo4ETSAqG1BhMSk/fYDWVlRxLjUKfq5ELCwOIfwF/ARR1N00ECiTBgUmIghUCMk2B8grXH4dH6ivalv/He9zk3991zRFUJ5sEb514dHotKSiEFqMK2gW1greTYSvB7aRSQYtFkJj48FZUXQIz/x0OlUHbtiuJDUVWkWDTZ8c13wEwb2BqVjbJrZxVVA5AZ33zSMfaPdbLWXQSQqbePRszvyC4QDzPxSDe90VucXhw3ryMwZkwtmu8ELw4+59nwS/pi/c3lOswZRNOd4KH4KPs/PvH18ktwO22AZgFByN9ZYLI39w/eOd/idXWZmtb+/gpIRYPl+rsGyCQekkvMEDNdZBLTbXEjkbvzo9MCSYCz2jcOvc+kb04x1jNB4sbtUKzw3lx1WDN733dYrb7iV/0yFF9lS+5bJ6nwkWsvMRAf4uTnURj2n7Hk2Aoqheu7Ve8gDINKoeTYit/KiGStu46o01604NZWVlTLrp1FZQnwQqiHylIDQ2AaG8ltuEkgX4eU+ONM2Dj/Afn3u1yy2NNwAAAAAElFTkSuQmCC'
        
        
        #Imagem do Relógio Indicando que o horário irá exceder
        
        
        self.imagemRelogioIlustrativoBase64 = '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'
        
        
        #Imagem da logo Admin codificada em base64
        
        
        self.imagemLogoAdminBase64 = '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'

class AplicacaoFront(AplicacaoBack):
   
    def __init__(self):
        
        self.janelaFuncio = Tk()
        self.janelaFuncio.title('Login Funcionário')
        self.janelaFuncio.configure(background='white')
        self.janelaFuncio.minsize(500, 400)
        
        #Chamando imagens codificadas
        self.imagens_codificadas_base64()
        
        self.icone = PhotoImage(data=base64.b64decode(self.iconeLogoMultimoldesBase64))
        
        self.sistemaOperacional = system()
        
        if self.sistemaOperacional == 'Windows':
            self.janelaFuncio.wm_iconphoto(True, self.icone)
            self.janelaFuncio.state('zoomed')
        else:
            self.janelaFuncio.attributes('-zoomed', True)
        
        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(900, 600, self.janelaFuncio)
        
        #Chamando imagens codificadas
        self.imagens_codificadas_base64()
        
        self.imgFun = PhotoImage(data=base64.b64decode(self.imagemLogoMultimoldesBase64))
        
        self.frameLogin = Frame(self.janelaFuncio, width=700, height=600, bg='white')
        self.frameLogin.pack()
        
        self.nMaquina = 'Máquina 01'
        self.lbMaquina = Label(self.janelaFuncio, text=self.nMaquina, bg='white', fg='#3e8e94', font=('arial',18,'bold'))
        self.lbMaquina.place(relx=0.870, rely=0.030)

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
        
        def limpar_campos_login():
            
            self.campoLogin.delete(0, END)
            self.campoSenha.delete(0, END)
            self.campoLogin.focus_force()
        
        self.botLimparCamposLogin = Button(self.frameLogin, text='Limpar', fg='white', activeforeground='white', bg='#3e8e94', activebackground='#3e8e94', border=0, font=('arial', 14, 'bold'), width=8, command=limpar_campos_login)
        self.botLimparCamposLogin.place(relx=0.770, rely=0.500)

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
            self.janelaADM.wm_iconphoto(True, self.icone)
        
        #Chamando Função Para Centralizar a Tela
        self.centraliza_tela(600, 600, self.janelaADM)
        
        #Adicionando Logo na Janela ADM
        imgAdm = PhotoImage(data=base64.b64decode(self.imagemLogoAdminBase64))

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
            self.janelaTempExtra.wm_iconphoto(True, self.icone)
        
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
        
        self.checkVazio = PhotoImage(data=base64.b64decode(self.imagemCheckBoxNoSelect))
        
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
        
        #(Tela Operativa) - LABELS QUE IMPRIMEM O TEMPO EXTRA QUANDO HOUVER
        self.vezes = Label(self.frameLeft, width=2, font=('arial', 15, 'bold'), bg='#135565', fg='white')
        
        self.campoProExt = Label(self.frameLeft, width=8, font=('arial', 15, 'bold'), bg='white', fg='red')
        
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
        
        logoMarca = PhotoImage(data=base64.b64decode(self.imagemLogoAzulMultimoldesBase64))
        
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
        
        self.UltimoTempAdd = '00:00:00' 
        
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
        image = PhotoImage(data=base64.b64decode(self.imagemLogoMultimoldesBase64))
        
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
            self.checkSelect = PhotoImage(data=base64.b64decode(self.imagemCheckBoxSelect))
            
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
