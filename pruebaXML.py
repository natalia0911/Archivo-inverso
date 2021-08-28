
import re
from unicodedata import normalize

ruta = input("Ingrese la ruta del archivo: ")
print(ruta)

#Expresiones regulares para quitar las etiquetas: http://carrefax.com/new-blog/2017/11/8/strip-xml-tags-out-of-file
texto = re.sub(r'<[^<]+>', "",open(ruta,encoding="utf8").read())


texto = texto.lower()

caracteres = "!?'-[]()\/''=`,:~}{" #-> caracteres innecesarios que se quitan 
texto = ''.join(x for x in texto if x not in caracteres)

#Obtenido de https://ideone.com/YcXaQD (ideone.com)
#Quita las tildes y otros acentos, con excepcion de la ñ
texto = re.sub( r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", texto), 0, re.I)

texto = normalize('NFC',texto)

#TXT de prueba donde muestra como queda(Faltan detalles) doc prueba: apx-authors.xml
with open("output.txt", "w") as f:
    f.write(texto)


