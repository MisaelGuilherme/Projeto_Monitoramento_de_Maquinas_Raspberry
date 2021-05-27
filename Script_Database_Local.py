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
                                HoraLogin time NOT NULL DEFAULT '00:00:00',
                                HoraInicial time NOT NULL DEFAULT '00:00:00',
                                DataInicial date NOT NULL DEFAULT '0000-00-00',
                                HoraFinal time NOT NULL DEFAULT '00:00:00',
                                DataFinal date NOT NULL DEFAULT '0000-00-00',
                                TempGasto time NOT NULL DEFAULT '00:00:00',
                                TempProgramado time NOT NULL DEFAULT '00:00:00',
                                OS varchar(13) NOT NULL DEFAULT '',
                                CodigoPeca varchar(13) NOT NULL DEFAULT '',
                                CodigoOperacao varchar(3) NOT NULL DEFAULT '',
                                TempGastoExt time NOT NULL DEFAULT '00:00:00',
                                VezTempExt tinyint(4) NOT NULL DEFAULT '0',
                                TempOperando time NOT NULL DEFAULT '00:00:00',
                                Tipo varchar(15) NOT NULL DEFAULT '',
                                Quant mediumint(9) NOT NULL DEFAULT '1',
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
                                HoraPause time NOT NULL DEFAULT '00:00:00',
                                DataPause date NOT NULL DEFAULT '0000-00-00',
                                HoraRetomada time NOT NULL DEFAULT '00:00:00',
                                DataRetomada date NOT NULL DEFAULT '0000-00-00',
                                TempMarcadoCron varchar(8) NOT NULL DEFAULT '',
                                TempGastoProg time NOT NULL DEFAULT '00:00:00',
                                TempGastoExt time NOT NULL DEFAULT '00:00:00',
                                VezTempExt tinyint(4) NOT NULL DEFAULT '0',
                                UltimTempAdd varchar(8) NOT NULL DEFAULT '00:00:00',
                                TempProg time NOT NULL DEFAULT '00:00:00',
                                CorTela varchar(8) NOT NULL DEFAULT '',
                                Hora_Login time NOT NULL DEFAULT '00:00:00',
                                Hora_Inicial time NOT NULL DEFAULT '00:00:00',
                                Data_Inicial date NOT NULL DEFAULT '0000-00-00',
                                TempOperando varchar(8) NOT NULL DEFAULT '00:00:00',
                                Tipo varchar(14) NOT NULL DEFAULT '',
                                Quant int(4) NOT NULL DEFAULT 1,
                                Maquina varchar(10) NOT NULL DEFAULT 'Máquina 00',
                                repairTemp varchar(8) NOT NULL DEFAULT '00:00:00')
                            
                            ''')
        
        print('BANCO DE DADOS LOCAL CRIADO')
        
    except Exception as erro:
        print('Erro ao criar Banco de Dados Local', erro)

#Invocando função
create_tabels()