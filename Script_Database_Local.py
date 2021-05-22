import sqlite3

#Conectando banco de dados local e cursor
bancoLocal = sqlite3.connect('Multimoldes_Database_Local')
cursorLocal = bancoLocal.cursor()

#Criando tabelas do banco de dados local
def create_tabels():
    
    try:
        
        #Tabela onde ficará armazenada as OS Finalizadas caso haja erro na rede
        cursorLocal.execute('''create table IF NOT EXISTS OS_Finalizadas
                                
                                (ID varchar(2) NOT NULL DEFAULT 'ID',
                                Operador varchar(30) NOT NULL DEFAULT '',
                                CPF varchar(11) NOT NULL DEFAULT '00000000000',
                                HoraLogin varchar(8) NOT NULL DEFAULT '00:00:00',
                                HoraInicial varchar(8) NOT NULL DEFAULT '00:00:00',
                                DataInicial date NOT NULL DEFAULT '0000-00-00',
                                HoraFinal varchar(8) NOT NULL DEFAULT '00:00:00',
                                DataFinal date NOT NULL DEFAULT '0000-00-00',
                                TempGasto varchar(8) NOT NULL DEFAULT '00:00:00',
                                TempProgramado varchar(8) NOT NULL DEFAULT '00:00:00',
                                OS varchar(8) NOT NULL DEFAULT '',
                                CodigoPeca varchar(8) NOT NULL DEFAULT '',
                                CodigoOperacao varchar(3) NOT NULL DEFAULT '',
                                TempGastoExt varchar(8) NOT NULL DEFAULT '00:00:00',
                                VezTempExt varchar(8) NOT NULL DEFAULT '0',
                                TempOperando varchar(8) NOT NULL DEFAULT '00:00:00',
                                Tipo varchar(15) NOT NULL DEFAULT '',
                                Quant int(4) NOT NULL DEFAULT 1,
                                Maquina varchar(10) NOT NULL DEFAULT 'Máquina 00')
                                
                            ''')
        
        #Tabela onde ficará armazenada as OS Pausadas caso haja erro na rede
        cursorLocal.execute('''create table IF NOT EXISTS OS_Pausadas
                                
                                (ID varchar(2) NOT NULL DEFAULT 'ID',
                                Operador varchar(30) NOT NULL DEFAULT '',
                                CPF varchar(11) NOT NULL DEFAULT '00000000000',
                                CodigoPeca varchar(8) NOT NULL DEFAULT '',
                                CodigoOperacao varchar(3) NOT NULL DEFAULT '',
                                OS varchar(8) NOT NULL DEFAULT '',
                                MotivoPause varchar(20) NOT NULL DEFAULT '',
                                HoraPause varchar(8) NOT NULL DEFAULT '',
                                DataPause date NOT NULL DEFAULT '0000-00-00',
                                HoraRetomada varchar(8) NOT NULL DEFAULT '',
                                DataRetomada date NOT NULL DEFAULT '0000-00-00',
                                TempMarcadoCron varchar(8) NOT NULL DEFAULT '',
                                TempGastoProg varchar(8) NOT NULL DEFAULT '00:00:00',
                                TempGastoExt varchar(8) NOT NULL DEFAULT '00:00:00',
                                VezTempExt varchar(2) NOT NULL DEFAULT '0',
                                UltimTempAdd varchar(8) NOT NULL DEFAULT '00:00:00',
                                TempProg varchar(8) NOT NULL DEFAULT '',
                                CorTela varchar(8) NOT NULL DEFAULT '',
                                Hora_Login varchar(8) NOT NULL DEFAULT '00:00:00',
                                Hora_Inicial varchar(8) NOT NULL DEFAULT '00:00:00',
                                Data_Inicial date NOT NULL DEFAULT '0000-00-00',
                                TempOperando varchar(8) NOT NULL DEFAULT '00:00:00',
                                Tipo varchar(14) NOT NULL DEFAULT '',
                                Quant int(4) NOT NULL DEFAULT 1,
                                Maquina varchar(10) NOT NULL DEFAULT 'Máquina 00')
                            
                            ''')
        
        print('BANCO DE DADOS LOCAL CRIADO')
        
    except:
        print('Erro ao criar Banco de Dados Local')

#Invocando função
create_tabels()