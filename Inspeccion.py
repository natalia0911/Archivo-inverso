
import json

   
def consultar(indice,tipo,dato):

    if tipo == 'ter':
        
        diccionarioGlobal = json.load(open(indice+'/'+'diccionarioGlobal.json','r'))
        queryPostings = ''
        try:
            postings = diccionarioGlobal[dato]['Postings']
            for post in postings:
                queryPostings = 'Postings: ' + '\n\tDocId: ' + post[0] + '\n\tFrecuencia: ' + str(post[1]) + '\n\tPeso: ' + str(post[2])

            query = 'Ni: ' + str(diccionarioGlobal[dato]['Ni']) + '\nIdf vectorial: ' + str(diccionarioGlobal[dato]['Idf'])+ \
            '\nIdf BM25: ' + str(diccionarioGlobal[dato]['IdfBM25']) + '\n' + queryPostings
            return query
        
        except KeyError:
            return 'Término no existente'


    elif tipo == 'doc':
        
        documentos = json.load(open(indice+'/'+'documentos.json','r'))
        query = ''
        for docId in documentos:
            if documentos[docId]['path'] == dato:
                query = 'Id del documento: ' + docId + '\nLongitud: ' + str(documentos[docId]['length']) + '\nNorma: ' + str(documentos[docId]['norma'])
                pass
        if query != '':
            return query
        else:
            print('Query vacia')
            return 'Ruta de documento no existente'

    else:
        return 'Consulta inválida'

    
