#1.- Importamos librerias

import pandas as pd
import networkx as nx
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import numpy as np
import community

#2.- Fijamos una semilla y importamos la base de datos

random_seed = 42

all_holds = pd.read_csv("all_holds.csv")

#3.- Creamos la SN

G = nx.from_pandas_edgelist(all_holds, "Holder", "comp", edge_attr=True)

#obtenemos las posiciones de los nodos
pos = nx.spring_layout(G)

#configuramos el tamaño de los nodos según su grado
node_size = [v * 1.5 for v in dict(G.degree()).values()]

#creamos los ejes
edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

#añadimos los ejes (líneas) al gráfico
edge_trace = go.Scatter(x=edge_x,
                        y=edge_y,
                        line=dict(width=0.5,
                                  color="#888"),
                        hoverinfo="none",
                        mode="lines"
                        )

#creamos los nodos
node_x = []
node_y = []

for x, y in pos.values():
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(x=node_x,
                        y=node_y,
                        mode="markers",
                        hoverinfo="text",
                        marker=dict(showscale=True,
                                    colorscale="Portland",
                                    size=node_size,
                                    colorbar=dict(thickness=15,
                                                  title="Conexiones Nodos",
                                                  xanchor="left",
                                                  titleside="right"
                                                  )
                                    )
                        )

node_trace.marker.color = node_size
node_trace.text = list(G.nodes())

#Creamos la figura

fig_sn = go.Figure(data = [edge_trace, node_trace],
                   layout = go.Layout(showlegend=False,
                                      hovermode="closest",
                                      margin=dict(b=0,l=0,r=0,t=0),
                                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                      )
                   )

#4.- Grados de la red

degrees = G.degree()

degrees_counter = Counter(dict(degrees))

top_nodes = degrees_counter.most_common(10)  #Necesitamos solo los 10 mas grandes

nodes, degrees = zip(*top_nodes)

df = pd.DataFrame({'Nodo': nodes, 'Grado': degrees})

# Graficar con Plotly Express
fig_degree = px.bar(df,
                    x='Nodo',
                    y='Grado',
                    title='Top 10 Nodos por Grado',
                    labels={'Nodo': 'Nodo', 'Grado': 'Grado'},
                    template="plotly_dark",
                    opacity = 0.5
                    )
fig_degree.update_layout(xaxis={'categoryorder': 'total descending'})

#5.- Centralidad de Intermediación
#Intermediación
betweenness_centrality = nx.betweenness_centrality(G)

betweenness_centrality = {
    "Vanguard Group Inc": 0.12254979835525735,
    "MMM": 0.021616956615184348,
    "Blackrock Inc.": 0.12254979835525735,
    "State Street Corporation": 0.12254979835525735,
    "Charles Schwab Investment Management, Inc.": 0.0047019846777215275,
    "Geode Capital Management, LLC": 0.12254979835525735,
    "Morgan Stanley": 0.10976588810461348,
    "State Farm Mutual Automobile Insurance Co": 0.0015167511555118376,
    "Newport Trust Company, LLC": 0.0007304448951865535,
    "Northern Trust Corporation": 0.03088733600885259,
    "Bank of America Corporation": 0.023801025283528194,
    "Berkshire Hathaway, Inc": 0.0006670465510422819,
    "AXP": 0.019176813649532498,
    "Wellington Management Group, LLP": 0.003843992483232504,
    "JP Morgan Chase & Company": 0.01603520405668941,
    "Massachusetts Financial Services Co.": 0.0015539736045169703,
    "AMGN": 0.054795088742052314,
    "Primecap Management Company": 0.00018200768610231397,
    "Capital Research Global Investors": 0.0018170603346271603,
    "Wells Fargo & Company": 0.0,
    "AAPL": 0.01512941638178609,
    "FMR, LLC": 0.014720866203110161,
    "Price (T.Rowe) Associates Inc": 0.006222511592933796
}

top_nodes = sorted(betweenness_centrality.items(),
                   key = lambda x:x[1],
                   reverse=True
                   )[:10]

nodes, centralities = zip(*top_nodes)

df = pd.DataFrame({'Nodo': nodes, 'Centralidad de Intermediación': centralities})

df = df[::-1]

# Graficar con Plotly Express
fig_ci = px.bar(df,
                x='Centralidad de Intermediación',
                y='Nodo',
                orientation='h',
                title='Top 10 Nodos por Centralidad de Intermediación',
                labels={'Nodo': 'Nodo', 'Centralidad de Intermediación': 'Centralidad de Intermediación'},
                template="plotly_dark",
                color='Centralidad de Intermediación',
                color_continuous_scale='Redor',
                opacity = 0.4
                )

#6.- Centralidad de Cercanía

#Cercanía
closeness_centrality = nx.closeness_centrality(G)

#Graficamos la centralidad de cercanía:
closeness_centrality = {
    "Vanguard Group Inc": 0.65,
    "MMM": 0.45,
    "Blackrock Inc.": 0.65,
    "State Street Corporation": 0.65,
    "Charles Schwab Investment Management, Inc.": 0.37,
    "Geode Capital Management, LLC": 0.65,
    "Morgan Stanley": 0.62,
    "State Farm Mutual Automobile Insurance Co": 0.35,
    "Newport Trust Company, LLC": 0.34,
    "Northern Trust Corporation": 0.46,
    "Bank of America Corporation": 0.44,
    "Berkshire Hathaway, Inc": 0.34,
    "AXP": 0.45,
    "Wellington Management Group, LLP": 0.37,
    "JP Morgan Chase & Company": 0.42,
    "Massachusetts Financial Services Co.": 0.34,
    "AMGN": 0.45,
    "Primecap Management Company": 0.32,
    "Capital Research Global Investors": 0.34,
    "Wells Fargo & Company": 0.31,
    "AAPL": 0.45,
    "FMR, LLC": 0.41,
    "Price (T.Rowe) Associates Inc": 0.37
}

top_nodes = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]

nodes, centralities = zip(*top_nodes)

df = pd.DataFrame({"Nodo":nodes, "Centralidad de Cercanía": centralities})
df = df[::-1]

fig_cc = px.bar(df,
                x="Centralidad de Cercanía",
                y="Nodo",
                orientation="h",
                title="Top 10 Nodos por Centralidad de Cercanía",
                labels={"Nodo": "Nodo", "Centralidad de Cercanía": "Centralidad de Cercanía"},
                color="Centralidad de Cercanía",
                template="plotly_dark",
                color_continuous_scale="Teal",
                opacity = 0.6
                )

#7.- Centralidad de Vecindad

# Centralidad de Vecindad
degree_centrality = nx.degree_centrality(G)


top_nodes_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]

nodes_closeness, centralities_closeness = zip(*top_nodes_centrality)

df_centrality = pd.DataFrame({'Nodo': nodes_closeness, 'Centralidad de Vecindad': centralities_closeness})
df_centrality = df_centrality[::-1]

# Graficar con Plotly Express
fig_closeness = px.bar(df_centrality, 
                        y='Nodo', 
                        x='Centralidad de Vecindad', 
                        orientation='h',
                        title='Top 10 Nodos por Centralidad de Vecindad',
                        labels={'Nodo': 'Nodo', 'Centralidad de Vecindad': 'Centralidad de Vecindad'},
                        template="plotly_dark",
                        color='Centralidad de Vecindad',  # Utilizar la variable de centralidad como color
                        color_continuous_scale='Mint',
                        opacity=0.7
                        )

# Diametro de la red
diameter = nx.diameter(G)

# Radio de la red
radius = nx.radius(G)

# Coeficiente de asortatividad:
asort = nx.degree_assortativity_coefficient(G)

# Bridges, Hubs y outliers

bridges = list(nx.bridges(G))
hubs = [node for node, degree in G.degree() if degree > 2 * (len(G) - 1) / len(G)] #medida que indica nodos más grandes que la media
outliers = [node for node, degree in G.degree() if degree == 1] #fijamos nodos minimos como aquellos con 1 grado

max_length = max(len(bridges), len(hubs), len(outliers)) #fijamos una sola longitud (la mas grande)

bridges += [None] * (max_length - len(bridges))
hubs += [None] * (max_length - len(hubs))
outliers += [None] * (max_length - len(outliers))

#consolidamos el dataframe

df_roles = pd.DataFrame({
    'Bridges':bridges,
    'Hubs':hubs,
    'Outliers':outliers
})

# Analisis de comunidades

# Obtén las comunidades utilizando el algoritmo de Louvain
partition = community.best_partition(G, random_state=np.random.RandomState(random_seed)) #usamos la semilla para evitar diferentes comunidades

# Asignar colores a nodos según la comunidad a la que pertenecen
node_colors = [partition[node] for node in G.nodes()]


# Crear un nuevo gráfico con colores de comunidad
fig_community = go.Figure(data=[
        edge_trace,
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            hoverinfo="text",
            marker=dict(
                color=node_colors,
                showscale=True,
                colorscale="Viridis",
                size=node_size,
                colorbar=dict(
                    thickness=15,
                    title="Comunidad",
                    xanchor="left",
                    titleside="right"
                )
            ),
            text=list(G.nodes())  # Asegúrate de incluir el texto para el hover
        )
    ],
    layout=go.Layout(
        showlegend=False,
        hovermode="closest",
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
)


#Layout

logo_image = "logo.png"
st.sidebar.image(logo_image, width=280)
st.sidebar.write("Las opciones seleccionadas aparecerán en la parte inferior de la red principal.")
st.sidebar.title("Seleccione indicadores:")

indicadores = ["Diámetro de la Red", "Radio de la Red", "Coeficiente de Asortatividad" ,"Grados de la Red", "Centralidad de Intermediación", "Centralidad de Cercanía",
               "Centralidad de Vecindad"]

indicadores_selec = st.sidebar.multiselect("Indicadores:",indicadores)

st.sidebar.title("Análisis de Roles en la Red")
roles = ["Bridges", "Hubs", "Outliers"]

roles_selec = st.sidebar.multiselect("Seleccione el Rol:", roles)

st.sidebar.title("Detección de Comunidades")

detec_graf = ["Comunidades detectadas en la red"]
detec = st.sidebar.multiselect("Ver red con detección de comunidades:", detec_graf)

selected_communities = st.sidebar.selectbox("Selecciona la comunidad:", sorted(set(partition.values())))
# Aseguramos que sea una lista
if not isinstance(selected_communities, list):
    selected_communities = [selected_communities]

# Filtrar nodos por comunidades seleccionadas
selected_nodes = [node for node, comm_id in partition.items() if comm_id in selected_communities]

st.title("¿Quién es el dueño del Dow Jones?")
st.write("El Dow Jones uno de los índices bursátiles más reconocidos y seguidos en el mundo financiero. Fue creado por Charles Dow en 1896 y originalmente incluía solo 12 compañías. Hoy en día, el Dow Jones Industrial Average consta de 30 grandes empresas estadounidenses líderes en diversos sectores, lo que lo convierte en un indicador representativo de la salud general del mercado de valores de Estados Unidos.")
st.header("Red Social del Dow Jones")
st.write("Los tenedores institucionales, que son inversionistas significativos en las 30 empresas del índice, ejercen influencia en decisiones de inversión y estrategias del mercado. Sus transacciones a gran escala pueden impactar los precios de acciones. En el contexto del Dow Jones, una red social representa relaciones de inversión y propiedad de activos, permitiendo identificar nodos clave (grandes propietarios), detectar comunidades y evaluar la importancia de nodos específicos en la red, facilitando el análisis de estructuras financieras complejas.")
st.write("Debo aclarar que en la parte inferior se visualiza un gráfico interactivo de la red. Usted puede hacer zoom en las zonas de interés utilizando las opciones de selección en la parte superior derecha del gráfico.")
st.plotly_chart(fig_sn)
st.write("En la red, nodos centrales como Vanguard, BlackRock y State Street ejercen una influencia dominante, afectando las tendencias del mercado. Un grupo intermedio, con empresas como Bank of America y JP Morgan, actúa como intermediario en la transmisión de información. Otro grupo, con impacto moderado, incluye a empresas como Apple y American Express, mientras que un cuarto grupo tiene un impacto marginal, posiblemente especializándose en sectores específicos. Estas posiciones reflejan la complejidad y diversidad de roles en la red financiera.")
st.divider()

if "Centralidad de Vecindad" in indicadores_selec:
    st.subheader("Centralidad de Vecindad")
    st.write("La **Centralidad de Vecindad** se entiende como la relevancia de actores financieros que ocupan **posiciones estratégicas dentro de grupos o comunidades específicas** en una red. Estos nodos pueden tener una influencia significativa en la toma de decisiones y la transmisión de información dentro de su entorno cercano, aunque no necesariamente sean los actores más grandes de la red en su totalidad.")
    st.plotly_chart(fig_closeness)
    st.divider()

if "Centralidad de Cercanía" in indicadores_selec:
    st.subheader("Centralidad de Cercanía")
    st.write("La **Centralidad de Cercanía** indica la **importancia de nodos financieros que están en una posición cercana a otros nodos en la red**. Estos actores tienden a tener conexiones directas con una variedad de participantes en el mercado, lo que les **otorga acceso a información diversa** y les permite influir en la transmisión efectiva de datos en la red.")
    st.plotly_chart(fig_cc)
    st.divider()

if "Centralidad de Intermediación" in indicadores_selec:
    st.subheader("Centralidad de Intermediación")
    st.write("La **Centralidad de Intermediación** refiere a la posición estratégica de actores financieros que actúan como **intermediarios clave** entre nodos más grandes y más pequeños en una red financiera. Estos actores facilitan la transmisión eficiente de información y desempeñan un papel fundamental en la conectividad del mercado.")
    st.plotly_chart(fig_ci)
    st.divider()

if "Grados de la Red" in indicadores_selec:
    st.subheader("Top Grados de la Red")
    st.write("En el siguiente gráfico se podrá ver las 10 entidades con más conexiones en la red. Dicha conexión brinda un impacto significativo en las demás entidades y en el mercado en general.")
    st.plotly_chart(fig_degree)
    st.divider()

if "Coeficiente de Asortatividad" in indicadores_selec:
    st.subheader("Coeficiente de Asortatividad")
    st.write("Mide la tendencia de los nodos de la red a conectarse con otros nodos que tienen un grado similar. El valor de asortatividad **oscila entre -1 a 1**.")
    st.write("Si el coeficiente es **positivo**, indica que existe una tendencia de **asortatividad** de los nodos a conectarse entre aquellos que tienen un grado similar. Es decir, los nodos con muchos enlaces tienden a enlazarse con otros nodos de muchos enlaces. Del mismo modo, nodos con pocos enlaces tienden a conectarse con nodos de pocos enlaces.")
    st.write("Si el coeficiente es **negativo**, indica una tendencia hacia la **disasortatividad**. En tal caso, los nodos con muchos enlaces tienden a conectarse con nodos con pocos enlaces y viceversa.")
    st.metric(label="Coeficiente de Asortatividad:",
              value=asort,
              delta="Grado de Asortatividad en la Red")
    st.write("En este caso, como el coeficiente de asortatividad es `-0.27`, sugiere una ligera tendencia hacia la **disasortatividad**. Esto significa que en la red, los nodos con muchos enlaces tienden a conectarse con nodos que tienen pocos enlaces y viceversa, pero la tendencia no es muy fuerte.")
    st.divider()

if "Radio de la Red" in indicadores_selec:
    st.subheader("Radio de la Red")
    st.write("El **radio de la red** es una medida que representa la distancia promedio entre un nodo central y todos los demás nodos en la red. Indica la **proximidad promedio** de cada institución financiera en el **Dow Jones** respecto a una entidad central. Un **radio bajo** sugiere una **mayor cohesión** en la red, ya que las distancias entre los actores clave y el nodo central son relativamente cortas.")
    st.metric(label="Radio de la Red:",
              value=radius,
              delta="Distancia promedio entre dos nodos más cercanos"
              )
    st.write("El **radio de la red es de 2**, indicando la distancia mínima entre cualquier nodo y su nodo más cercano en la red. En términos financieros, esto sugiere que **la información y la influencia pueden propagarse rápidamente en un entorno altamente interconectado**. ")
    st.divider()

if "Diámetro de la Red" in indicadores_selec:
    st.subheader("Diámetro de la red")
    st.write("Describe **la distancia más larga** entre dos nodos dentro de una red. Representa la longitud máxima del camino más corto entre cualquier par de instituciones financieras en el **Dow Jones Industrial Average (DJIA)**. Si el diámetro es bajo, la red está más estrechamente conectada, ya que la distancia máxima entre actores clave es relativamente corta.")
    st.metric(label="Diámetro de la Red:",
              value=diameter,
              delta="Distancia máxima entre cualquier par de entidades"
              )
    st.write("**El valor del diámetro de la red es 4**, es decir, la distancia máxima entre cualquier par de instituciones financieras del **Dow Jones** es de **4 conexiones**. En síntesis, sugiere una mayor eficiencia en la transmisión de **eventos del mercado**, **decisiones financieras** y **cambios en las condiciones económicas**.")
    st.divider()

if "Outliers" in roles_selec:
    st.subheader("Nodos Outliers")
    st.write("Nodos con conexiones mínimas (Outliers):")
    st.write(df_roles["Outliers"])

if "Hubs" in roles_selec:
    st.subheader("Nodos Centrales (Hubs)")
    st.write("Nodos que actúan como líderes de comunidad:")
    st.write(df_roles["Hubs"])
    st.divider()

if "Bridges" in roles_selec:
    st.subheader("Nodos Puente (Bridges)")
    st.write("Nodos que actúan como puentes entre partes diferentes de la red:")
    st.write(df_roles["Bridges"])
    st.divider()

if "Comunidades detectadas en la red" in detec:
    st.subheader("Comunidades detectadas en la Red")
    st.write("La detección de comunidades consiste en identificar grupos de nodos en una red que están más estrechamente conectados entre sí que con el resto de la red. Estos grupos de nodos forman comunidades o subgrupos dentro de la red más amplia. El objetivo principal de este análisis es revelar la estructura interna y la organización de la red, destacando las relaciones más fuertes y significativas entre sus miembros.")
    st.write("En el caso del Dow Jones se detectaron 5 comunidades cada una con un color distinto a modo de diferenciarlas. Usted puede visualizar en el gráfico las comunidades o a través del sidebar donde se visualizarán en formato de tablas.")
    st.plotly_chart(fig_community)

# Mostrar tabla con nodos ordenados por tamaño
    if selected_nodes:
        node_sizes = {node: G.degree[node] for node in selected_nodes}
        sorted_nodes = sorted(node_sizes.items(), key=lambda x: x[1], reverse=True)
        
        st.subheader(f"Comunidad {selected_communities}")
        st.table(sorted_nodes)
    else:
        st.sidebar.info("Selecciona al menos una comunidad en el multiselect.")

if st.sidebar.button("Descarga la Base de Datos"):
    all_holds.to_csv("all_holds.csv", index=False)
    st.sidebar.success("¡Base de Datos descarga!")















