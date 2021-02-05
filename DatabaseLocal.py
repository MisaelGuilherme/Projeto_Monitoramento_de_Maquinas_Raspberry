import sqlite3

bancoLocal = sqlite3.connect('Multimoldes_Database_Local')
cursorLocal = bancoLocal.cursor()

def create_tabels():
    
    try:
        cursorLocal.execute('''create table IF NOT EXISTS OS_Finalizadas
                                
                                (id int NOT NULL,
                                Operador varchar(30) NOT NULL DEFAULT '',
                                HoraLogin varchar(8) NOT NULL DEFAULT '',
                                HoraInicial varchar(8) NOT NULL DEFAULT '',
                                DataInicial varchar(8) NOT NULL DEFAULT '',
                                HoraFinal varchar(8) NOT NULL DEFAULT '',
                                DataFinal varchar(8) NOT NULL DEFAULT '',
                                TempGasto varchar(8) NOT NULL DEFAULT '',
                                TempProgramado varchar(8) NOT NULL DEFAULT '',
                                OS varchar(8) NOT NULL DEFAULT '',
                                CodigoPeca varchar(8) NOT NULL DEFAULT '',
                                CodigoOperacao varchar(3) NOT NULL DEFAULT '',
                                TempGastoExt varchar(8) NOT NULL DEFAULT '',
                                VezTempExt varchar(8) NOT NULL DEFAULT '',
                                TempOperando varchar(8) NOT NULL DEFAULT '',
                                Tipo varchar(15) NOT NULL DEFAULT '',

                                PRIMARY KEY (id))
                                
                            ''')
        
        cursorLocal.execute('''create table IF NOT EXISTS OS_Pausadas
                                
                                (id int NOT NULL,
                                Operador varchar(30) NOT NULL DEFAULT '',
                                CodigoPeca varchar(8) NOT NULL DEFAULT '',
                                CodigoOperacao varchar(3) NOT NULL DEFAULT '',
                                OS varchar(8) NOT NULL DEFAULT '',
                                MotivoPause varchar(20) NOT NULL DEFAULT '',
                                HoraPause varchar(8) NOT NULL DEFAULT '',
                                DataPause varchar(8) NOT NULL DEFAULT '',
                                
                                HoraLogin varchar(8) NOT NULL DEFAULT '',
                                HoraInicial varchar(8) NOT NULL DEFAULT '',
                                DataInicial varchar(8) NOT NULL DEFAULT '',
                                HoraFinal varchar(8) NOT NULL DEFAULT '',
                                DataFinal varchar(8) NOT NULL DEFAULT '',
                                TempGasto varchar(8) NOT NULL DEFAULT '',
                                TempProgramado varchar(8) NOT NULL DEFAULT '',
                                TempGastoExt varchar(8) NOT NULL DEFAULT '',
                                VezTempExt varchar(8) NOT NULL DEFAULT '',
                                TempOperando varchar(8) NOT NULL DEFAULT '',
                                Tipo varchar(15) NOT NULL DEFAULT '',

                                PRIMARY KEY (id))                            
                            
                            ''')
        
    except:
        print('Erro ao criar Banco de Dados Local')

create_tabels()