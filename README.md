Quién es dueño del Dow Jones
Este proyecto utiliza técnicas de análisis de redes para explorar la estructura y dinámica de la red financiera del Dow Jones Industrial Average (DJIA). La red se construye a partir de las relaciones de propiedad e inversión entre las principales instituciones financieras que componen el índice DJIA.

Contenido del Proyecto
1. Creación de la Red
La red se genera a partir de la base de datos "all_holds.csv", que contiene información sobre las conexiones entre los tenedores institucionales y las compañías en el Dow Jones.

2. Visualización de la Red
Se utiliza la biblioteca NetworkX junto con Plotly para visualizar la red de manera interactiva. Los nodos representan instituciones financieras, y las conexiones entre ellos indican relaciones de propiedad e inversión.

3. Análisis de Indicadores Financieros
Se calculan varios indicadores financieros, incluyendo grados de la red, centralidades de intermediación, cercanía y vecindad. Estos indicadores proporcionan insights sobre la importancia y el papel de cada institución en la red financiera.

4. Detección de Comunidades
Se utiliza el algoritmo de Louvain para detectar comunidades dentro de la red. Cada comunidad se visualiza con un color distinto, revelando agrupaciones significativas de instituciones financieras.

5. Análisis de Roles en la Red
Se identifican y visualizan nodos destacados, como Hubs, Bridges y Outliers, que desempeñan roles clave en la transmisión de información y conectividad de la red.

Resultados Destacados
Visualización Interactiva de la Red: Explora la red financiera del Dow Jones de manera interactiva con la capacidad de hacer zoom y resaltar nodos específicos.

Análisis de Indicadores Financieros: Comprende la importancia relativa de las instituciones financieras mediante el análisis de grados, centralidades y otros indicadores clave.

Detección de Comunidades: Descubre agrupaciones naturales de instituciones financieras y analiza sus interacciones internas.

Roles en la Red: Identifica nodos clave que actúan como Hubs, Bridges y Outliers, proporcionando información sobre la estructura y dinámica de la red.

Instrucciones de Uso
Requisitos: Asegúrate de tener instaladas todas las bibliotecas necesarias especificadas en el archivo requirements.txt.

Ejecución Local: Ejecuta el script script_database.py para generar y visualizar la red en tu entorno local.

Exploración Interactiva: Utiliza Streamlit para explorar la red y analizar diferentes aspectos utilizando los controles en la barra lateral.

Descarga de Datos: Si deseas descargar la base de datos generada, utiliza el botón correspondiente en la barra lateral
