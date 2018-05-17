from xlrd import open_workbook
import random
from io import StringIO
import io

def manejar_excel(file):
    #input = StringIO()
    #input.write(file.decode('base64'))
    hoja = open_workbook(file_contents=file.read())
    elementos = []
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    contrasena = ""
    numero_caracteres_contrasena = 6
    for h in hoja.sheets():
        numero_filas = h.nrows
        numero_columnas = 3
        for row in range(1, numero_filas):
            valores = []
            for colum in range(numero_columnas):
                valor = (h.cell(row,colum).value)
                try:
                    valor = str(int(valor))
                except ValueError:
                    pass
                finally:
                    valores.append(valor)
            for c in range(numero_caracteres_contrasena):
                contrasena += random.choice(caracteres)
            valores.append(contrasena)
            elementos.append(valores)
            contrasena = ""
    return elementos

#manejar_excel("C:/Users/user/Documents/Juegos/Usuarios.xlsx")




            
