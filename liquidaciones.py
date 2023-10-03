from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re

# MODELO

def conexion():
    con = sqlite3.connect("mibase.db")
    return con

def crearTabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS liquidaciones
             (id INTEGER PRIMARY KEY,
             empresa varchar(20) NOT NULL,
             detalle varchar(10),
             pagado real,
             fecha DATE,
             comisiones real,
             pagoRecibido varchar(10))
    """
    cursor.execute(sql)
    con.commit()
try:
    conexion()
    crearTabla() 
except:
    showerror('Error','Error de conexión')


def actualizarTreeview(tree):
    records = tree.get_children()
    for element in records:
        tree.delete(element)

    sql = 'SELECT * FROM liquidaciones ORDER BY id ASC'
    con=conexion()
    cursor=con.cursor()
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        tree.insert('', 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))
    con.close()
      

def alta(id, empresa, detalle, pagado, fecha, comisiones, pagoRecibido, tree):
    if not id or not empresa or not detalle or not fecha:
        showerror('Error', 'Los campos ID, Empresa, Detalle y Fecha son obligarios.')
        return
    
    patronFecha = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
    if not re.match(patronFecha, fecha):
        showerror('Error', 'El formato de fecha ingresado es incorrecto. Utilice dd/mm/yyyy.')
        return

    con = conexion()
    cursor = con.cursor()
    
    # Verifica si el ID ya existe en la base de datos
    cursor.execute('SELECT id FROM liquidaciones WHERE id = ?', (id,))
    existeID = cursor.fetchone()
    
    if existeID:
        showerror('Error', 'El ID ya existe en la base de datos, ingrese un valor diferente.')
        con.close()
        return
    else:
        data = (id, empresa, detalle, pagado, fecha, comisiones, pagoRecibido)
        sql = 'INSERT INTO liquidaciones(id, empresa, detalle, pagado, fecha, comisiones, pagoRecibido) VALUES (?, ?, ?, ?, ?, ?, ?)'
        cursor.execute(sql, data)
        con.commit()
        actualizarTreeview(tree)
        showinfo('Exito', 'Liquidacion cargada con éxito.')
    # Limpia los campos de entrada después de la inserción exitosa
    for var in (id_val, emp_val, det_val, pago_val, fecha_val, comis_val, pagoRec_val):
        var.set('')

    con.close()

def filtrar(empresa, fecha):
    con=conexion()
    cursor=con.cursor()
    sql = 'SELECT * FROM liquidaciones WHERE 1=1'
    params = []
    
    if empresa:
        sql += ' AND empresa LIKE :empresa'
        params.append(f"%{empresa}%") 
    
    if fecha:
        try:
            mes, anio = fecha.split('/')
            mes = int(mes)
            anio = int(anio)
            sql += ' AND substr(fecha, -7) LIKE :fecha'
            params.append(f'%{mes:02d}/{anio}%') 

        except ValueError:
            showerror('Error', 'Ingrese una fecha válida en formato mm/aaaa.')
            con.close()
            return
            
    cursor.execute(sql, params)
    resultado = cursor.fetchall()

    for row in tree.get_children():
        tree.delete(row)
    
    for fila in resultado:
        tree.insert('', 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))

    for var in (filtroemp_val, filtromesyanio_val):
        var.set('') 
    
    con.close()

def calcularTotales(tree):
    totaloPagado = 0
    totalFacturado = 0

    for row in tree.get_children():
        fila = tree.item(row)["values"]
        
        totaloPagado += float(fila[2])
        totalFacturado += float(fila[4])

    filaTotales = ('Total', '', totaloPagado, '', totalFacturado)
    tree.insert('', 'end', values=filaTotales)

def borrar(tree):
    valor = tree.selection() 
    if not valor:
        showinfo('Borrar', 'Por favor, seleccione una fila para eliminar.')
        return
    item = tree.item(valor)
    mi_id = item['text']

    con = conexion()
    cursor = con.cursor()
    mi_id = int(mi_id)
    data = (mi_id,)
    
    # Obtengo los datos antes de eliminar la fila
    cursor.execute('SELECT * FROM liquidaciones WHERE id = ?;', data)
    filaEliminada = cursor.fetchone()

    sql = 'DELETE FROM liquidaciones WHERE id = ?;'
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)
    
    # Muestro los datos de la fila eliminada
    if filaEliminada:
        showinfo('Cambios Realizados', f'Elemento eliminado con éxito.\nDatos eliminados: {filaEliminada}')
    else:
        showinfo('Cambios Realizados', 'Elemento eliminado con éxito. Los datos no se pudieron recuperar.')


def editar(tree):
    seleccion = tree.selection()
    if not seleccion:
        showinfo('Editar', 'Por favor, seleccione una fila para editar:')
        return
    
    item = tree.item(seleccion)
    filaValores = [item['text']] + item['values']
    filaID = item['text']  

    nombresCampos = ['ID: Ingrese el ID de la fila a editar.', 'Empresa', 'Detalle', 'Monto Pagado', 'Fecha de cierre:\n(dd/mm/yyyy)', 'Monto Facturado', 'Pago Recibido']

    cuadrosEntrada = []
    nuevasVariables = []
    etiquetas = []

    for i, (nombre, valor) in enumerate(zip(nombresCampos, filaValores)):
        etiqueta = Label(root, text=nombre)
        etiqueta.grid(row=i+1, column=2, sticky=W)
        etiquetas.append(etiqueta)

        var = StringVar(value=valor)
        
        cuadro = Entry(root, textvariable=var, width=w_ancho)
        cuadro.grid(row=i+1, column=2)
        
        cuadrosEntrada.append(cuadro)
        nuevasVariables.append(var)

    def guardarEdicion():
        nuevosValores = [nuevasVariables[0].get()] + [var.get() for var in nuevasVariables[1:]]  # Excluir el primer valor que es el ID
        fecha = nuevosValores[4]
        patronFecha = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
        montoPagado = nuevosValores[3]
        montoFacturado = nuevosValores[5]
        
        if not re.match(patronFecha, fecha):
           showerror('Error', 'El formato de fecha ingresado es incorrecto. Utilice dd/mm/yyyy.')
           return
        
        if not montoPagado.replace('.', '', 1).isdigit() or not montoFacturado.replace('.', '', 1).isdigit():
            showerror('Error', 'Los valores de monto pagado o monto facturado deben ser numéricos.')
            return
        
        if not nuevosValores[0] or not nuevosValores[1] or not nuevosValores[2] or not nuevosValores[4]:
            showerror('Error', 'Los campos ID, Empresa, Detalle y Fecha son obligatorios.')
            return
        
        con = conexion()
        cursor = con.cursor()
        try:
            sql = 'UPDATE liquidaciones SET id=?, empresa=?, detalle=?, pagado=?, fecha=?, comisiones=?, pagoRecibido=? WHERE id=?'
            data = tuple(nuevosValores) + (filaID,) 
        
            cursor.execute(sql, data)
            con.commit()
            actualizarTreeview(tree)
            showinfo('Cambios Realizados', 'Los cambios se han guardado exitosamente.')
        except Exception as e:
            showerror('Error', f'Error al guardar cambios: {str(e)}')
        finally:
            con.close()
        cancelarEdicion()

    def cancelarEdicion():
        for cuadro, etiqueta in zip(cuadrosEntrada, etiquetas):
            cuadro.grid_remove()
            etiqueta.grid_remove()
        botonGuardar.grid_remove()
        botonCancelar.grid_remove()

    botonGuardar = Button(root, text='Guardar', command=guardarEdicion)
    botonGuardar.grid(row=7, column=2, pady=5, padx=(100, 50), sticky=E)

    botonCancelar = Button(root, text='Cancelar Edición', command=cancelarEdicion)
    botonCancelar.grid(row=8, column=2, pady=5, padx=(100, 50), sticky=E)
    

# VISTA

root = Tk()
root.title('Liquidaciones')
        
titulo = Label(root, text='Registro de Liquidaciones', bg='DarkOrchid3', fg='thistle1', height=1, width=60)
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W+E)

id = Label(root, text='ID: Ingrese un ID único:')
id.grid(row=1, column=0, sticky=W, padx=5)
empresa = Label(root, text='Empresa:')
empresa.grid(row=2, column=0, sticky=W, padx=5)
detalle = Label(root, text='Detalle:')
detalle.grid(row=3, column=0, sticky=W, padx=5)
pagado = Label(root, text='Monto Pagado:')
pagado.grid(row=4, column=0, sticky=W, padx=5)
fecha = Label(root, text='Fecha de cierre:\n(dd/mm/yyyy)')
fecha.grid(row=5, column=0, sticky=W, padx=5)
comisiones=Label(root, text='Monto Facturado:')
comisiones.grid(row=6, column=0, sticky=W, padx=5)
pagoRecibido=Label(root, text='Pago Recibido:')
pagoRecibido.grid(row=7, column=0, sticky=W, padx=5)

'''
Defino variables para tomar valores de campos de entrada
'''
id_val, emp_val, det_val, pago_val, fecha_val, comis_val, pagoRec_val = IntVar(), StringVar(), StringVar(), DoubleVar(), StringVar(), DoubleVar(), StringVar()
w_ancho = 20

entrada1 = Entry(root, textvariable = id_val, width = w_ancho) 
entrada1.grid(row = 1, column = 0)
entrada2 = Entry(root, textvariable = emp_val, width = w_ancho) 
entrada2.grid(row = 2, column = 0)
entrada3 = Entry(root, textvariable = det_val, width = w_ancho) 
entrada3.grid(row = 3, column = 0)
entrada4 = Entry(root, textvariable = pago_val, width = w_ancho) 
entrada4.grid(row = 4, column = 0)
entrada5 = Entry(root, textvariable = fecha_val, width = w_ancho) 
entrada5.grid(row = 5, column = 0)
entrada6 = Entry(root, textvariable = comis_val, width = w_ancho) 
entrada6.grid(row = 6, column = 0)
entrada7 = Entry(root, textvariable = pagoRec_val, width = w_ancho) 
entrada7.grid(row = 7, column = 0)

filtroEmpresa = Label(root, text='Buscar por Empresa')
filtroEmpresa.grid(row=1, column=1, sticky=W)
filtromesyanio = Label(root, text='Buscar por Mes\n(mm/yyyy)')
filtromesyanio.grid(row=2, column=1, sticky=W)

filtroemp_val, filtromesyanio_val = StringVar(), StringVar()
w_ancho = 20

inputEmpresa = Entry(root, textvariable = filtroemp_val, width = w_ancho)
inputEmpresa.grid(row=1, column=1)
filtromesyanio = Entry(root, textvariable= filtromesyanio_val, width=w_ancho)
filtromesyanio.grid(row=2, column=1)


# TREEVIEW

if __name__ == '__main__':

    tree = ttk.Treeview(root)
    tree['columns']=('col1', 'col2', 'col3', 'col4', 'col5', 'col6')
    tree.column('#0', width=90, minwidth=50, anchor=W)
    tree.column('col1', width=200, minwidth=80)
    tree.column('col2', width=200, minwidth=80)
    tree.column('col3', width=200, minwidth=80)
    tree.column('col4', width=200, minwidth=80)
    tree.column('col5', width=200, minwidth=80)
    tree.column('col6', width=200, minwidth=80)
    tree.heading('#0', text='ID')
    tree.heading('col1', text='Empresa')
    tree.heading('col2', text='Detalle')
    tree.heading('col3', text='Monto Pagado')
    tree.heading('col4', text='Fecha de cierre')
    tree.heading('col5', text='Monto Facturado')
    tree.heading('col6', text='Pago Recibido')
    tree.grid(row=10, column=0, columnspan=3, pady=10, padx=5)

    actualizarTreeview(tree)

botonCargar=Button(root, text='Cargar', command=lambda:alta(id_val.get(), emp_val.get(), det_val.get(), pago_val.get(), fecha_val.get(), comis_val.get(), pagoRec_val.get(), tree))
botonCargar.grid(row=8, column=0, pady=5)

botonFiltrar=Button(root, text='Filtrar', command=lambda:filtrar(filtroemp_val.get(), filtromesyanio_val.get()))
botonFiltrar.grid(row=4, column=1, pady=5, padx=1)

botonEliminarFiltro=Button(root, text='Eliminar Filtro', command=lambda:actualizarTreeview(tree))
botonEliminarFiltro.grid(row=5, column=1, columnspan=1, pady=5, padx=1)

botonCalcularTotales=Button(root, text='Calcular Totales', command=lambda:calcularTotales(tree))
botonCalcularTotales.grid(row=6, column=1, pady=5, padx=1)

botonBorrar=Button(root, text='Borrar Elemento Seleccionado', command=lambda:borrar(tree))
botonBorrar.grid(row=9, column=1, pady=5, columnspan=1)

botonEditar=Button(root, text='Editar Elemento Seleccionado', command=lambda:editar(tree))
botonEditar.grid(row=9, column=2, pady=5, columnspan=1)

root.mainloop()