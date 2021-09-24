# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import os
import numpy as np
import pandas as pd
import urllib.parse
from decouple import config
from sqlalchemy import create_engine

### Funciones recurso para crear la conexión a la base
### de datos.

def create_conn(credentials):
    try:
        engine = create_engine(credentials)

        print('Conexión establecida')
        return engine

    except:
        print('Conexión no establecida')  
        return None

def query_generation(objetivo, tiempo, lugar):
    """
    Genera el respectivo query según los valores capturados en el form
    """        
    # para cuando el objetivo captura el genero
    obj, gen = objetivo.split(' ')

    if obj in ['positivas', 'positivos']: # para obj positivo
        if tiempo in ['últimos {} meses'.format(i) for i in range(2,13)]: # si preguntan por los últimos meses
            # se parte de la suposición que todos tiene lugar
            _, meses, _ = tiempo.split(' ') # solo se considera para número pero se puede hacer un mapeo si viene en letra
            query = "SELECT count(SUBDATE(NOW(), INTERVAL {} month)) from s_IRA_muestras where ajuste=3 and comuna like (%{}%);".format(meses,lugar)


class QueryResponse(Action):
    """
    Función que hace la conexión a la base de datos
    y con base en las entidades capturadas en la pregunta hecha 
    por el usuario se genera el query a la base de datos
    """   

    def name(self) -> Text:
        return "query_responce"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:  

        # Capturar los valores en lo slots llenados por el usuario
        objetivo = tracker.get_slot("objetivo") 
        tiempo = tracker.get_slot("tiempo")
        lugar =  tracker.get_slot("lugar")

        # primero crear la conexión a la base de datos
        # CREDEMCIALES PARA INGRESAR A LA BASE DE DATOS 
        # ESTAS CREDENCIALES DEBEN ESTAR ALMACENADAS EN 
        # UN ARCHIVO OCULTO POR SEGURIDAD
        
        covid_DB_credential = {
        'user' : config('user'),
        'password':urllib.parse.quote_plus(config('password')), # SE USA PARA NO TENER PROBLEMA CON CARACTERES ESPECIALES
        'url':config('url'),
        'port':config('port'),
        'db_name':config('db_name'),
        'tsql_chunksize':2097
                                }

        # strings de conexión
        info_str_covid = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(covid_DB_credential['user'],
                                                            covid_DB_credential['password'],
                                                            covid_DB_credential['url'],
                                                            covid_DB_credential['port'],
                                                            covid_DB_credential['db_name'])

        # Establecer la conexión
        conn = create_conn(info_str_covid)   

        # Crear y hacer el query a la base de datos

        query = 'select (fec_not) DIA,count(FEC_NOT) POSITIVOS_DIA from s_IRA_ira where AJUSTE=3  group by (fec_NOT);'
        query_result = pd.read_sql_query(query, 
                                        con = conn, 
                                        index_col = None, 
                                        coerce_float = True, 
                                        parse_dates = True, 
                                        chunksize = None)

        return_text = "Estos fueron los valores que capture Objetivo: {} - tiempo: {} y lugar: {} y el\
                        query resultante es {}".format(objetivo,tiempo,lugar,query_result)

        dispatcher.utter_message(text=str(return_text))


        return []



# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
