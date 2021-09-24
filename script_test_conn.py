import numpy as np
import pandas as pd
import urllib.parse
from sqlalchemy import create_engine

def create_conn(credentials):
    try:
        engine = create_engine(credentials)

        print('Conexión establecida')
        return engine

    except:
        print('Conexión no establecida')  
        return None

# crear la conexion a la base de datos de covid
covid_DB_credential = {
    'user' : 'etlsaludpcc',
    'password':urllib.parse.quote_plus('Et1s@1udXX20'),
    'url':'131.110.1.43',
    'port':'3306',
    'db_name':'salud_fin_1',
    'tsql_chunksize':2097
}

# crear la conexión a vacunción
vac_DB_credential = {
    'user' : 'admin_vacunacion',
    'password':urllib.parse.quote_plus('ADMINvac2021*'),
    'url':'131.110.1.11',
    'port':'3306',
    'db_name':'vacunacionbga',
    'tsql_chunksize':2097
}


# strings de conexión
info_str_covid = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(covid_DB_credential['user'],
                                                        covid_DB_credential['password'],
                                                        covid_DB_credential['url'],
                                                        covid_DB_credential['port'],
                                                        covid_DB_credential['db_name'])

info_str_vac = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(vac_DB_credential['user'],
                                                        vac_DB_credential['password'],
                                                        vac_DB_credential['url'],
                                                        vac_DB_credential['port'],
                                                        vac_DB_credential['db_name'])

# crear la conexión a la base de datos de covid
conn_covid = create_conn(info_str_covid)  
# crear la conexión a la base de datos de vacunacion
conn_vac = create_conn(info_str_vac) 
print(conn_covid)
print(conn_vac)
# hacer un query de ejemplo
# positivos_covid
query = 'select (fec_not) DIA,count(FEC_NOT) POSITIVOS_DIA from s_IRA_ira where AJUSTE=3  group by (fec_NOT);'
positivos_covid = pd.read_sql_query(query, 
                                    con = conn_covid, 
                                    index_col = None, 
                                    coerce_float = True, 
                                    parse_dates = True, 
                                    chunksize = None)

print(positivos_covid)                                    
