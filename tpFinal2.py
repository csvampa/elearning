from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re

# MODELO

def conexion():
    con = sqlite3.connect("mibase.db")
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS liquidaciones
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             empresa varchar(20) NOT NULL,
             periodo varchar(10),
             pagado real,
             fecha varchar(10),
             comisiones real,
             pagoRecibido varchar(10))
    """
    cursor.execute(sql)
    con.commit()

try:
    conexion()
    crear_tabla()
except:
    print("Hay un error")

def alta(liquidacionId, empresa, periodo, pagado, fecha, comisiones, pagoRecibido, tree):
    cadena = liquidacionId
    patron="^[A-Za-záéíóú]*$"  #regex para el campo cadena
    if(re.match(patron, cadena)):
        print(liquidacionId, empresa, periodo, pagado, fecha, comisiones, pagoRecibido)
        con=conexion()
        cursor=con.cursor()
        data=(liquidacionId, empresa, periodo, pagado, fecha, comisiones, pagoRecibido)
        sql="INSERT INTO liquidaciones(liquidacionId, empresa, periodo, pagado, fecha, comisiones, pagoRecibido) VALUES(?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        print("Estoy en alta todo ok")
        actualizar_treeview(tree)
    else:
        print("error en campo liquidacion")


def consultar():
    print("liquidacion")

def borrar(tree):
    valor = tree.selection()
    print(valor)   #('I005',)
    item = tree.item(valor)
    print(item)    #{'text': 5, 'image': '', 'values': ['daSDasd', '13.0', '2.0'], 'open': 0, 'tags': ''}
    print(item['text'])
    mi_id = item['text']

    con=conexion()
    cursor=con.cursor()
    #mi_id = int(mi_id)
    data = (mi_id,)
    sql = "DELETE FROM productos WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)



def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM liquidaciones ORDER BY id ASC"
    con=conexion()
    cursor=con.cursor()
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))


# VISTA


root = Tk()
root.title("Liquidaciones")
        
titulo = Label(root, text="Registro de Liquidaciones", bg="DarkOrchid3", fg="thistle1", height=1, width=60)
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W+E)

empresa = Label(root, text="Empresa")
empresa.grid(row=1, column=0, sticky=W)
periodo = Label(root, text="Periodo Liquidado")
periodo.grid(row=2, column=0, sticky=W)
pagado = Label(root, text="Monto Pagado")
pagado.grid(row=3, column=0, sticky=W)
fecha = Label(root, text="Fecha de cierre")
fecha.grid(row=4, column=0, sticky=W)
comisiones=Label(root, text="Monto Facturado")
comisiones.grid(row=5, column=0, sticky=W)
pagoRecibido=Label(root, text="Fecha de Pago Recibido")
pagoRecibido.grid(row=6, column=0, sticky=W)

# Defino variables para tomar valores de campos de entrada
a_val, b_val, c_val, d_val, e_val, f_val = StringVar(), StringVar(), DoubleVar(), StringVar(), DoubleVar(), StringVar()
w_ancho = 20

entrada1 = Entry(root, textvariable = a_val, width = w_ancho) 
entrada1.grid(row = 1, column = 1)
entrada2 = Entry(root, textvariable = b_val, width = w_ancho) 
entrada2.grid(row = 2, column = 1)
entrada3 = Entry(root, textvariable = c_val, width = w_ancho) 
entrada3.grid(row = 3, column = 1)
entrada4 = Entry(root, textvariable = d_val, width = w_ancho) 
entrada4.grid(row = 4, column = 1)
entrada5 = Entry(root, textvariable = e_val, width = w_ancho) 
entrada5.grid(row = 5, column = 1)
entrada6 = Entry(root, textvariable = f_val, width = w_ancho) 
entrada6.grid(row = 6, column = 1)

# TREEVIEW

tree = ttk.Treeview(root)
tree["columns"]=("col1", "col2", "col3", "col4", "col5", "col6")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.column("col4", width=200, minwidth=80)
tree.column("col5", width=200, minwidth=80)
tree.column("col6", width=200, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="Empresa")
tree.heading("col2", text="Periodo Liquidado")
tree.heading("col3", text="Monto Pagado")
tree.heading("col4", text="Fecha de cierre")
tree.heading("col5", text="Monto Facturado")
tree.heading("col6", text="Fecha de Pago Recibido")
tree.grid(row=10, column=0, columnspan=4)

boton_alta=Button(root, text="Alta", command=lambda:alta(a_val.get(), b_val.get(), c_val.get(), d_val.get(), e_val.get(), f_val.get(), tree))
boton_alta.grid(row=7, column=1)

boton_consulta=Button(root, text="Consultar", command=lambda:consultar())
boton_consulta.grid(row=8, column=1)

boton_borrar=Button(root, text="Borrar", command=lambda:borrar(tree))
boton_borrar.grid(row=9, column=1)
root.mainloop()