import sqlite3
import requests
import json
import pandas as pd

urlapi = 'https://servicodados.ibge.gov.br/api/v2/censos/nomes/'

def createtable():
    conn = sqlite3.connect('gender_br')
    cursor = conn.cursor()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS genero (id TEXT PRIMARY KEY, gen TEXT) ''' )

    conn.commit()
    conn.close()

def frequencia(data):
    freq = 0
    if len(data) == 0:
        return 0
    
    for i in data[0]['res']:                           #res e frequencia é a key interna do json do IBGE
        freq = i['frequencia'] + freq
        
    return freq

def genero(nome):
    
    nome = nome.split()[0]
    nome = nome.strip()
    
    conn = sqlite3.connect('gender_br')
    cursor = conn.cursor()
    
    
    
    a = cursor.execute("SELECT * from genero WHERE id=? ",(nome,) )
    b = cursor.fetchall()
    
    if len(b) != 0 :
        return b[0][1]
        
        
    else:
    
        dadosmasc = requests.get(urlapi+nome+'?sexo=M').json()
        dadosfem = requests.get(urlapi+nome+'?sexo=F').json()
    
        if len(dadosmasc) == 0 and len(dadosfem) == 0:
            cursor.execute('INSERT INTO genero (id, gen) VALUES (?, ?)', (nome, 'Indefinido'))
            conn.commit()
            return 'None'
    
        elif frequencia(dadosmasc)>frequencia(dadosfem):
            
            cursor.execute('INSERT INTO genero (id, gen) VALUES (?, ?)', (nome, 'Masculino'))
            conn.commit()
            return 'M'
        else:
            
            
            cursor.execute('INSERT INTO genero (id, gen) VALUES (?, ?)', (nome, 'Feminino'))
            conn.commit()
            return 'F'
    
    conn.commit()
    conn.close()
    
