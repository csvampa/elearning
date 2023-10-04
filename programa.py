eleccion = input("Para iniciar ingrese 'i', para finalizar ingrese 'f': ")
el_id=0
liquidacion={}
totalPagado = 0
totalFacturado = 0
if eleccion == "i":
    valor=True
else:
    valor=False

# VISTA

def menu():
    print("\n Elija una opción: ")
    print("    (a) Agregar liquidacion")
    print("    (e) Eliminar liquidacion")
    print("    (l) Listar liquidaciones")
    print("    (m) Modificar liquidacion")
    print("    ó cualquier otra tecla para salir")
    global valor
    global eleccion
    eleccion = input()
    if eleccion=="a" or eleccion=="e" or eleccion=="l" or eleccion=="m":
        valor=True
        print("ingresada")
    else:
        valor=False
        print("Chau")

menu()

# MODELO

def alta(empresa, periodo, pagado, fecha, comisiones, pagoRecibido): 
    global totalPagado
    global totalFacturado
    global el_id
    global liquidacion

    totalPagado = totalPagado + float(pagado)
    totalFacturado = totalFacturado + float(comisiones)
    liquidacion[el_id]= {'empresa':empresa, 'periodo':periodo, 'pagado':pagado,'fecha':fecha, 'comisiones':comisiones, 'pagoRecibido':pagoRecibido }
    el_id+=1
    print("Estoy en alta")

def borrar(id_borrar): 
    global totalPagado
    global totalFacturado
    global el_id
    print(liquidacion[id_borrar])

    totalPagado = totalPagado - float((liquidacion[id_borrar]['pagado']))
    totalFacturado = float(totalFacturado) - float((liquidacion[id_borrar]['comisiones']))
    del liquidacion[id_borrar]
    print("Estoy en borrar")
    
def listar(): 
    for x in liquidacion:
        print("Empresa: ", x[0], "Periodo Liquidado:", x[2], "Monto Pagado: ", x[3], "Fecha de liquidacion: ", x[4], "Comisiones: ", x[5], "PagoRecibido: ", x[6])
#     global liquidacion
#     global totalPagado
#     global totalFacturado

#     print(liquidacion)
#     print("Total Pagado: ", totalPagado)
#     print("Total Facturado: ", totalFacturado)
#     print("Estoy en listar")

def modificar(id_modificar, pagado, comisiones): 
    global liquidacion
    global totalPagado
    global totalFacturado
    pagoRegistrado = float((liquidacion[id_modificar]['pagado']))
    liquidacion[id_modificar]['pagado']=pagado
    pagoModificado = float((liquidacion[id_modificar]['pagado']))
    totalPagado = totalPagado + pagoModificado - pagoRegistrado

    comisionesRegistradas = float((liquidacion[id_modificar]['comisiones']))
    liquidacion[id_modificar]['comisiones']=comisiones
    comisionesModificadas = float((liquidacion[id_modificar]['pagado']))
    totalFacturado = totalFacturado + comisionesModificadas - comisionesRegistradas
   
    print("Estoy en modificar")

# CONTROLADOR

while valor == True:
    print("eleccion: ", eleccion)

    if eleccion=='a':
        empresa = input("Ingrese el nombre de la Empresa:")
        periodo = input("Ingrese el período liquidado:")
        pagado = input("Ingrese el monto pagado:")
        fecha = input("Ingrese la fecha de liquidacion:")
        comisiones = input("Ingrese el monto facturado por comisiones:")
        pagoRecibido = input("Ingrese la fecha del pago recibido:")
        alta(empresa, periodo, pagado, fecha, comisiones, pagoRecibido)
        eleccion = input("Para agregar otra liquidacion ingrese 'i', para finalizar ingrese cualquier otro caracter: ")
        if eleccion == "i":
            valor=True
        else:
            valor=False
    elif eleccion=='e':
        id_borrar = input("Ingrese el id del elemento a borrar: ")
        borrar(int(id_borrar))
        print("Total Pagado: ", totalPagado)
        print("Total Facturado: ", totalFacturado)
    elif eleccion=='l':
        print(liquidacion)
        print("Total Pagado: ", totalPagado)
        print("Total Facturado: ", totalFacturado)
        print("Estoy en listar")
    elif eleccion=='m':
        id_modificar, pagado = input("Ingrese el id y el nuevo monto pagado: ").split()
        id_modificar, comisiones = input("Ingrese el id y el nuevo monto facturado: ").split()
        modificar(int(id_modificar), float(pagado), float(comisiones))
        print("Total Pagado: ", totalPagado)
        print("Total Facturado: ", totalFacturado)
    else:
        break

    menu()
    """producto, cantidad, precio = input("Ingrese el nombre la cantidad de producto en kg y el precio separado por espacio: ").split()
    total = total + float(cantidad)*float(precio)
    compra.append([producto, cantidad, precio])
    eleccion = input("Para agregar otro producto ingrese 'i', para finalizar ingrese cualquier otro caracter: ")
    if eleccion == "i":
        valor=True
    else:
        valor=False"""
#print("El costo total de lo comprado es: ", total)
#print(compra)