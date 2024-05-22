# Alex Ferrandis Ros
from pymongo import MongoClient
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

def conectarBD():
    # Conexión al servidor de MongoDB (localhost por defecto)
    cliente = MongoClient('mongodb://localhost:27017/')
    # Conexión a la base de datos 'ventas'
    db = cliente['vendes']
    return db
# Función para insertar un nuevo artículo en la colección articles
def insertarArticle():
    nom = simpledialog.askstring("Entrada de Datos", "Nom del article: ")
    preu = simpledialog.askstring("Entrada de Datos", "Preu del article: ")
    stock = simpledialog.askstring("Entrada de Datos", "Stock: ")
    try:
        preu = float(preu)
        stock = int(stock)
    except ValueError:
        print("Preu y Stock deben ser numéricos.")
        return
    db = conectarBD()
    articles = db['articles']
    articles.insert_one({'nom': nom, 'preu': preu, 'stock': stock})
def ferVenda():
    try:
        db = conectarBD()
        articles = db['articles']
        vendes = db['vendes']
        # Obtener datos del usuario: nombre del artículo y cantidad vendida
        article_nom = simpledialog.askstring("Entrada de Datos", "Nom del article: ")
        quantitat = simpledialog.askinteger("Entrada de Datos", "Quantitat venuda: ")
        try:
            quantitat = int(quantitat)
        except ValueError:
            print("La cantitat deu de ser numéric.")
            return
        if article_nom is None or quantitat is None:
            print("Venta cancelada.")
            return
        # Verificar y actualizar el stock del artículo en la base de datos
        article = articles.find_one({'nom': article_nom})
        if article is None:
            print(f"No se encontró el artículo '{article_nom}'. Venta cancelada.")
            return
        if article['stock'] < quantitat:
            print(f"No hay suficiente stock para realizar la venta. Stock disponible: {article['stock']}.")
            return
        # Actualizar el stock del artículo
        articles.update_one(
            {'nom': article_nom},
            {'$inc': {'stock': -quantitat}}
        )
        # Insertar la venta en la colección 'vendes'
        vendes.insert_one({'nom': article_nom, 'quantitat': quantitat})
        print("Venta realizada con éxito.")
    except Exception as e:
        print(f"Ha ocurrido un error al realizar la venta: {e}")
def mostrarStock():
    # Conectar a la base de datos MongoDB
    db = conectarBD()
    coleccion = db['articles']
    # Obtener todos los documentos de la colección 'articles'
    articles = coleccion.find({})
    # Crear ventana y configuración
    ventana = tk.Tk()
    ventana.title("Stock de Artículos")
    # Crear un widget de Texto para mostrar los datos
    texto = tk.Text(ventana)
    texto.pack(expand=True, fill=tk.BOTH)  # Expandir para llenar la ventana
    # Agregar los datos al widget de Texto
    for article in articles:
        texto.insert(tk.END, f"Nombre: {article['nom']}\nPrecio: {article['preu']}\nStock: {article['stock']}\n\n")
    # Ejecutar el bucle principal de la ventana
    ventana.mainloop()
def eliminarDato():
    try:
        # Conectar a la base de datos MongoDB
        db = conectarBD()
        coleccion = db['articles']
        # Obtener el nombre del artículo a eliminar
        nombre = simpledialog.askstring("Entrada de Datos", "Ingresa article: ")
        if nombre:
            # Eliminar el artículo de la colección
            resultado = coleccion.delete_one({'nom': nombre})
            if resultado.deleted_count > 0:
                print(f"Article {nombre} eliminat correctament.")
            else:
                print(f"No se encontró el artículo '{nombre}' para eliminar.")
        else:
            print("Eliminación cancelada, no se proporcionó ningún nombre.")
    except Exception as e:
        print(f"Error al eliminar el article: {e}")
def eixir():
    messagebox.showinfo("Eixida del programa", "Gracies per utilitzar la meua aplicació. Torna prompte!")
    ventana.destroy()
def centrarVentana(ancho, alto, ventana):
    anchoPantalla = ventana.winfo_screenwidth()
    altoPantalla = ventana.winfo_screenheight()
    x = (anchoPantalla // 2) - (ancho // 2)
    y = (altoPantalla // 2) - (alto // 2)
    return f"{ancho}x{alto}+{x}+{y}"
# ------------------------- PROGRAMA PRINCIPAL -------------------------
ventana = tk.Tk()
ventana.title("MENU")
ventana.geometry(centrarVentana(400,400,ventana))
# Crear botons
boton1 = tk.Button(ventana, text="ARTICLE NOU", command=insertarArticle)
boton1.pack(pady=5)
boton2 = tk.Button(ventana, text="FER UNA VENDA", command=ferVenda)
boton2.pack(pady=5)
boton3 = tk.Button(ventana, text="MOSTRAR STOCK", command=mostrarStock)
boton3.pack(pady=5)
boton4 = tk.Button(ventana, text="BORRAR ARTICLE", command=eliminarDato)
boton4.pack(pady=5)
boton5 = tk.Button(ventana, text="EIXIR", command=eixir)
boton5.pack(pady=5)
# Executar el bucle principal de la finestra
ventana.mainloop()