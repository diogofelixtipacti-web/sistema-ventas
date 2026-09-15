import os

archivo_inv = "productos.txt"
archivo_ven = "registro_ventas.txt"


def preparar_archivos():

    if not os.path.exists(archivo_inv):
        with open(archivo_inv, "w") as archivo:
            archivo.write("")

    if not os.path.exists(archivo_ven):
        with open(archivo_ven, "w") as archivo:
            archivo.write("")


def leer_inventario():

    inventario = {}

    try:

        with open(archivo_inv, "r") as archivo:
            datos = archivo.readlines()

        posicion = 0

        while posicion + 3 < len(datos):

            codigo = int(datos[posicion].strip())
            nombre = datos[posicion + 1].strip()
            precio = float(datos[posicion + 2].strip())
            cantidad = int(datos[posicion + 3].strip())

            inventario[codigo] = {
                "nombre": nombre,
                "precio": precio,
                "stock": cantidad
            }

            posicion += 4

    except FileNotFoundError:

        print("No se encontró el archivo.")

    except ValueError:

        print("Se encontró un dato incorrecto.")

    else:

        print("Productos cargados.")

    finally:

        print("Proceso de lectura terminado.")

    return inventario


def leer_ventas():

    ventas = []

    try:

        with open(archivo_ven, "r") as archivo:
            datos = archivo.readlines()

        posicion = 0

        while posicion + 4 < len(datos):

            venta = {
                "codigo": int(datos[posicion].strip()),
                "producto": datos[posicion + 1].strip(),
                "cantidad": int(datos[posicion + 2].strip()),
                "descuento": float(datos[posicion + 3].strip()),
                "total": float(datos[posicion + 4].strip())
            }

            ventas.append(venta)

            posicion += 5

    except FileNotFoundError:

        print("Todavía no existe un historial de ventas.")

    except ValueError:

        print("Hay información incorrecta en ventas.")

    return ventas


def guardar_inventario(inventario):

    try:

        with open(archivo_inv, "w") as archivo:

            for codigo in inventario:

                archivo.write(str(codigo) + "\n")
                archivo.write(inventario[codigo]["nombre"] + "\n")
                archivo.write(str(inventario[codigo]["precio"]) + "\n")
                archivo.write(str(inventario[codigo]["stock"]) + "\n")

    except OSError:

        print("No se pudo guardar los productos.")


def registrar_producto(inventario):

    print("\nREGISTRO DE PRODUCTO")

    try:

        codigo = int(input("Código: ").strip())

        if codigo <= 0:

            print("El código debe ser mayor que cero.")

        elif codigo in inventario:

            print("Ese código ya existe.")

        else:

            nombre = input("Nombre: ").strip().capitalize()

            precio = float(input("Precio: S/. ").strip())

            stock = int(input("Cantidad disponible: ").strip())

            if nombre == "":

                print("Debe colocar un nombre.")

            elif precio < 0 or stock < 0:

                print("Precio y stock no pueden ser negativos.")

            else:

                inventario[codigo] = {
                    "nombre": nombre,
                    "precio": precio,
                    "stock": stock
                }

                guardar_inventario(inventario)

                print("Producto guardado.")

    except ValueError:

        print("Ingrese correctamente los datos.")


def buscar_producto(inventario):

    print("\nBÚSQUEDA DE PRODUCTO")

    try:

        codigo = int(input("Código del producto: ").strip())

        if codigo in inventario:

            producto = inventario[codigo]

            print("\nCódigo:", codigo)
            print("Producto:", producto["nombre"])
            print("Precio: S/.", producto["precio"])
            print("Stock:", producto["stock"])

        else:

            print("No se encontró ese producto.")

    except ValueError:

        print("El código debe ser un número.")


def modificar_producto(inventario):

    print("\nMODIFICAR PRODUCTO")

    try:

        codigo = int(input("Código del producto: ").strip())

        if codigo in inventario:

            print("Producto actual:", inventario[codigo]["nombre"])

            nombre = input("Nuevo nombre: ").strip().capitalize()
            precio = float(input("Nuevo precio: S/. ").strip())
            stock = int(input("Nuevo stock: ").strip())

            if nombre == "":

                print("El nombre está vacío.")

            elif precio < 0 or stock < 0:

                print("No se permiten valores negativos.")

            else:

                inventario[codigo]["nombre"] = nombre
                inventario[codigo]["precio"] = precio
                inventario[codigo]["stock"] = stock

                guardar_inventario(inventario)

                print("Producto modificado.")

        else:

            print("El producto no existe.")

    except ValueError:

        print("Datos incorrectos.")


def mostrar_productos(inventario):

    print("\nLISTA DE PRODUCTOS")

    if len(inventario) == 0:

        print("No hay productos.")

    else:

        for codigo in inventario:

            print("-----------------------")
            print("Código:", codigo)
            print("Nombre:", inventario[codigo]["nombre"])
            print("Precio: S/.", inventario[codigo]["precio"])
            print("Stock:", inventario[codigo]["stock"])


def guardar_venta(venta):

    try:

        with open(archivo_ven, "a") as archivo:

            archivo.write(str(venta["codigo"]) + "\n")
            archivo.write(venta["producto"] + "\n")
            archivo.write(str(venta["cantidad"]) + "\n")
            archivo.write(str(venta["descuento"]) + "\n")
            archivo.write(str(venta["total"]) + "\n")

    except OSError:

        print("No se pudo guardar la venta.")


def vender(inventario, ventas):

    print("\nREGISTRAR VENTA")

    try:

        codigo = int(input("Código del producto: ").strip())

        if codigo not in inventario:

            print("El producto no existe.")

        else:

            producto = inventario[codigo]

            print("Producto:", producto["nombre"])
            print("Precio:", producto["precio"])
            print("Disponible:", producto["stock"])

            cantidad = int(input("Cantidad a vender: ").strip())

            if cantidad <= 0:

                print("Cantidad incorrecta.")

            elif cantidad > producto["stock"]:

                print("No existe suficiente stock.")

            else:

                descuento = float(input("Descuento (%): ").strip())

                if descuento < 0 or descuento > 100:

                    print("Descuento incorrecto.")

                else:

                    subtotal = producto["precio"] * cantidad

                    rebaja = subtotal * descuento / 100

                    total = subtotal - rebaja

                    print("Subtotal: S/.", subtotal)
                    print("Descuento: S/.", rebaja)
                    print("Total: S/.", total)

                    respuesta = input(
                        "¿Realizar venta? (si/no): "
                    ).lower().strip()

                    if respuesta == "si":

                        producto["stock"] = producto["stock"] - cantidad

                        venta = {
                            "codigo": codigo,
                            "producto": producto["nombre"],
                            "cantidad": cantidad,
                            "descuento": descuento,
                            "total": total
                        }

                        ventas.append(venta)

                        guardar_inventario(inventario)

                        guardar_venta(venta)

                        print("Venta realizada.")

                    else:

                        print("Venta anulada.")

    except ValueError:

        print("Ingrese valores válidos.")


def reporte(inventario, ventas):

    print("\nREPORTE")

    cantidad_productos = len(inventario)

    unidades = 0
    valor_stock = 0

    for codigo in inventario:

        unidades += inventario[codigo]["stock"]

        valor_stock += (
            inventario[codigo]["precio"]
            * inventario[codigo]["stock"]
        )

    dinero_ventas = 0

    for venta in ventas:

        dinero_ventas += venta["total"]

    print("Tipos de productos:", cantidad_productos)
    print("Unidades en almacén:", unidades)
    print("Valor del stock: S/.", valor_stock)
    print("Ventas realizadas:", len(ventas))
    print("Total vendido: S/.", dinero_ventas)


def menu_principal():

    preparar_archivos()

    inventario = leer_inventario()

    ventas = leer_ventas()

    opcion = ""

    while opcion != "7":

        print("\n==========================")
        print(" SISTEMA DE VENTAS")
        print("==========================")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Modificar producto")
        print("4. Realizar venta")
        print("5. Ver productos")
        print("6. Ver reporte")
        print("7. Finalizar")

        opcion = input("Opción: ").strip()

        if opcion == "1":

            registrar_producto(inventario)

        elif opcion == "2":

            buscar_producto(inventario)

        elif opcion == "3":

            modificar_producto(inventario)

        elif opcion == "4":

            vender(inventario, ventas)

        elif opcion == "5":

            mostrar_productos(inventario)

        elif opcion == "6":

            reporte(inventario, ventas)

        elif opcion == "7":

            guardar_inventario(inventario)

            print("Cerrando sistema...")

        else:

            print("Opción no válida.")


menu_principal()
