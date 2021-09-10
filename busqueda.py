import json
import math

def norma(vec):
    #Nomral que utiliza la similitud vectorial
    norma =0
    norma+= vec*vec
    return math.sqrt(norma)


def simVec(dj,q):
    #similitud vectorial 
    sim = 0
    for w in dj:
        for v in q:
            sim+=w*v
    sim = sim/norma(dj)*norma(q)

def obtenerPesos(diccionarioGlobal,termino):
    #retorna los pesos de los doc donde se encuentra el termino
    pesos = []
    for doc in diccionarioGlobal[termino]['Postings']:
        pesos.append(doc[2])
    return pesos

def buscarConsulta(dir,prefijo,numDocs,consulta):

    coleccion = json.load(open(dir+'/'+'coleccion.json','r'))
    diccionarioGlobal = json.load(open(dir+'/'+'diccionarioGlobal.json','r'))
    documentos = json.load(open(dir+'/'+'documentos.json','r'))
    
    terminos =consulta.split()
    
    #for termino in terminos:
    pesosTermino = obtenerPesos(diccionarioGlobal,terminos[0])
     #  simVec(termino)





#Parametro -> ruta del directorio donde se encuentran los json

if __name__ == '__main__':
    ruta = input('ingrese el dir de indice: ')
    buscarConsulta(ruta,'vec','4','autores y evolution')
