import json
import math
import operator
from datetime import datetime


def normaConsulta(vec):
    #Nomral que utiliza la similitud vectorial
    norma =0
    for i in vec:
        norma+= vec[i]*vec[i]
    return math.sqrt(norma)

def crearDict(pesosTermino):
    dict = {}
    for termino in pesosTermino:
        for doc in pesosTermino[termino]:
            dict[doc[0]] = 0
    print(dict)
    return dict

def simVec2(similitudes, pesosConsulta,documentos):
    for similitud in similitudes:
        similitudes[similitud]= similitudes[similitud]/normaConsulta(pesosConsulta)*documentos[similitud]['norma']
    return similitudes
    
def simVec(pesosTermino, pesosConsulta, terminos, documentos):
    #similitud vectorial 
    
    similitudes = crearDict(pesosTermino)
    for termino in terminos:
        if termino in pesosTermino:
            for w in pesosTermino[termino]:
                sim = 0
                sim+=w[1]*pesosConsulta[termino]
                similitudes[w[0]]+= sim

    similitudes = simVec2(similitudes,pesosConsulta,documentos)
    return similitudes


def obtenerPesos(diccionarioGlobal,terminos):
    #retorna los pesos de los doc donde se encuentra el termino, y el indice del doc
    resultado = {}
    
    for termino in terminos:
        pesos=[]
        if termino in diccionarioGlobal:
            for peso in diccionarioGlobal[termino]['Postings']:
                doc = []
                doc.append(peso[0])
                doc.append(peso[2])
                pesos.append(doc)# 0 = nombre doc, 2 = peso del termino en doc    
            resultado[termino] = pesos       
    return resultado

def obtenerPesosConsulta(terminos,pesosTermino,coleccion):
    resultado = {}
    for termino in terminos:
       if termino in pesosTermino: 
        peso = math.log(1+terminos.count(termino),2)*math.log(coleccion['N']/len(pesosTermino[termino]),2) 
        resultado[termino] = peso
    return resultado



def crearEscalafon(similitudes,prefijo):
    #escalafon final .esca
    escalafon = open(prefijo+'.esca','w')
    sortedDic = sorted(similitudes.items(),key=operator.itemgetter(1),reverse=True)
    print(sortedDic)
    pos = 1
    for doc in sortedDic: 
        escalafon.write(str(pos)+". "+str(doc)+'\n')
        pos+=1
    escalafon.close()

def crearHTML(similitudes,prefijo,numDocs):
    html = open(prefijo+'.html','w')
    html.write(datetime.today().strftime('%A, %B %d, %Y %H:%M:%S'))

    #pos = buscarPosDoc
    #for doc, sim in similitudes:


    html.close()
    return

def buscarConsulta(dir,prefijo,numDocs,consulta):

    coleccion = json.load(open(dir+'/'+'coleccion.json','r'))
    diccionarioGlobal = json.load(open(dir+'/'+'diccionarioGlobal.json','r'))
    documentos = json.load(open(dir+'/'+'documentos.json','r'))
    
    terminos = consulta.split()
    pesosTermino = obtenerPesos(diccionarioGlobal,terminos) #Dicc de terminos donde traen sus docs y pesos
    
    pesosConsulta = obtenerPesosConsulta(terminos,pesosTermino,coleccion)    
    similitudes = {}
    print(pesosConsulta)

    similitudes = simVec(pesosTermino,pesosConsulta,terminos,documentos)
    print(similitudes)

    crearEscalafon(similitudes,prefijo)
    crearHTML()



#Parametro -> ruta del directorio donde se encuentran los json

if __name__ == '__main__':
    ruta = input('ingrese el dir de indice: ')
    buscarConsulta(ruta,'prueba','4','autores y evolution')
