import json
import math
import operator
from datetime import datetime
import re
import Indizacion
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

    return dict

def simVec2(similitudes, pesosConsulta,documentos):
    for doc in similitudes:
        print(str(doc)+'   '+str(similitudes[doc])+'  '+str(normaConsulta(pesosConsulta))+'   '+str(documentos[doc]['norma']))
        similitudes[doc]= similitudes[doc]/(normaConsulta(pesosConsulta)*documentos[doc]['norma'])
        print(str(similitudes[doc]))
    return similitudes
    
def simVec(pesosTermino, pesosConsulta, terminos, documentos):
    #similitud vectorial 
    
    similitudes = crearDict(pesosTermino)
    for termino in terminos:
        if termino in pesosTermino:
            for w in pesosTermino[termino]:
                print('Similitud '+w[0]+' =' +str(w[1])+'   '+str(pesosConsulta[termino]))
                
                similitudes[w[0]]+=w[1]*pesosConsulta[termino]

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
    print(similitudes)
    pos = 1
    for doc in similitudes: 
        escalafon.write(str(pos)+". "+str(doc)+'\n')
        pos+=1
    escalafon.close()

def crearHTML(similitudes,prefijo,numDocs,documentos,consulta):
    html = open(prefijo+'.html','w')
    html.write('<html>\n')
    html.write('<head>\n<title>Primeros Documentos del Escalafon</title>\n</head>\n')
    html.write('<body>\n')
    html.write(datetime.today().strftime('%A, %B %d, %Y %H:%M:%S')+'\n'+'<br>')
    html.write('Consulta: '+ consulta+'\n\n\n'+'<br>')
    pos = 1
    for doc, sim in similitudes:
        if numDocs != 0:
           html.write('<H1>'+doc+'</H1>')
           html.write('<P>') 
           html.write('Posicion: '+str(pos)+'\n'+'<br>')
           html.write('Similitud: '+str(sim)+'\n'+'<br>')
           ruta = documentos[doc]['path']
           html.write('Ruta: '+ruta+'\n\n'+'<br>')
           texto = re.sub(r'<[^<]+>', "",open(ruta,encoding="utf8").read())
           caracteres = texto[:200]
           html.write('Primeros 200 caracteres: \n'+caracteres+'\n\n\n')
           html.write('</P>')
           pos = pos+1
           numDocs = numDocs -1
        else:
            html.write('</body>\n')
            html.write('</html>\n')
            html.close()
            return
    html.write('</body>\n')
    html.write('</html>\n')
    html.close()
    return


def obtenerDocs(consultas,diccionarioGlobal):
    resultado = {}
    for consulta in consultas:
        frec=[]
        if consulta in diccionarioGlobal:
            for peso in diccionarioGlobal[consulta]['Postings']:
                doc = []
                doc.append(peso[0])
                doc.append(peso[1])
                frec.append(doc)   
            resultado[consulta] = frec       
    return resultado



def simBM25(docs,coleccion,documentos,diccionarioGlobal):
    similitudes = crearDict(docs)
    for termino in docs:
        for doc in docs[termino]:
            similitudes[doc[0]]+= diccionarioGlobal[termino]['IdfBM25']*((doc[1]*(1.2+1))/(doc[1]+1.2*(1-0.75+1*(documentos[doc[0]]['length']/coleccion['AvgLen']))))

    return similitudes


def buscarConsulta(dir,tipo,prefijo,numDocs,consulta):
    
    coleccion = json.load(open(dir+'/'+'coleccion.json','r'))
    diccionarioGlobal = json.load(open(dir+'/'+'diccionarioGlobal.json','r'))
    documentos = json.load(open(dir+'/'+'documentos.json','r'))
    
    terminos = consulta.lower()
    terminos = Indizacion.deleteAccents(terminos)

    terminos = terminos.split()
    
    similitudes = {}

    print(terminos)

    if tipo == 'vec': 
        pesosTermino = obtenerPesos(diccionarioGlobal,terminos) #Dicc de terminos donde traen sus docs y pesos

        pesosConsulta = obtenerPesosConsulta(terminos,pesosTermino,coleccion)    
    
        print(pesosConsulta)
        print(pesosTermino)
        similitudes = simVec(pesosTermino,pesosConsulta,terminos,documentos)
        print(similitudes)

        similitudes = sorted(similitudes.items(),key=operator.itemgetter(1),reverse=True)#Orden descendente
        crearEscalafon(similitudes,prefijo)
        crearHTML(similitudes,prefijo,numDocs,documentos,consulta)
        return

    elif tipo == 'bm25':
        docsFrec = obtenerDocs(terminos,diccionarioGlobal)
        similitudes = simBM25(docsFrec,coleccion,documentos,diccionarioGlobal)

        similitudes = sorted(similitudes.items(),key=operator.itemgetter(1),reverse=True)#Orden descendente
        crearEscalafon(similitudes,prefijo)
        crearHTML(similitudes,prefijo,numDocs,documentos,consulta)
        return
    
    else:
        print('No existe este tipo de busqueda.\n')
    


#Parametro -> ruta del directorio donde se encuentran los json

if __name__ == '__main__':
    ruta = input('ingrese el dir de indice: ')
    buscarConsulta(ruta,'vec','prueba',4,'autores y evolution')
