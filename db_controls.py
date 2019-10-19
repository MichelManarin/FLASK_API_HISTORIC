from flask import Flask, request, url_for, render_template, jsonify, json, abort
import psycopg2 as pg
from urllib.parse import urlparse

DB_URL = "dbname='fybixyoh' user='fybixyoh' host='salt.db.elephantsql.com' password='A4iNsc4fOZVSJAB6ky1itVEvrEgLPXdU' port='5432'"

def get_historic():

    conn = pg.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM HISTORICO ORDER BY DATA DESC")

    linhasCidade = 0

    ListaHistorico = []
    ListaTempo = []

    DicionarioHistorico = {}
    DicionarioItemHistorico = {}
    DicionarioTempo = {}

    aux = {}
    
    for i in cur:
        linhasCidade=linhasCidade+1
        cur2 = conn.cursor()
        cur2.execute("SELECT * FROM HISTORICO_TEMPO WHERE IDHISTORICO = " + str(i[0]))
        for x in cur2:
            aux = {'data' : x[2], 'min' : x[4], 'max':x[3]}
            DicionarioTempo = aux
            ListaTempo.append(DicionarioTempo)
        cur2.close()
        aux = {'city' : i[2], 'data' : i[1], 'tempo':ListaTempo}
        ListaTempo = []
        DicionarioItemHistorico['historico'+str(linhasCidade)] = aux
    ListaHistorico.append(DicionarioItemHistorico)
    DicionarioHistorico["Historico"] = ListaHistorico

    conn.close() 
    return jsonify(DicionarioHistorico)
    
def insert_historic(*data):

    conn = pg.connect(DB_URL)

    for x in data:
        cur = conn.cursor()
        cur2 = conn.cursor()
        sql = "INSERT INTO HISTORICO(DATA,NOMECIDADE) VALUES(current_date, '" + str(x['cidade']) + "')"
        cur.execute(sql)
        conn.commit()
        previsao = x["previsao"]
        for i in previsao:
            sql = "INSERT INTO HISTORICO_TEMPO(IDHISTORICO,DATA,MAXTEMP,MINTEMP) VALUES((SELECT MAX(IDHISTORICO) FROM HISTORICO), "
            sql = sql + "'" + i["data"] + "'" + "," + i["max_temp"] + "," + i["min_temp"] + ")" 
            cur2.execute(sql)
            conn.commit() 

    cur.close()
    cur2.close()
    conn.close() 
    
    return 200        

