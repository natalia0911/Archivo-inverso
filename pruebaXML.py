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
    return quitarPreposiciones(texto)
    
    #TXT de prueba donde muestra como queda(Faltan detalles) doc prueba: apx-authors.xml
    #with open("output.txt", "w") as f:
    #    f.write(texto)


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


def quitarPreposiciones(texto):

    #Aqui hacer algo para quitar las presiones necesarias
    #De momento separa en palabras
    return re.split(r'\W+', texto)     #Dividir por palabras

    
def countWords(words):
    '''
    Recorre las palabras, si no existen con anterioridad las agrega al dicciionario y aumenta la frecuencia de cada palabra.
    Diccionario para cada documento
    '''
    frequency = {} # Palabra, frecuencia
    for word in words:
        if word in frequency and word != '':
            frequency[word] +=1
        else:
            frequency[word]=1
            
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
            diccionarioGlobal[word] = dict({'Ni': 1, 'Idf': 0, 'Postings': []})
            
        diccionarioGlobal[word]["Postings"].append([docId,longitud,0])  #Postings de la palabra
        modificarDocumentos(docId,longitud)  #Se aumenta la longitud del documento en general


    return diccionarioGlobal
    

def insertarEnDocumentos(path,docId):
    
    documentos[docId] = dict({'path': path, 'length': 0, 'norma': 0})
    
def modificarDocumentos(docId,frecuencia):
    global documentos
    documentos[docId]["length"] += frecuencia

def getFrecuenciaDocumento(docId):
    global documentos
    return documentos[docId]["length"]


def modificarColeccion(longitudTotal):
    global coleccion
    coleccion['AvgLen'] += longitudTotal
    coleccion["N"]+=1  #Aumenta N por cada doc procesado
    
    

def tomarArchivos():
    global docId
    
    #ruta = input("Ingrese la ruta del archivo: ")
    pathlist = Path("D:/2 SEMESTRE 2021/RIT/PROYECTOS/Proyecto 1/Archivo-inverso/xml-es").glob('**/*.xml')
    for path in pathlist:
        docIdentifier = "doc"+str(docId)
        insertarEnDocumentos(path,docIdentifier)
        texto = formatearTexto(path)
        dicc = countWords(texto)
        diccGlobal = insertarEndiccionarioGlobal(dicc,docIdentifier)
        longitudTotal = getFrecuenciaDocumento(docIdentifier)
        modificarColeccion(longitudTotal)
        #print(diccGlobal)
        docId += 1

        

if __name__ == '__main__':

    #Luego vemos como pasarlo a bonito
    global docId
    global documentos
    global diccionarioGlobal
    global coleccion
    
    docId = 0
    coleccion = {'N' :  0, 'AvgLen':0, 'rutaAbsoluta': ''}  
    documentos = {}            #DocId, ruta relativa, longitud, norma.
    diccionarioGlobal = {}     # Ni, Idfs, *postings ---> [(doc1,long,peso),(doc2,long,peso),...]
    tomarArchivos()

