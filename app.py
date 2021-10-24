import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from streamlit.legacy_caching.hashing import _key
#import SessionState


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
    initial_sidebar_state='auto',
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
st.sidebar.subheader("Index")

pages = ['Introduction', 
                '📝📊 Initial data analisys and insights', 
                '🚗🛵🥡 Delivery data insights',
                "🚦 The intersection problem",
                "💡 Our proposal",
                "🚀 Future benefits",
                "📈 Economics",
                "📊 Datasets",
                "🧠 The Team",
                "📚 References"
]
#a = st.sidebar.empty()

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Introduction'

if 'index' not in st.session_state:
    st.session_state.index = 0

st.session_state.current_page = st.sidebar.radio(
                                    "",
                                    pages)
                                    #st.session_state.index)

#st.session_state.index = pages.index(st.session_state.current_page)

# App layout #
st.title('USB-AI Mobility Team')

if st.session_state.current_page == "Introduction":
    st.image("https://media.istockphoto.com/photos/panoramic-view-of-pittsburgh-and-the-3-rivers-picture-id1093811582?k=20&m=1093811582&s=612x612&w=0&h=-KpOZ2OHlG7g2-A5fAGTCB0GtNCNVhmgZCqbr8hbzNE=")

    st.markdown("""
    <div style="text-align: justify">

    Welcome to the USB-AI Mobility Team interactive booth for the SAE-AI mini-challenge.

    The objective of our entry was to develop a series of recommendations that would improve mobility accessibility, solving crucial social issues in Allegheny County, Pennsylvania, based mainly on data analysis.

    With that objective in mind, and through the use of data mining tools and extensive research we found that a good solution to improve the mobility of the county citizens is to incentivize cycling among the county residents, through the development of cycling infrastructure.

    While looking through the data, we also found other useful insights that might be worth mentioning.

    In this application, we show the complete process that went into developing our solution and the different insight that we found in the data.
    </div>

    """,unsafe_allow_html=True)




if  st.session_state.current_page == '📝📊 Initial data analisys and insights':
    st.header(st.session_state.current_page)
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
    probably due to two main factors: the weather during those months (snow and rain) affects
    the road conditions boosting accidents; while christmas and vacation events tend to the 
    mobilize many people, increasing the likelihood of vehicle crashes. 

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





if st.session_state.current_page == "🚗🛵🥡 Delivery data insights":
    st.header(st.session_state.current_page)
   
    #st.plotly_chart(px.pie(df, values='tip', names='day'), use_container_width=True)
    st.write("""
    One of the dataset that we work on was a gridwise dataset with delivery information of: 
    115346 rideshare, 15512 food delivery and 475 grocery, from July 2019 to June 2020.
    Amongs other things we want to know the distance of this delivery, because currently
    all of them use an automovile for transportation.
    """)

    fig = px.histogram(df_gw, x = "distance", labels=dict(probability_density="Count", distance="Distance in miles"))
    fig.update_xaxes(range=[0, 40])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div style="text-align: justify">

    It becomes clear that there is a high frecuency on the short distance side of the figure.
    Actually 58 percent of the deliveries travels a distance of 5 miles or less.
    This means that more than half hose trips can be completed by cycling.
    </div>
    """,unsafe_allow_html=True)

    




if st.session_state.current_page == "🚦 The intersection problem":
    st.header(st.session_state.current_page)
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

    st.subheader("Intersection Crashes clusterized ✨🚦")
    st.markdown("""
        <div style="text-align: justify">
        
        A method that we use to visualize the zones of the county where there were more 
        accidents near instersections, was to clusterize the data using the k-means 
        algorithm. In the map below it is possible to see that the city center is the area 
        where are more accidents occur near road intersections.

        </div>

        """,unsafe_allow_html=True)

    with st.expander("✨ What is clusterization"):
        st.markdown("""
        <div style="text-align: justify">
        
        Clustering is the task of grouping a set of objects in such a 
        way that objects in the same group (called a cluster) are more similar 
        (in some sense) to each other than to those in other groups (clusters). (Wikipedia)

        ### k-means clustering

        The KMeans algorithm clusters data by trying to separate samples in n groups of 
        equal variance, minimizing a criterion known as the inertia or within-cluster 
        sum-of-squares (see below). This algorithm requires the number of clusters to 
        be specified. It scales well to large number of samples and has been used across 
        a large range of application areas in many different fields. (Sklearn)


        </div>

        """,unsafe_allow_html=True)
        st.image("https://d33wubrfki0l68.cloudfront.net/e1aaf634f896d77c5dd6bb59a4a28b18350cf3b8/8060f/wp-content/uploads/2019/07/clustering.png")



    st.plotly_chart(px.scatter_mapbox(df_clust_intersections, 
                            lat="DEC_LAT", 
                            lon="DEC_LONG",  
                            color='CLUSTER_COUNT', #size='CRASH_YEAR', text = 'CLUSTER_COUNT',
                            size_max=3, zoom=10),use_container_width=True)


    st.header("🚲💥 Bike related crashes")
    st.write("""
    We also wanted to analize bike related accidents and the first thing we did was to 
    them plot in a map.In the map it is possible to  observe that a majority of the 
    accidents occur near intersections.
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

    
    st.markdown("""
    This is in fact confirmed by the following plot, aroud **70%** of 
    all bike related crashes ocurr near intersections.
    """)  
    plot_data = pd.DataFrame(df['INTERSECTION'].loc[df['BICYCLE']==True].value_counts())
    st.plotly_chart(px.bar(plot_data), use_container_width=True)
              
    st.subheader("Bike Crashes clusterized ✨🚲")
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
    A proven meassure to prevent and reduce these kind of accidents are protected intersections,
    These are a special type of intersection where the cyclist and pedestrians are 
    separated from cars by a buffer zone, and drivers gain wider visibility and thus 
    increase their reaction time.
    """)

    st.image("https://cyclingtips.com/wp-content/uploads/2020/12/albert_landsdowne.jpg",
    caption="Proposed protected intersection in Melbourne Australia")



if st.session_state.current_page == "📈 Economics":

    plot_data = pd.DataFrame({" ":["Personal Vehicle","Bicycle","E-Bike","Bike Sharing","Rideshare"],
                               "Cost [USD]"  :   [5921, 300,518,240,18456],
                                })
                                
    #@Amin aquí deberían estar las gráficas de los temas economicos que creo que mandó yisus
    st.plotly_chart(px.bar(plot_data, x  ="Cost [USD]", y =" ",  orientation="h",
    title ="Total cost per comunig vehicle per year (logarithmic scale)",log_x=True ), use_container_width=True)
    st.write("""
    Looking at the graph we can see that cycling options for daily comunting are 
    way cheaper alternatives to cimmuting by car.
    """)

    st.write("[Calculations](https://docs.google.com/spreadsheets/d/1Z71tazN491rzIdnNvWWqFI-zk8twvNgIUo6BUs9BqMc/edit?usp=sharing)")

    






if st.session_state.current_page == "📊 Datasets":
    st.header(st.session_state.current_page)
    st.write("""
    The data used for this study is the Allegheny County Crash Data, it is a dataset 
    containing information about the different car crashes and accidents that occurred 
    in the County between the years 2004 and 2020.  
    The data set is well structured and contains lots of details abouteach accident. 
    A data set provided by Gridwise was also employed to find some complementary insights 
    for our proposal.
    """)



if st.session_state.current_page == "💡 Our proposal":
    st.header(st.session_state.current_page)
    st.markdown("""
    <div style="text-align: justify">
    
    Being the city of Pittsburgh seat of the Allegheny County, it’s interesting to study 
    the Bike(+) MasterPlan, which was published in June 2020 and 
    it is currently being implemented, one very importantcurrent project that has been 
    developed around alternatives means of transportation around the city. 
    It is important to notice that the program is not only limited to bikes, 
    the term is used to also includeother personal mobility devices such as electric
    pedal-assist bicycles, kick scooters or e-scooters, andanother similar lightweight 
    (less than 150 pounds), low-speed (less than 20 MPH) vehicles without 
    internalcombustion engines.

    </div>

    """,unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col2:
        st.image("https://apps.pittsburghpa.gov/redtail/images/9995_Bike(+)_Plan_Cover.JPG")

    with col3:
        st.write("")
    

    st.markdown("""
    <div style="text-align: justify">
    
    Our proposal for protected intersections will focus, in an initial phase, on the two 
    sectors that contain the highest percentage of crashes that we want to avoid. The data
    analysis showed that the areas to be used would be:

    1. The East Allegheny, Strip District and Downtown Pittsburgh areas 
    2. Friendship, Bloomfield and Shadyside.


    Which respectively account for 8.5% and 8.2% of the intersection crashes involving the 
    county. The goal of this proposal is to focus the Bike(+) Plan to increase bicyclist 
    safety in at-risk areas.

    </div>

    """,unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: justify">
    
    ##

    We also propose to implement electric bicycles as a means of delivery. The expansion 
    of bicycle infrastructure may lead to the introduction of new types of delivery 
    workers who perform their services using bicycles because, according to data analysis, 
    58% of delivery trips are 5 miles or less. This can be a benefit to the industry and 
    workers because it lowers the barrier to entry for a delivery job, as a car is no l
    onger required to complete customer orders. In addition, for delivery service workers, 
    profits would increase by 52% by using electric bikes instead of cars to make 
    deliveries. Because, although the number of daily deliveries would decrease, the costs 
    associated with fuel and regular vehicle maintenance decrease significantly and net 
    profit would increase. Therefore, the implementation of electric bicycles by delivery 
    companies would mean traffic benefits within the city, higher net profits for workers, 
    and a healthier lifestyle.

    </div>

    """,unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: justify">
    
    ##  Traffic density

    With the objective of reducing traffic density, there should be noted that Mount 
    Lebanon, Beechview and the White Hall neighborhoods,located in the southern west part 
    of the city, have high traffic density during rush hour, and are not cover by the new bike 
    rental locations from the Bike(+) Plan, and so are important to be consider.
    
    </div>

    """,unsafe_allow_html=True)

    st.image("images/proposal/Traffic density in Pittsburgh.png", 
    'Pittsburg traffic density map.')




    st.markdown("""
    <div style="text-align: justify">
    
    ##  Obesity rates

    Our solution can positvely affect  the high 
    obesity rates found in Allegheny County being approximately  34%, 4% higher than the national 
    average.  That is why we took into account the obesity distribution (show in the figure below),
    to target areas with high obesity rates
    in the solution.  Particularly, the northwest part ofthe city reports obesity rates 
    that are considerably higher than the rest of the city.  This neighborhoods should be 
    taken into consideration for improving their health and quality of life. 
    
    </div>

    """,unsafe_allow_html=True)

    st.image("images/proposal/Obesity map.png", 
    'Pittsburg obesity distribution map.')


    st.markdown("""
    <div style="text-align: justify">
    
    ## Poverty density

    The implementation of the Bike (+) Plan could 
    be a solution for those that do not have the possibility to afford a car. In this regard, 
    we take into account our target to be the low moderate and high-moderate poverty zones.  
    
    </div>

    """,unsafe_allow_html=True)

    st.image("images/proposal/Poverty density map.png", 
    'Pittsburg poverty density map: From this map we can see that entire city could benefit from this service, improving easy-access to mobility overall.')

    st.markdown("""
    <div style="text-align: justify">

    ## Traffic control systems
    
    Finally, we consider the implementation of traffic control using artificial 
    intelligence to monitor the status of traffic lights at intersections. These systems 
    can be based on computer vision for detection of road agents (cars, bicycles, 
    motorcycles, pedestrians, etc.) and the control algorithm employed can be based on 
    reinforcement learning or traditional control theory. Currently, this style of 
    solution is used to reduce intersection delay time at traffic signals, but it could 
    also allow for a safer way to control bicycle and pedestrian traffic. However, it is 
    very important to implement measures to ensure that the systems do not violate 
    people's privacy and that appropriate tests are performed on the systems to 
    corroborate their robustness to high-risk situations.

    </div>

    """,unsafe_allow_html=True)

    st.image("https://www.artificialinventive.com/wp-content/uploads/elementor/thumbs/introducci%C3%B3n-a-visi%C3%B3n-por-computadora-oeoladq1ni8z945r0akzx7ofhs3l6jjmwslhfk9ie0.jpg",
    "Visual representation of a visual detection algorithm for dettecting objects in a street")


if st.session_state.current_page == "🚀 Future benefits":

    st.image("https://static01.nyt.com/images/2017/09/07/world/07Bikes1/02Bikes1-superJumbo.jpg",
    "Cyclists crossing an intersection near the Central Station of Utrecht, the Netherlands. [https://www.nytimes.com/2017/09/06/world/europe/bicycling-utrecht-dutch-love-bikes-worlds-largest-bike-parking-garages.html]")

    st.markdown("""
    <div style="text-align: justify">

    ## 
    
    

    </div>

    """,unsafe_allow_html=True)


if st.session_state.current_page == "🧠 The Team":

    st.write("[Párrafo hablando paja del equipo]")
    col1, col2, col3 = st.columns(3)
    
    col1.write("Mechanichal Engineering - USB")
    col1.write("[Linkedin Profile](https://www.linkedin.com/in/jeppires/?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACyfAuYBfdUUHjCot76aaeadm6q07bf6PjM)")
    col1.write("[Github Profile](https://github.com/jesusepp)")

    col1.write("Computer Engineering - USB")
    col1.write("[Linkedin Profile](https://www.linkedin.com/in/amin-lorenzo-arriaga-utrera-8379b0177/)")
    col1.write("[Github Profile](https://github.com/eduardo98m)")

    col2.write("Production Engineering - USB")
    col2.write("[Linkedin Profile](https://www.linkedin.com/in/oriana-petitjean-a19a721b4/?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADH9wjUBYlhB96eYOzTEAbXyOI0x0Hdb-WY)")
    col2.write("[Github Profile](https://github.com/eduardo98m)")

    col2.write("Mechanichal Engineering - USB")
    col2.write("[Linkedin Profile](https://www.linkedin.com/in/carlosdanielcorrea/?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACpKGlIBIhYEqBtJmS78bEIBxPM4PU-aEzw)")
    col2.write("[Github Profile](https://github.com/eduardo98m)")


    col3.write("Computer Engineering - USB")
    col3.write("[Linkedin Profile](https://www.linkedin.com/in/jrbarreram/?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACvtuqIBvuk9GUtXxIB2-Vv7yyuIWQqekb4)")
    col3.write("[Github Profile](https://github.com/JRBarreraM)")

    col3.write("Mechanichal Engineering - USB")
    col3.write("[Linkedin Profile](https://www.linkedin.com/in/eduardo-lópez-a934ba15b/)")
    col3.write("[Github Profile](https://github.com/eduardo98m)")


    col2.write("Research Engineer- Ford")
    col2.write("[Linkedin Profile](https://www.linkedin.com/in/alemayehu-solomon-admasu/)")
    col2.write("[Github Profile](https://github.com/eduardo98m)")

if st.session_state.current_page == "📚 References":
    st.write("Amin mete las refencias aqui")

"""
col1, col2, col3 = st.columns([1,6,1])

with col1:
    
    if st.session_state.current_page !=  pages[0]:
        prev =  st.button('Previous', key="previous")
        if prev:
            print("atras")
            st.session_state.index = pages.index(st.session_state.current_page) - 1
            #st.session_state.current_page = pages[st.session_state.index ]
            prev = False
            

with col3:
    
    if st.session_state.current_page !=  pages[-1]:
        
        next =  st.button('Next', key="next")
        if next:
            print("adelante")
            st.session_state.index = pages.index(st.session_state.current_page) + 1
            #st.session_state.current_page = pages[st.session_state.index ]
            next = False
"""