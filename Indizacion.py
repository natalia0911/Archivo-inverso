####################################################
#Version de Python 3.9.2
#Creado el 27/08/2021
#Ultima modificación
####################Autores#########################
#Javier Rivera
#Natalia Vargas Reyes
#Proyecto 1, Recuperación de la información textual
####################################################

import re
from unicodedata import normalize
from pathlib import Path
from pathlib import PurePath
from math import log
from math import sqrt
import json
import os


global stopWords
global docId
global documentos
global diccionarioGlobal
global coleccion

stopWords = []
docId = 0
coleccion = {'N' :  0, 'AvgLen':0, 'rutaAbsoluta': ''}  
documentos = {}            #DocId, ruta relativa, longitud, norma.
diccionarioGlobal = {}     # Ni, Idfs, *postings ---> [(doc1,long,peso),(doc2,long,peso),...]


    
def leerStopWords(ruta):
    '''
    Leer stopwords y llenar la lista de stopwords global
    '''
    global stopWords
    
    with open(ruta,"r") as archivo:
        for linea in archivo:
            stopWords.append(linea.rstrip('\n').rstrip('\t').rstrip('\b'))

        
def formatearTexto(ruta):
    '''
    Quita las etiquetas xml para extraer el texto, quita caracteres,convierte a minuscula
    y devuelve lista de palabras sin acentos (Como que hace más de una cosa xd)
    '''
    #Expresiones regulares para quitar las etiquetas: http://carrefax.com/new-blog/2017/11/8/strip-xml-tags-out-of-file
    texto = re.sub(r'<[^<]+>', "",open(ruta,encoding="utf8").read())

    texto = texto.lower()

    caracteres = "!?'-[]()\/''=`,:~}{" #-> caracteres innecesarios que se quitan 
    texto = ''.join(x for x in texto if x not in caracteres)


    texto = deleteAccents(texto)
    return re.split(r'\W+', texto) #Dividir por palabras
    

def deleteAccents(text):
    '''
    Borrar acentos del texto, exceptuando ñ
    #Obtenido de https://ideone.com/YcXaQD (ideone.com)
    '''
    #NFD (Normalization Form Canonical Decomposition) expresion para eliminar diacríticos 
    text = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", text), 0, re.I)

    #NFC (#Normalization Form Canonical Composition) volver a su forma compuesta
    text = normalize( 'NFC', text)

    return text


    
def countWords(words):
    '''
    Recorre las palabras, si no existen con anterioridad las agrega al diccionario y aumenta la frecuencia de cada palabra.
    Diccionario para cada documento
    '''
    global stopWords
    
    frequency = {} # Palabra, frecuencia
    for word in words:
        if  word != '' and word not in stopWords:
            if word in frequency :
                frequency[word] += 1
            else:
                frequency[word] = 1
            
    return frequency

def insertarEndiccionarioGlobal(dicc,docId):
    '''
    Inserta las palabras del diccionario, en el diccionario de la coleccion completa
    '''
    global diccionarioGlobal
    for word in dicc:
        longitud = dicc[word] #Frecuencia
        if word in diccionarioGlobal:
            diccionarioGlobal[word]["Ni"] +=1
        else:
            diccionarioGlobal[word] = dict({'Ni': 1, 'Idf': 0, 'IdfBM25': 0, 'Postings': []})
            
        diccionarioGlobal[word]["Postings"].append([docId,longitud,0])  #Postings de la palabra
        modificarDocumentos(docId,longitud)  #Se aumenta la longitud del documento en general


    return diccionarioGlobal
    

def insertarEnDocumentos(path,docId):
    
    documentos[docId] = dict({'path': str(path), 'length': 0, 'norma': 0})
    
def modificarDocumentos(docId,frecuencia):
    global documentos
    documentos[docId]["length"] += frecuencia

def getFrecuenciaDocumento(docId):
    global documentos
    return documentos[docId]["length"]


def modificarColeccion(longitudTotal):
    global coleccion

    coleccion["AvgLen"] += longitudTotal
    coleccion["N"]+=1  #Aumenta N por cada doc procesado

    
def getNColeccion():
    global coleccion
    return coleccion["N"]


def avgColeccion():
    '''
    Calcular el promedio de longitud de todos los documentos
    '''
    global coleccion
    coleccion['AvgLen'] =  coleccion['AvgLen']/coleccion["N"]



def idf_ijColeccionVect(N, ni):
    '''
    Dado un N y un ni devuelve el resultado del inverse document frequency
    '''
    idf = log(N/ni,2)
    if idf >= 0:
        return idf
    else:
        return 0


def idf_ijColeccionBM25(N, ni):
    '''
    Dado un N y un ni devuelve el resultado del inverse document frequency
    '''
    idf = log((N-ni+0.5)/(ni+0.5),2)
    if idf >= 0:
        return idf
    else:
        return 0
    

def calcularPeso(idf_ij,freq_ij):
    '''
    Calcular el peso de un termino 
    '''

    return log(1+freq_ij,2)*idf_ij



def normas():
    '''
    Una vez que se tiene la suma de los pesos al cuadrado se calcula la raíz 
    '''
    global documentos
    
    for doc in documentos:
        documentos[doc]["norma"] = sqrt(documentos[doc]["norma"])
        


def procesarDiccColeccion(N):
    '''
    Estructura de los Postings: [[docId, freq_ij, peso]]
    '''
    global diccionarioGlobal
    global documentos
    
    
    for word in diccionarioGlobal:
        #calcularIdf_ij 
        ni = diccionarioGlobal[word]["Ni"]
        diccionarioGlobal[word]['Idf'] = idf_ijColeccionVect(N, ni)
        diccionarioGlobal[word]['IdfBM25'] = idf_ijColeccionBM25(N, ni)
        #CalcularPeso
        idf_ij = diccionarioGlobal[word]["Idf"]
        postings = diccionarioGlobal[word]["Postings"]
        for post in postings:
            peso = calcularPeso(idf_ij,post[1])  #Se le pasa el idf y la frecuencia del termino en el documento
            post[2] = peso
            documentos[post[0]]["norma"] = peso**2    #Se va sumando a la norma

    normas()


    #----------------Pruebas----------------------------#
    '''
    a=0
    for word in diccionarioGlobal:
        if a==76:
            print('Palabra:',word)
            print('Ni:',diccionarioGlobal[word]["Ni"])
            print('IdfVect:',diccionarioGlobal[word]["Idf"])
            print('IdfBM25:',diccionarioGlobal[word]["IdfBM25"])
            print('Postings:',diccionarioGlobal[word]["Postings"])
        a+=1
    
    #print(documentos)
    '''
    return diccionarioGlobal
    

def guardarIndice(rutaIndice,coleccion,documentos,diccionarioGlobal):
    if os.path.exists(rutaIndice):
        crearIndice(rutaIndice,coleccion,documentos,diccionarioGlobal)

    else:
        os.makedirs(rutaIndice)
        crearIndice(rutaIndice,coleccion,documentos,diccionarioGlobal)



def crearIndice(rutaIndice,coleccion,documentos,diccionarioGlobal):
    with open(rutaIndice+'/'+'coleccion.json', 'w') as c:
            json.dump(coleccion, c)
    
    with open(rutaIndice+'/'+'documentos.json', 'w') as doc:
            json.dump(documentos, doc)
    
    with open(rutaIndice+'/'+'diccionarioGlobal.json', 'w') as dic:
            json.dump(diccionarioGlobal, dic)
    
def tomarArchivos(rutaColeccion,rutaStopwords,rutaIndice):
    
    global docId
    global documentos
    global diccionarioGlobal
    global coleccion

    rutaColeccion = PurePath(rutaColeccion)
    coleccion['rutaAbsoluta']= str(rutaColeccion)
    leerStopWords(rutaStopwords)
    pathlist = Path(rutaColeccion).glob('**/*.xml')
    
    for path in pathlist:
        docIdentifier = "doc"+str(docId)
        insertarEnDocumentos(path.relative_to(rutaColeccion),docIdentifier)
        texto = formatearTexto(path)
        dicc = countWords(texto)
        insertarEndiccionarioGlobal(dicc,docIdentifier)
        longitudTotal = getFrecuenciaDocumento(docIdentifier)  #Longitud total del documento actual procesado
        modificarColeccion(longitudTotal)                      #Se suma a la longitud de la colecci[on
        docId += 1

    # Calculos de los modelos
    avgColeccion()
    N = getNColeccion()
    procesarDiccColeccion(N)

    guardarIndice(rutaIndice,coleccion,documentos,diccionarioGlobal)
    

