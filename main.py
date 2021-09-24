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
    #buscar,C:\Users\javir\Desktop\TEC Javi\RIT\Proyecto1_Final\index2,vec,qvec_imp,20,impuestos y depreciacion
    #buscar,C:\Users\javir\Desktop\TEC Javi\RIT\Proyecto1_Final\index2,bm25,qbm25_conf,60,configuración de un servidor de correo
    #indizar,C:\Users\javir\Desktop\TEC Javi\RIT\Proyecto1_Final\Archivo-inverso\xml-es,C:\Users\javir\Desktop\TEC Javi\RIT\Proyecto1_Final\Archivo-inverso\StopWords.txt,index2
    comando = input("Ingrese el comando(parametros con comas seguidas): ")
    elegirComando(comando)


