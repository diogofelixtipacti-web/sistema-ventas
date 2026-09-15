import os
import streamlit as st

# Configuración de los archivos de texto (se guardan en el servidor en la nube)
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
        if not os.path.exists(archivo_inv):
            return inventario
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
                "stock": cantidad,
            }
            posicion += 4
    except Exception:
        pass
    return inventario


def leer_ventas():
    ventas = []
    try:
        if not os.path.exists(archivo_ven):
            return ventas
        with open(archivo_ven, "r") as archivo:
            datos = archivo.readlines()
        posicion = 0
        while posicion + 4 < len(datos):
            venta = {
                "codigo": int(datos[posicion].strip()),
                "producto": datos[posicion + 1].strip(),
                "cantidad": int(datos[posicion + 2].strip()),
                "descuento": float(datos[posicion + 3].strip()),
                "total": float(datos[posicion + 4].strip()),
            }
            ventas.append(venta)
            posicion += 5
    except Exception:
        pass
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
        st.error("No se pudo guardar los productos en el archivo.")


def guardar_venta(venta):
    try:
        with open(archivo_ven, "a") as archivo:
            archivo.write(str(venta["codigo"]) + "\n")
            archivo.write(venta["producto"] + "\n")
            archivo.write(str(venta["cantidad"]) + "\n")
            archivo.write(str(venta["descuento"]) + "\n")
            archivo.write(str(venta["total"]) + "\n")
    except OSError:
        st.error("No se pudo guardar la venta.")


# --- INTERFAZ WEB CON STREAMLIT ---
st.set_page_config(page_title="Sistema de Ventas", layout="centered")
preparar_archivos()

# Cargar datos en cada recarga
if "inventario" not in st.session_state:
    st.session_state.inventario = leer_inventario()
if "ventas" not in st.session_state:
    st.session_state.ventas = leer_ventas()

st.title("🏪 Sistema de Gestión de Ventas")

# Menú lateral para cambiar de función
menu = [
    "Agregar Producto",
    "Buscar Producto",
    "Modificar Producto",
    "Realizar Venta",
    "Ver Inventario",
    "Ver Reporte",
]
opcion = st.sidebar.selectbox("Selecciona una opción del menú", menu)

# 1. AGREGAR PRODUCTO
if opcion == "Agregar Producto":
    st.header("📝 Registro de Producto")
    with st.form("form_agregar", clear_on_submit=True):
        codigo = st.number_input("Código:", min_value=1, step=1)
        nombre = st.text_input("Nombre del producto:")
        precio = st.number_input(
            "Precio (S/.):", min_value=0.0, format="%.2f", step=0.5
        )
        stock = st.number_input("Cantidad disponible (Stock):", min_value=0, step=1)
        boton_guardar = st.form_submit_button("Guardar Producto")

        if boton_guardar:
            if nombre.strip() == "":
                st.warning("Debe colocar un nombre válido.")
            elif codigo in st.session_state.inventario:
                st.error("❌ Ese código ya existe en el sistema.")
            else:
                st.session_state.inventario[codigo] = {
                    "nombre": nombre.strip().capitalize(),
                    "precio": precio,
                    "stock": stock,
                }
                guardar_inventario(st.session_state.inventario)
                st.success(
                    f"✅ Producto '{nombre.capitalize()}' guardado con éxito."
                )

# 2. BUSCAR PRODUCTO
elif opcion == "Buscar Producto":
    st.header("🔍 Búsqueda de Producto")
    codigo_buscar = st.number_input(
        "Ingrese el código a buscar:", min_value=1, step=1
    )
    if st.button("Buscar"):
        if codigo_buscar in st.session_state.inventario:
            prod = st.session_state.inventario[codigo_buscar]
            st.info(f"**Código:** {codigo_buscar}")
            st.write(f"**Nombre:** {prod['nombre']}")
            st.write(f"**Precio:** S/. {prod['precio']:.2f}")
            st.write(f"**Stock disponible:** {prod['stock']} unidades")
        else:
            st.error("❌ No se encontró ningún producto con ese código.")

# 3. MODIFICAR PRODUCTO
elif opcion == "Modificar Producto":
    st.header("✏️ Modificar Producto")
    codigo_mod = st.number_input(
        "Código del producto a modificar:", min_value=1, step=1
    )

    if codigo_mod in st.session_state.inventario:
        prod_act = st.session_state.inventario[codigo_mod]
        st.write(f"Modificando actual: **{prod_act['nombre']}**")

        with st.form("form_modificar"):
            nuevo_nombre = st.text_input(
                "Nuevo nombre:", value=prod_act["nombre"]
            )
            nuevo_precio = st.number_input(
                "Nuevo precio (S/.):", min_value=0.0, value=prod_act["precio"]
            )
            nuevo_stock = st.number_input(
                "Nuevo stock:", min_value=0, value=prod_act["stock"]
            )
            boton_modificar = st.form_submit_button("Actualizar")

            if boton_modificar:
                if nuevo_nombre.strip() == "":
                    st.error("El nombre no puede quedar vacío.")
                else:
                    st.session_state.inventario[codigo_mod] = {
                        "nombre": nuevo_nombre.strip().capitalize(),
                        "precio": nuevo_precio,
                        "stock": nuevo_stock,
                    }
                    guardar_inventario(st.session_state.inventario)
                    st.success("✅ Producto actualizado correctamente.")
    else:
        st.caption("Introduce un código válido existente para editarlo.")

# 4. REALIZAR VENTA
elif opcion == "Realizar Venta":
    st.header("💰 Registrar Nueva Venta")
    codigo_vender = st.number_input(
        "Código del producto a vender:", min_value=1, step=1
    )

    if codigo_vender in st.session_state.inventario:
        prod = st.session_state.inventario[codigo_vender]
        st.write(f"🛒 **Producto:** {prod['nombre']} | Precio: S/. {prod['precio']:.2f} | Stock: {prod['stock']}")

        cantidad = st.number_input("Cantidad a vender:", min_value=1, step=1)
        descuento = st.number_input(
            "Descuento (%):", min_value=0.0, max_value=100.0, step=1.0
        )

        subtotal = prod["precio"] * cantidad
        rebaja = subtotal * (descuento / 100)
        total = subtotal - rebaja

        st.markdown(f"**Subtotal:** S/. {subtotal:.2f}")
        st.markdown(f"**Descuento aplicado:** S/. {rebaja:.2f}")
        st.markdown(f"### **Total a Pagar:** S/. {total:.2f}")

        if cantidad > prod["stock"]:
            st.error("❌ No hay suficiente stock disponible.")
        else:
            if st.button("Confirmar y Procesar Venta"):
                st.session_state.inventario[codigo_vender]["stock"] -= cantidad
                nueva_venta = {
                    "codigo": codigo_vender,
                    "producto": prod["nombre"],
                    "cantidad": cantidad,
                    "descuento": descuento,
                    "total": total,
                }
                st.session_state.ventas.append(nueva_venta)

                guardar_inventario(st.session_state.inventario)
                guardar_venta(nueva_venta)
                st.success("🎉 ¡Venta realizada con éxito!")
                st.rerun()
    else:
        st.caption("Escribe el código de un producto existente.")

# 5. VER INVENTARIO
elif opcion == "Ver Inventario":
    st.header("📋 Lista Completa de Productos")
    if len(st.session_state.inventario) == 0:
        st.info("No hay productos registrados en el inventario.")
    else:
        tabla_datos = []
        for cod, datos in st.session_state.inventario.items():
            tabla_datos.append(
                {
                    "Código": cod,
                    "Nombre": datos["nombre"],
                    "Precio": f"S/. {datos['precio']:.2f}",
                    "Stock": datos["stock"],
                }
            )
        st.dataframe(tabla_datos, use_container_width=True)

# 6. VER REPORTE
elif opcion == "Ver Reporte":
    st.header("📊 Reporte General del Negocio")

    tipos_productos = len(st.session_state.inventario)
    unidades_totales = sum(
        p["stock"] for p in st.session_state.inventario.values()
    )
    valor_total_stock = sum(
        p["precio"] * p["stock"] for p in st.session_state.inventario.values()
    )
    total_dinero_ventas = sum(v["total"] for v in st.session_state.ventas)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tipos de Productos", tipos_productos)
        st.metric("Unidades en Almacén", unidades_totales)
    with col2:
        st.metric("Valor del Stock", f"S/. {valor_total_stock:.2f}")
        st.metric("Total Vendido", f"S/. {total_dinero_ventas:.2f}")

Usa el código con precaución.st.subheader("Historial de Transacciones")if len(st.session_state.ventas) == 0:st.caption("Aún no se registran ventas en el sistema.")else:st.dataframe(st.session_state.ventas, use_container_width=True)
