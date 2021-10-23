import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

import pandas as pd


from get_dataframes import get_crash_data_df, get_gridwise_data_df, get_intersections_clust_data_df, get_bikes_clust_data_df

import plotly.graph_objects as go


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
              horizontal=False,
              update_layout_kwargs = {},
              **kwargs,
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
                orientation="h",**kwargs)
        
        else:
            fig = plt_f(data_to_plot, x=group, y="count", #color='#00059E',
                title= title,
                labels = labels,**kwargs)        
    
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
                orientation="h",**kwargs)
        
        else:
            fig = plt_f(data_to_plot, x=group, y="count", color=color,
                title= title,
                labels = labels,**kwargs)

    
    fig.update_layout(**update_layout_kwargs)

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

st.markdown("""
<div style="text-align: justify">

Welcome to the USB-SAE Mobility Team interactive both for the SAE-AI mini challenge.

The objective of our entry was to develop a series of recomendations that would improve mobility accessibility, 
solving crucial social issues in Allegheny County, Pennsylvania, based mainly on data analisys.

With that objective in mind,  and trough the use of data mining tools and extensive research
we found that a good solution to imporve the mobility of the county citizens is to incetivice 
cycling among the county residents,
through the building of cycling infrastructure.

While looking trough the data, We also found other useful insights that might be worth mentioning.


In this application we show the tough process that went into developing our solution and the 
diferent insight that we found in the data.
</div>

""",unsafe_allow_html=True)



with st.expander("🚗🛵🥡 Initial data analisys and insights"):
    # @amin
    # La idea de esta parte es colcoar todas las gráficas de los insgishts que no tengan 
    # que ver mucho con las bicicletas o las intersecciones

    #Ejm: La de los accidentes por año, mes y día de la semana
    # Agrupados por límites de velocidad
    # Ageupados por nivel de luz 
    # Agrupados porroad condition

    st.markdown("""
    <div style="text-align: justify">

    We begin by analyzing the data looking for temporal patterns that show an increase or 
    decrease of accidents at certain times. Therefore, we grouped the data by year, month 
    and day of the week. For the first case, a sharp decrease in accidents can be observed 
    between the years 2019 and 2020, which can be easily attributed to the CoVID-19 
    pandemic and the subsequent lockdown measures taken by the state government. 
    These measures drastically reduced the mobility of citizens and subsequently the 
    likelihood of accidents on the road. Fewer cars on the roads, fewer accidents are 
    likely to occur.

    </div>

    """,unsafe_allow_html=True)
    
  
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
        plt_f=px.line,
        markers=True,
    )
    st.plotly_chart(graph, use_container_width=True)

    st.markdown("""
    <div style="text-align: justify">

    Regarding the months, the ones that accumulate more accidents are January and December, 
    probably due to two main factors: road conditions at that time is rainy and snowy, 
    negatively affecting mobility; while Christmas and vacation events promote the 
    mobilization of many people, increasing the likelihood of vehicle crashes. 

    </div>

    """,unsafe_allow_html=True)

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

    st.markdown("""
    <div style="text-align: justify">

   The weekdays with the highest proportion of accidents are Thursdays, 
   Fridays and Saturdays, as more people tend to go out to parties and gatherings, 
   this is in constrast to Sundays and Mondays where people tend to stay at home and only 
   go out to work.

    </div>

    """,unsafe_allow_html=True)

    # Accidents vs Day of Week
    graph = get_graph(
        df, 
        'DAY_OF_WEEK', 
        x_label ='Day', 
        y_label ='Accidents', 
        title = 'Total accidents per day of week',
        only_bikes=False,
        update_layout_kwargs={'xaxis':{'categoryorder':'array', 
        'categoryarray':['Monday','Thursday','Wednesday','Tuesday',
                        'Friday', 'Saturday', 'Sunday']}},
    )
    st.plotly_chart(graph, use_container_width=True)

    st.markdown("""
    <div style="text-align: justify">

   Then, we decided to study how much weather conditions affect the proportion of disasters, 
   and indeed if the road is wet the proportion is high, corroborating its increase at the
   end of the year due to winter. The reason why the dry road has the highest number of 
   accidents is because it is the common condition of the road, not because 
   being dry promotes the occurrence of disasters.

    </div>

    """,unsafe_allow_html=True)

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

    st.markdown("""
    <div style="text-align: justify">

    Another important factor that we took into consideration are the illumination 
    conditions, which is also related to the weather since in winter the nights last 
    longer. It can be noted that a significant proportion of accidents occur in areas 
    without streetlighs, thus installing streetlights in those areas could be a 
    significant step to solving this problem.
    </div>

    """,unsafe_allow_html=True)

    

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

    st.markdown("""
    <div style="text-align: justify">

    Lastly, we noticed that the number of accidents that occurred on roads with 25 mph 
    speed limits is very high. This is a relevant insight, as it can be explained by two 
    factors: that most roads have a 25 mph speed limit, but also that such a limit may not 
    be appropriate for some of the roads where it is imposed, i.e., reducing the speed 
    limit to 20 mph by introducing some traffic calming measures may result in a reduction 
    of accidents on those roads.
    </div>

    """,unsafe_allow_html=True)

    # Accidents vs Speed Limit
    graph = get_graph(
        df, 
        'SPEED_LIMIT', 
        x_label = 'Speed Limit (milles per hour)', 
        y_label = 'Accident count', 
        title = 'Total accidents per speed limit',
    )
    st.plotly_chart(graph, use_container_width=True)






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
    st.markdown("""
    <div style="text-align: justify">
    One of the most important features we found in the data is that around 40% of all 
    accidents occurred near intersections. This means that intersections are a
    focal point that increases the proportion of traffic accidents. 
    The following map shows the distribution of crashes at different
    intersections in the County.
    </div>

    """,unsafe_allow_html=True)

    st.subheader("Intersection Crashes clusterized")

    st.plotly_chart(px.scatter_mapbox(df_clust_intersections, 
                            lat="DEC_LAT", 
                            lon="DEC_LONG",  
                            color='CLUSTER_COUNT', #size='CRASH_YEAR', text = 'CLUSTER_COUNT',
                            size_max=3, zoom=10))


    st.header("🚲💥 Bike crashes")
    st.write("""
    The map below shows the number of bike accidents by year, there it is possible to 
    observe that a majority of the crashes occur near intersections.
    """)
    bk_crash_options = year_list + ["2004-2020"]
    bike_crash_year = st.selectbox("Year",
                                    bk_crash_options,
                                    len(bk_crash_options)-1
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
                    size_max=15, zoom=10),use_container_width=True)

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
                    size_max=8, zoom=10),use_container_width=True)
    
    st.markdown("""
    ## Protected Intersections
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





with st.expander("💡 Our proposal"):

    st.write("""
    The data used for this study is the Allegheny County Crash Data, it is a dataset 
    containing information about the different car crashes and accidents that occurred 
    in the County between the years 2004 and 2020.  
    The data set is well structured and contains lots of details abouteach accident. 
    A data set provided by Gridwise was also employed to find some complementary insights 
    for our proposal.
    """)
