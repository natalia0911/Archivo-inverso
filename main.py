####################################################
#Version de Python 3.9.2
#Creado el 7/09/2021
#Ultima modificación
####################Autores#########################
#Javier Rivera
#Natalia Vargas Reyes
#Proyecto 1, Recuperación de la información textual
####################################################


import Indizacion


def elegirComando(comando):

    comandos = comando.split(",")
    
    if comandos[0]=="indizar":
        coleccion = comandos[1]
        stopwords = comandos[2]
        indice = comandos[3]
        print(comandos)
        Indizacion.tomarArchivos(coleccion,stopwords,indice)
        return
    
    if comandos[0]=="buscar":
        indice = comandos[1]
        tipo = comandos[2]  #bm25 0 vec
        prefijo = comandos[3] #arch. salida
        numDocs = int(comandos[4]) #cant de doc en escalafon mostrados en el .html
        consulta = comandos[5] #texto que se va a consultar
        return
    else:
        print("El comando no existe\n")
        return



    

 








if __name__ == '__main__':
    #indizar,C:\Users\javir\Desktop\TEC Javi\RIT\Proyecto1\Archivo-inverso\xml-es,C:\Users\javir\Desktop\TEC Javi\RIT\Proyecto1\Archivo-inverso\StopWords.txt,coleccion
    #
    comando = input("Ingrese el comando(parametros con comas): ")
    elegirComando(comando)