####################################################
#Version de Python 3.9.2
#Creado el 7/09/2021
#Ultima modificación 13/09/2021
####################Autores#########################
#Javier Rivera
#Natalia Vargas Reyes
#Proyecto 1, Recuperación de la información textual
####################################################


import Indizacion
import busqueda
import Inspeccion

def elegirComando(comando):

    comandos = comando.split(",")
    
    if comandos[0]=="indizar":
        coleccion = comandos[1]
        stopwords = comandos[2]
        indice = comandos[3]
        Indizacion.tomarArchivos(coleccion,stopwords,indice)
        return
    
    elif comandos[0]=="buscar":
        indice = comandos[1]
        tipo = comandos[2]  #bm25 0 vec
        prefijo = comandos[3] #arch. salida
        numDocs = int(comandos[4]) #cant de doc en escalafon mostrados en el .html
        consulta = comandos[5] #texto que se va a consultar
        busqueda.buscarConsulta(indice,tipo,prefijo, numDocs, consulta)
        return
    
    elif comandos[0]=="mostrar":
        indice = comandos[1]
        tipo = comandos[2]  #ter o doc
        dato = comandos[3]
        print(Inspeccion.consultar(indice,tipo,dato))
        return 
    
    else:
        print("El comando no existe\n")
        return




if __name__ == '__main__':
    #indizar,C:\Users\javir\Desktop\TEC Javi\RIT\Proyecto1\Archivo-inverso\xml-es,C:\Users\javir\Desktop\TEC Javi\RIT\Proyecto1\Archivo-inverso\StopWords.txt,coleccion
    #buscar,C:\Users\javir\Desktop\TEC Javi\RIT\Proyecto1_Final\coleccion,vec,qvec_imp,20,impuestos y depreciacion
    #buscar,C:\Users\javir\Desktop\TEC Javi\RIT\Proyecto1_Final\coleccion,bm25,qbm25_imp,20,impuestos y depreciacion
    #indizar,D:/2 SEMESTRE 2021/RIT/PROYECTOS/Proyecto 1/Archivo-inverso/xml-es,D:/2 SEMESTRE 2021/RIT/PROYECTOS/Proyecto 1/Archivo-inverso/StopWords.txt,D:/2 SEMESTRE 2021/RIT/PROYECTOS/Proyecto 1/Archivo-inverso/Indice
    #mostrar,D:/2 SEMESTRE 2021/RIT/PROYECTOS/Proyecto 1/Archivo-inverso/Indice,ter,tantos
    #REVISAR ESTE
    #mostrar,D:/2 SEMESTRE 2021/RIT/PROYECTOS/Proyecto 1/Archivo-inverso/Indice,doc,D:\\2 SEMESTRE 2021\\RIT\\PROYECTOS\\Proyecto 1\\Archivo-inverso\\xml-es\\xml-es\\applets\\whereami-ug.xml
    #buscar,D:/2 SEMESTRE 2021/RIT/PROYECTOS/Proyecto 1/Archivo-inverso/Indice,vec,prueba,4,autores y evolution

    comando = input("Ingrese el comando(parametros con comas seguidas): ")
    elegirComando(comando)

    '''
    indice = 'D:/2 SEMESTRE 2021/RIT/PROYECTOS/Proyecto 1/Archivo-inverso/Indice'
    dato = "D:\\2 SEMESTRE 2021\\RIT\\PROYECTOS\\Proyecto 1\\Archivo-inverso\\xml-es\\xml-es\\applets\\whereami-ug.xml"
    print(Inspeccion.consultar(indice,'doc',dato))

    buscarConsulta(ruta,'vec','prueba',4,'autores y evolution')
    '''
