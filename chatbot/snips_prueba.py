# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from snips_nlu import SnipsNLUEngine, load_resources
from SPARQLWrapper import SPARQLWrapper, JSON
import sys
import io
import json
import snips_nlu

resultado = []
snips_nlu.load_resources("es")
reload(sys)
sys.setdefaultencoding('utf8')
# lectura del archivo de entrenamiento para identificar la intencion
with io.open("trained.json") as f:
    engine_dict = json.load(f)
engine = SnipsNLUEngine.from_dict(engine_dict)


# metodo para obtener el detalle de la pregunta realizada
def pregunta(frase):
    r = engine.parse(unicode(frase))
    return json.dumps(r, indent=2)


# conexion a VIRTUOSO
sparql = SPARQLWrapper("http://localhost:8890/sparql/plantas1")


# metodos para las consultas a VIRTUOSO
def tipos(entidad):
    print('\n********     Tipos     ************')
    resultado = []
    print('tipos: ' + entidad)
    # envio de la sentencia SPARQL a VIRTUOSO
    sparql.setQuery("""
    select ?tipos where{
        <example:""" + entidad + """> <http://www.w3.org/2004/02/skos/core#narrower> ?tipos
    }""")
    sparql.setReturnFormat(JSON)
    # extraccion del resultado en formato JSON
    results = sparql.query().convert()
    print(results)
    # extraccion del resultado del formato JSON
    for valor in results['results']['bindings']:
        dato = (valor['tipos']['value'])
        resultado.append(dato.strip('example:'))
    # retorno del resultado para ser presentado
    print(resultado)
    return (resultado)


def definicion(entidad):
    resultado = []
    print('\n********     DEFINICION      ************')
    print(entidad)
    sparql.setQuery("""
        select ?tipos where{
            <example:""" + entidad + """> <http://www.w3.org/2004/02/skos/core#definition> ?tipos
        }""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)
    for valor in results['results']['bindings']:
        dato = (valor['tipos']['value'])
        resultado.append(dato)
    print(resultado)
    return (resultado)


def kichua(entidad):
    print('\n********     TRADUCTOR     ************')
    resultado = []
    print('kichua: ' + entidad)
    sparql.setQuery("""
        select  ?tipos where{
            <example:""" + entidad + """> <http://www.w3.org/2004/02/skos/core#prefLabel> ?tipos
        }""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)
    for valor in results['results']['bindings']:
        dato = (valor['tipos']['value'])
        resultado.append(dato)
    print(resultado)
    return (resultado[1])


def grupo(entidad):
    print('\n********     GRUPO     ************')
    resultado = []
    print('grupo: ' + entidad)
    sparql.setQuery("""
        select  ?tipos where{
            <example:""" + entidad + """> <http://www.w3.org/2004/02/skos/core#broader> ?tipos
        }""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)
    for valor in results['results']['bindings']:
        dato = (valor['tipos']['value'])
        resultado.append(dato)
    print(resultado)
    return (resultado[1])


def imagen(nombre):
    url = '/Users/macbookpro/Projects/sbcProyecto/chatbot/imagen/' + nombre + '.jpg'
    return url
