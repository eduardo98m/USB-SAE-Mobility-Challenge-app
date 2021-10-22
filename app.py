import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

import pandas as pd


from get_dataframes import get_crash_data_df, get_gridwise_data_df, get_intersections_clust_data_df, get_bikes_clust_data_df

@st.cache()
def get_graph(df,
              group,
              title = "plot_title",  
              x_label = "x_label",
              y_label = "y_label",
              z_label = "z_label", 
              color = None,  
              only_bikes=False, 
              ticks=0, 
              plt_f=px.bar,
              horizontal=False 
              ):
    
    if only_bikes: df = df[df['BICYCLE'] == 1]

    labels = {
        group:x_label,
        "count":y_label,
        color:z_label,
    }

    if not color:
        df_groups = df.groupby(group)
        X = []
        Y = []
        
        for s, d in df_groups:

            X.append(s)
            Y.append(int(len(d)))
        
        data_to_plot = pd.DataFrame(
                                    {group: X,
                                    'count': Y,
                                    })

        
        if horizontal:
            fig = plt_f(data_to_plot, x="count", y=group, #color='#00059E',
                title= title,
                labels = labels,
                orientation="h")
        
        else:
            fig = plt_f(data_to_plot, x=group, y="count", #color='#00059E',
                title= title,
                labels = labels)
    
    else:
        df_groups = df.groupby(group)
        X = []
        Y = []
        Z = []
        
        for x_category, data in df_groups:

            df_groups_b = data.groupby(color)

            for z_category, d in df_groups_b:
            
                X.append(x_category)
                Y.append(int(len(d)))
                Z.append(z_category)
        

        data_to_plot = pd.DataFrame(
                                    {group: X,
                                    'count': Y,
                                    color:Z}
                                    )
        
        if horizontal:
            fig = plt_f(data_to_plot, x="count", y=group, color=color,
                title= title,
                labels = labels,
                orientation="h")
        
        else:
            fig = plt_f(data_to_plot, x=group, y="count", color=color,
                title= title,
                labels = labels)



    return fig


st.set_page_config(
     page_title='USB-SAE Mobility Team',
     page_icon="🚲",
     layout="centered", # Puede cambiarse a "wide"
     initial_sidebar_state="collapsed",
     menu_items={
         'Report a bug': "https://github.com/eduardo98m",
         'About': "https://www.sae.org",

     }
 )

px.set_mapbox_access_token(st.secrets["map_box_key"])

# Reading the datasets files

df = get_crash_data_df()

df_gw = get_gridwise_data_df()

df_clust_intersections =  get_intersections_clust_data_df()

df_clust_bikes = get_bikes_clust_data_df()

#
year_list = list(df['CRASH_YEAR'].unique())
# 

# App layout #
st.title('USB-SAE Mobility Team')

st.image("https://media.istockphoto.com/photos/panoramic-view-of-pittsburgh-and-the-3-rivers-picture-id1093811582?k=20&m=1093811582&s=612x612&w=0&h=-KpOZ2OHlG7g2-A5fAGTCB0GtNCNVhmgZCqbr8hbzNE=")
st.text("[Párrafo introductorio]")



with st.expander("🚗🛵🥡 Initial data analisys and insights"):
    # @amin
    # La idea de esta parte es colcoar todas las gráficas de los insgishts que no tengan 
    # que ver mucho con las bicicletas o las intersecciones

    #Ejm: La de los accidentes por año, mes y día de la semana
    # Agrupados por límites de velocidad
    # Ageupados por nivel de luz 
    # Agrupados porroad condition

    
    # Accidents vs Speed Limit
    graph = get_graph(
        df, 
        'SPEED_LIMIT', 
        x_label = 'Speed Limit (milles per hour)', 
        y_label = 'Accident count', 
        title = 'Total accidents per speed limit',
    )
    st.plotly_chart(graph, use_container_width=True)

    # Accidents vs Year
    graph = get_graph(
        df, 
        'CRASH_YEAR', 
        x_label = 'Year', 
        y_label = 'Accidents', 
        title ='Total accidents per year',
        #color = "CRASH_MONTH",
        #z_label = "month",
        only_bikes=False,
    )
    st.plotly_chart(graph, use_container_width=True)

    # Accidents vs Month
    graph = get_graph(
        df, 
        'CRASH_MONTH', 
        x_label ='Month', 
        y_label ='Accidents', 
        title ='Total accidents per month',
        only_bikes=False,
    )
    st.plotly_chart(graph, use_container_width=True)

    # Accidents vs Day of Week
    graph = get_graph(
        df, 
        'DAY_OF_WEEK', 
        x_label ='Day', 
        y_label ='Accidents', 
        title = 'Total accidents per day of week',
        only_bikes=False,
    )
    st.plotly_chart(graph, use_container_width=True)



    # Accidents vs Light Condition
    graph = get_graph(
        df, 
        'ILLUMINATION', 
        x_label ='Illumination condition', 
        y_label ='Accidents', 
        title = 'Total accidents by road illumination',
        only_bikes=False,
    )
    st.plotly_chart(graph, use_container_width=True)

    # Accidents vs Road Condition
    graph = get_graph(
        df, 
        'ROAD_CONDITION', 
        x_label ='Road Condition', 
        y_label ='Accidents', 
        title = 'Total accidents per road condition',
        only_bikes=False,
    )
    st.plotly_chart(graph, use_container_width=True)

    st.write("""
    [Párrafo Explicando la data]
    """)


with st.expander("🚗🛵🥡 Delivery data insights"):
   
    #st.plotly_chart(px.pie(df, values='tip', names='day'), use_container_width=True)
    st.write("""
    [Párrafo Explicando la data]
    """)

    




with st.expander("🚦 The intersection problem"):
    # Aqui faltarian mapas de accidentes cerca de intersecciones
        
    #@Amin ponme esta gráfica bonita (Si se pudiesen colocar los porcentajes estaría peppa)
    plot_data = pd.DataFrame(df['INTERSECTION'].value_counts())
    st.plotly_chart(px.bar(plot_data), use_container_width=True)
    st.write("""
    [Párrafo Explicando la data]
    """)

    st.subheader("Intersection Crashes clusterized")

    st.plotly_chart(px.scatter_mapbox(df_clust_intersections, 
                            lat="DEC_LAT", 
                            lon="DEC_LONG",  
                            color='CLUSTER_COUNT', #size='CRASH_YEAR', text = 'CLUSTER_COUNT',
                            size_max=3, zoom=10))


    st.header("🚲💥 Bike crashes")
    st.write("""
    The map below show the number of bike accidents by year, there it is possible to 
    observe that a majority of the crashes occur near intersections.
    """)
    bk_crahs_options = year_list + ["2004-2020"]
    bike_crash_year = st.selectbox("Year",
                                    bk_crahs_options,
                                    len(bk_crahs_options)-1
                                    )  
    
    if bike_crash_year != "2004-2020":
        df_crash_bikes = df.loc[df['BICYCLE']==True].loc[df['CRASH_YEAR']==bike_crash_year]    
    else:
        df_crash_bikes = df.loc[df['BICYCLE']==True]

    st.plotly_chart(px.scatter_mapbox(
                    df_crash_bikes, 
                    lat="DEC_LAT", 
                    lon="DEC_LONG", 
                    color="BICYCLE_DEATH_COUNT", 
                    size='BICYCLE_COUNT',
                    size_max=15, zoom=10))

    #@Amin ponme esta gráfica bonita  (Si se pudiesen colocar los porcentajes estaría peppa)
    plot_data = pd.DataFrame(df['INTERSECTION'].loc[df['BICYCLE']==True].value_counts())
    st.plotly_chart(px.bar(plot_data), use_container_width=True)
    st.write("""
    [Párrafo Explicando la data]
    """)            
    st.subheader("Bike Crashes clusterized")
    st.plotly_chart(px.scatter_mapbox(df_clust_bikes, 
                    lat="DEC_LAT", lon="DEC_LONG",  
                    color='Accidents per cluster',
                    title = "Clusterized Data Bycicle accidents",
                    opacity=0.55, 
                    #color_continuous_scale= px.colors.sequential.turbo,
                    size='CRASH_YEAR',# text = 'CLUSTER_COUNT',
                    size_max=8, zoom=10))
    
    st.write("""
    A proven meassure to reduce these kind of accidents are protected intersections,
    These are a special type of intersection where the cyclist and pedestrians are 
    separated from cars by a buffer zone, and drivers gain wider visibility and thus 
    increase their reaction time.
    """)
    st.image("https://cyclingtips.com/wp-content/uploads/2020/12/albert_landsdowne.jpg",
    caption="Proposed protected intersection in Melbourne Australia")
    

with st.expander("📈 Economics"):
    
    plot_data = pd.DataFrame(df['CRASH_YEAR'].value_counts())
    #@Amin aquí deberían estar las gráficas de los temas economicos que creo que mandó yisus
    #st.plotly_chart(px.pie(plot_data), use_container_width=True)
    st.write("""
    [Párrafo Explicando la data]
    """)






with st.expander("📊 Datasets"):

    st.write("""
    The data used for this study is the Allegheny County Crash Data, it is a dataset 
    containing information about the different car crashes and accidents that occurred 
    in the County between the years 2004 and 2020.  
    The data set is well structured and contains lots of details abouteach accident. 
    A data set provided by Gridwise was also employed to find some complementary insights 
    for our proposal.
    """)
