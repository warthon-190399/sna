import pandas as pd
import networkx as nx
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

all_holds = pd.read_csv("all_holds.csv")

# 3.- Creamos la SN

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

top_nodes = degrees_counter.most_common(10)  # cambiamos a 10 el número deseado de nodos principales

print("Nodos más grandes segun numero de grados:")
for node, degree in top_nodes:
    print(f"Nodo: {node}, Grado: {degree}")

nodes, degrees = zip(*top_nodes)

df = pd.DataFrame({'Nodo': nodes, 'Grado': degrees})



# Graficar con Plotly Express
fig_degree = px.bar(df, x='Nodo', y='Grado', title='Top 10 Nodos por Grado', labels={'Nodo': 'Nodo', 'Grado': 'Grado'},
             template="plotly_dark", opacity = 0.6)
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
fig_ci = px.bar(df, x='Centralidad de Intermediación', y='Nodo', orientation='h',
             title='Top 10 Nodos por Centralidad de Intermediación',
             labels={'Nodo': 'Nodo', 'Centralidad de Intermediación': 'Centralidad de Intermediación'},
             template="plotly_dark",
             color='Centralidad de Intermediación', color_continuous_scale='Redor', opacity = 0.6)

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


#Layout

logo_image = "logo.png"
st.sidebar.image(logo_image, width=280)
st.sidebar.title("Seleccione indicadores:")

indicadores = ["Grados de la Red", "Centralidad de Intermediación", "Centralidad de Cercanía",
               "Centralidad de Vecindad", "Diámetro de la Red", "Radio de la Red", "Coeficiente de Asortatividad"]

indicadores_selec = st.sidebar.multiselect("Indicadores:",indicadores)

st.title("¿Quién es el dueño del Dow Jones? Holi xd")
st.header("Red Social del Dow Jones")
st.write("Un red social es un estructura que sirve para representar entidades **(nodos)** y relaciones **(ejes, aristas)**."
         " En el contexto financiero sirve para entender y visualizar relaciones de inversión y la propiedad de activos de las empresas."
         " Dentro del análisis de redes podemos identificar nodos clave (grandes propietarios), detección de comunidades y la importancia de nodos específcos en la red.")
st.plotly_chart(fig_sn)
st.write("En la red podemos observar los nodos centrales que constituyen una **posición dominante** como **Vanguard**, **Blackrock Inc** o **State Street**."
         " Esto indica la existencia de relaciones muy sólidas con otros tenedores institucionales. Sus decisiones influyen en las tendencias del mercado y afectan carteras de inversión de otros tenedores."
         )
st.write("El segundo grupo que ocupa una **posición intermedía** en la red comprende empresas como **Bank of America**, **Northern Trust**, **FMR** y **JP Morgan**."
         " Al estar conectados con nodos más grandes y más pequeños, este grupo puede desempeñar un papel crucial en la **transmisión de información** dentro de la red."
         " Probablemente actuen como **intermediarios** que facilitan la conexión entre diferentes partes del mercado financiero." 
         )
st.divider()

if "Grados de la Red" in indicadores_selec:
    st.plotly_chart(fig_degree)
    st.divider()

if "Centralidad de Intermediación" in indicadores_selec:
    st.plotly_chart(fig_ci)
    st.divider()
if "Centralidad de Cercanía" in indicadores_selec:
    st.plotly_chart(fig_cc)
    st.divider()

if "Centralidad de Vecindad" in indicadores_selec:
    st.plotly_chart(fig_closeness)
    st.divider()
















