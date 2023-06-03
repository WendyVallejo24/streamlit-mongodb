from pymongo import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from pymongo import MongoClient
from collections import Counter
import pandas as pd

sidebar = st.sidebar
sidebar.image('perfil.jpeg')
sidebar.title("Wendy Belén Vallejo Patraca")
sidebar.write("Matricula: S20006733")
sidebar.write("zS20006733@estudiantes.uv.mx")
sidebar.markdown("___")

uri = "mongodb+srv://wendy24:wendy_ptr2402@artists.klushnh.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client.artists
    print("MongoDB Connected successfully!")
except:
    print("Could not connect to MongoDB")

st.title("Artists MongoDB Dashboard")
@st.experimental_memo(ttl=600)
def get_dataReactions():
    items = db.artists_reactions.find()
    items = list(items)
    return items

def commentsDataframe():
    db = client['artists']
    collection = db['artists_comments']
    documentos = collection.find()
    datos = []
    for documento in documentos:
        datos.append(documento)
    df = pd.DataFrame(datos)
    return df

def reactionsDataframe():
    db = client['artists']
    collection = db['artists_reactions']
    documentos = collection.find()
    datos = []
    for documento in documentos:
        datos.append(documento)
    df = pd.DataFrame(datos)
    return df
datos_reactions= reactionsDataframe()

def grafico_pastel_reactions(datos_reactions):
    fig = px.pie(datos_reactions, names='reactionId')
    st.plotly_chart(fig)

datos_df = commentsDataframe()
def grafico_barras_usuarios(datos_df):
    fig = px.bar(datos_df.groupby('userId').count().reset_index(), x='userId', y='comment')
    st.plotly_chart(fig)

def grafico_pastel_objetos(datos_df):
    fig = px.pie(datos_df, names='objectId')
    st.plotly_chart(fig)

def grafico_caja_usuarios(datos_df):
    fig = px.box(datos_df, x='userId', y='comment')
    st.plotly_chart(fig)

@st.experimental_memo(ttl=600)
def get_dataComents():
    itemsC = db.artists_comments.find()
    itemsC = list(itemsC)
    return itemsC

itemsC = get_dataComents()

def mostrarComents():
    listasdb = db.artists_comments.distinct("comentId")
    listasdb = list(listasdb)
    return listasdb

def mostrar():
    listasdb = db.artists_reactions.distinct("reactionId")
    listasdb = list(listasdb)
    return listasdb

print(mostrar())


items = get_dataReactions()

sidebar.header("Vistas de datos")
sidebar.header("Selecciona una opción")

agree = sidebar.checkbox("Comentarios en tabla")
if agree:
    st.header("info de comentarios...")
    st.dataframe(itemsC)
    st.markdown("_")

agree = sidebar.checkbox("Reacciones en tabla")
if agree:
    st.header("info de reacciones...")
    st.dataframe(items)
    st.markdown("_")

agree = sidebar.checkbox("Raw de comentarios")
if agree:
    st.header("info de comentarios...")
    st.write(itemsC)
    st.markdown("_")
#
    
agree = sidebar.checkbox("Raw de reacciones")
if agree:
    st.header("info de reacciones...")
    st.write(items)
    st.markdown("_")

if st.sidebar.checkbox('Comentarios'):
    collection = db['artists_comments']
    collection2 = db['artists_reactions']
    registros = collection.find()

    # Crear una lista con los campos "comment" y "objectId"
    data = [["Comentario", "Publicacion", "Usuario"]]
    for registro in registros:
        comment = registro['comment']
        objectId = registro['objectId']
        userId = registro['userId']
        data.append([comment, objectId, userId])

    # Mostrar la tabla en Streamlit
    st.table(data)

sidebar.markdown("___")
sidebar.header("Gráficas")
sidebar.header("Selecciona una opción")

if st.sidebar.checkbox('Grafica de pastel reactions'):
    st.header("Gráfico de pastel para mostrar la proporción de reacciones por tipo:")
    grafico_pastel_reactions(datos_reactions)

if st.sidebar.checkbox('Grafica de barras reactions'):

    collection = db['artists_reactions']
    registros = collection.find()

    # Obtener los "reactionId" y contar la cantidad de cada uno
    reaction_ids = [registro['reactionId'] for registro in registros]
    contador_reaction_ids = Counter(reaction_ids)

    # Obtener los datos para la gráfica
    reaction_ids_list = list(contador_reaction_ids.keys())
    cantidad_list = list(contador_reaction_ids.values())

    # Crear la gráfica de barras con Plotly
    fig = go.Figure(data=[go.Bar(x=reaction_ids_list, y=cantidad_list)])

    # Configurar el diseño de la gráfica
    fig.update_layout(
        title="Cantidad de reacciones por tipo",
        xaxis_title="Reaction ID",
        yaxis_title="Cantidad"
    )
    # Mostrar la gráfica en Streamlit
    st.plotly_chart(fig)

if st.sidebar.checkbox('Grafica de pastel comments'):
    st.header("Gráfico de pastel para mostrar la proporción de comentarios por objeto:")
    grafico_pastel_objetos(datos_df)

if st.sidebar.checkbox('Grafica de barras usuarios'):
    st.header("Gráfico de barras para contar el número de comentarios por usuario:")
    grafico_barras_usuarios(datos_df)


def grafico_barras_agrupadas(datos_df):
    fig = px.bar(datos_df, x='userId', y='comment', color='objectId', barmode='group')
    st.plotly_chart(fig)

if st.sidebar.checkbox('Grafica de barras agrupadas'):
    st.header("Gráfico de barras agrupadas para mostrar el número de comentarios por usuario y por objeto:")
    grafico_barras_agrupadas(datos_df)
