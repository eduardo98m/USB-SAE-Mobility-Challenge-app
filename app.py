from re import S
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from streamlit.legacy_caching.hashing import _key
#import SessionState


from get_dataframes import get_crash_data_df, get_gridwise_data_df, get_intersections_clust_data_df, get_bikes_clust_data_df

import plotly.graph_objects as go

import streamlit.components.v1 as components

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
        "📊 Datasets",
        '📝📊 Initial data analisys and insights', 
        '🚗🛵🥡 Delivery data insights',
        "🚦 The intersection problem",
        "🚲 The cycling context",
        "💡 Our proposal",
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

# Esto hace que al cambiar de  página se resetee la vista
components.html(
    f"""
        <p>{st.session_state.current_page }</p>
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
    """,
    height=0
)

# App layout #

st.title('USB-AI Mobility Team')

if st.session_state.current_page == "Introduction":
    st.image("images/dark_banner.png")
    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col2:
        st.image("https://media.istockphoto.com/photos/panoramic-view-of-pittsburgh-and-the-3-rivers-picture-id1093811582?k=20&m=1093811582&s=612x612&w=0&h=-KpOZ2OHlG7g2-A5fAGTCB0GtNCNVhmgZCqbr8hbzNE=")

    with col3:
        st.write("")
    

    st.markdown("""
    <div style="text-align: justify">

    Welcome to the USB-AI Mobility Team interactive booth for the SAE-AI mini-challenge.

    The objective of our entry was to develop a series of recommendations that would improve mobility accessibility, solving crucial social issues in Allegheny County, Pennsylvania, based mainly on data analysis.

    With that objective in mind, and through the use of data mining tools and extensive research we found that a good solution to improve the mobility of the county citizens is to incentivize cycling among the county residents, through the development of cycling infrastructure.

    While looking through the data, we also found other useful insights that might be worth mentioning.

    In this application, we show the complete process that went into developing our solution and the different insight that we found in the data.
    </div>

    """,unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: justify">

    A more detailed explanation of our entry can be found in our [stakeholder´s report](https://drive.google.com/file/d/1zD86ogsLWmjS-RjmHYBHnJfWyQ6GOYIn/view?usp=sharing)

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
    decrease of accidents at certain times. Therefore, we grouped the data by year, month, 
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


    Regarding the months, the ones that accumulate more accidents are January and December, probably due to two main factors: 

    * Weather: during those months (snow and rain) affects the road conditions, possibly increasing accident potential
    * Holidays: an increase in mobilization during Christmas and vacation could increase the likelihood of vehicle crashes overall


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

    The weekdays with the highest proportion of accidents are Thursdays, Fridays, and 
    Saturdays when people tend to go out to parties and gatherings, in comparison to 
    Sundays and Mondays where people tend to stay at home and only go out to work.

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
    
    Then, we decided to study how much weather conditions affect the proportion of crashes, 
    and indeed if the road is wet the accident proportion is higher, corroborating that the 
    increase of crashes at the end of the year is due to winter conditions. Accidents in dry 
    road conditions are more common overall, as this condition is the most frequent in the 
    year. It is not to be confused with an increase in the likelihood of traffic accidents 
    happening.

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

    Another important factor that we took into consideration is the road illumination 
    conditions, which are also related to the weather since, during winter, the nights 
    last longer. It can be noted that a significant proportion of accidents occur in areas
    without streetlights, thus installing streetlights in those areas could be a 
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
    speed limits is the highest overall. This is a relevant insight, as it can be 
    explained by two factors: that most roads have a 25 mph speed limit; but also that 
    such a limit may not be appropriate for some of the roads where it is imposed, i.e., 
    reducing the speed limit to 20 mph by introducing some traffic calming measures may
     result in a reduction of accidents on those roads.
    
    </div>

    """,unsafe_allow_html=True)
    # Aqui vendrian bien una referencia

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
    One of the data sets that we worked on was the Gridwise data set, with delivery 
    information of 115346 rideshares, 15512 food deliveries, and 475 grocery deliveries, 
    from July 2019 to June 2020. Among other things, we want to know the distance of these 
    deliveries, because currently all of them use an automobile for transportation
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

    st.markdown("""
    <div style="text-align: justify">

    One of the most important features we found in the data is that around **40%** of 
    all accidents occurred near intersections. Meaning that intersections are a focal 
    point that increases the proportion of traffic accidents.. 
    
    </div>

    """,unsafe_allow_html=True)

    plot_data = pd.DataFrame(df['INTERSECTION'].value_counts())
    st.plotly_chart(px.bar(plot_data), use_container_width=True)
    

    st.subheader("Intersection Crashes clusterized ✨🚦")
    st.markdown("""
        <div style="text-align: justify">
        
        A method that we used to visualize the zones of the county where there were more 
        accidents near intersections, was to cluster the data using the k-means algorithm.
         In the map below you can see that the city center is the area where more
          accidents occur near street intersections.

        </div>

        """,unsafe_allow_html=True)

    with st.expander("✨ What is clusterization ?"):
        st.markdown("""
        <div style="text-align: justify">
        
        Clustering is the task of grouping a set of objects in such a 
        way that objects in the same group (called a cluster) are more similar 
        (in some sense) to each other than to those in other groups (clusters). (Wikipedia)

        ### k-means clustering

        The KMeans algorithm clusters data by trying to separate samples in n groups of 
        equal variance, minimizing a criterion known as the inertia or within-cluster 
        sum-of-squares (see below). This algorithm requires the number of clusters to be 
        specified. It scales well to a large number of samples and has been used across a 
        large range of application areas in many different fields. (Sklearn)


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
    We also wanted to analyze bike-related accidents, and the first thing we did was plot 
    them on a map. In the map below you can see that a majority of the accidents occur 
    near intersections.
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
    This is, in fact, confirmed by the following bar plot, which tells us that around 
    **70%** of all bike-related crashes occurred near intersections.
    """)  
    plot_data = pd.DataFrame(df['INTERSECTION'].loc[df['BICYCLE']==True].value_counts())
    st.plotly_chart(px.bar(plot_data), use_container_width=True)
              
    st.subheader("Bike Crashes clusterized ✨🚲")

    st.markdown("""
    <div style="text-align: justify">
    
    As with the intersection accidents, we clusterized the bike crashes around the county 
    and found that a significant proportion of those accidents occur near the city center. 

    </div>

    """,unsafe_allow_html=True)
    st.plotly_chart(px.scatter_mapbox(df_clust_bikes, 
                    lat="DEC_LAT", lon="DEC_LONG",  
                    color='Accidents per cluster',
                    title = "Clusterized Data Bycicle accidents",
                    opacity=0.55, 
                    #color_continuous_scale= px.colors.sequential.turbo,
                    size='CRASH_YEAR',# text = 'CLUSTER_COUNT',
                    size_max=8, zoom=10),use_container_width=True)

    st.subheader("🔎Feature importance analisys")

    st.markdown("""
    <div style="text-align: justify">
    As part of the data analysis, we developed a classification model to determine what 
    features had more influence on the likelihood of a traffic accident where bikes were 
    involved. The process consists in training a random forest classifier and then 
    calculating that clasificator feature importance. The random forest employed had a 
    tree depth of 3 and was trained with the full data set.
    </div>
    """,unsafe_allow_html=True)

    with st.expander("What is feature importance analisys 🔎 ?"):
        
        st.markdown("""
        <div style="text-align: justify">
        
        The feature importance of a model is the value of inffluence that each feature of 
        the data has in the classification of the data. It is necessary to mention that 
        for all the features the sum of the feature importance is equal to one. 

        </div>

        """,unsafe_allow_html=True)

    st.image("images/Features importance for bike accidents.png")
    st.markdown("""
    <div style="text-align: justify">

    The most important features that characterized a bike accident were “propertydamage”, 
    “injury”, “injury or fatal”, and “vehicle count”. 
    These factors can be explained by the dynamics of a bike accident, where there is 
    usually, only one car involved and the cyclist is more vulnerable to the impact than 
    the car, thus these accidents are more prone to injuries.  

    There is also the possibility that the driver damages the user bike or crashes with 
    property in the sidewall triggering the property damage feature, this can also be 
    related to the importance of the “hit fixed object” feature.Other factors that show 
    relevance in the classification where the “road owner”,  “local road”,  “stateroad” 
    and “local road only” features, this can be attributed to the location where the 
    accident took place,as the majority of the cycling-related accidents occur in the 
    urban areas of the county.
    
    The other group of features that characterized a cycling 
    accidents are the intersections related features, the “non intersection”, 
    “intersection” and “intersection type” features contribute to around 10% of the feature 
    importance of the classification, this is also correlated to the fact explained in the 
    data exploration section that, 70% of all cycling accidents occur near intersections.
    
    </div>

    """,unsafe_allow_html=True)


    
    
    st.markdown("""
    <div style="text-align: justify">

    # Conclusions
    
    In this case, the data shows that regular intersections are a serious problem for all 
    traffic actors (cyclists and drivers). The safety risk that they pose is so great that 
    a significant proportion of all traffic accidents occur near them, and it extends to 
    almost 70% in the case of bicycle-related accidents. They, in turn, inhibit people 
    from cycling and make driving a more significant safety risk.

    </div>

    """,unsafe_allow_html=True)

    st.markdown("""
    ## Protected Intersections
    A proven measure to prevent and reduce these kinds of accidents is protected 
    intersections. These are a special type of intersection where the cyclist and 
    pedestrians are separated from cars by a buffer zone, and drivers gain wider 
    visibility, increasing their reaction time.
    """)

    st.image("https://cyclingtips.com/wp-content/uploads/2020/12/albert_landsdowne.jpg",
    caption="Proposed protected intersection in Melbourne Australia")



if st.session_state.current_page ==  "🚲 The cycling context":

    st.header(st.session_state.current_page)

    st.markdown("""
    <div style="text-align: justify">

    According to the discoveries and insights made in the exploratory data analysis phase, 
    there is strong evidence pointing at intersections as an unsafe place for bicycle 
    riders. Lack of alternative bicycle roads and the imminent dangers of intersections 
    could be holding back a potential alternative to the gas-powered cars that represent 
    the 72% of commuting vehicles in Allegheny County[1]. Even the city’s Director of 
    Mobility and Infrastructure, Karina Ricks, states that about 60% of that population is 
    willing to bike if they feel the lanes are safe enough[2]. Therefore, solving part of 
    Allegheny County’s mobility problems using bicycles is not only feasible and 
    beneficial but could be a solution fully embraced by its citizens.

    In this section, we will explain some of the benefits of cycling.

    </div>

    """,unsafe_allow_html=True)


    st.image("https://static01.nyt.com/images/2017/09/07/world/07Bikes1/02Bikes1-superJumbo.jpg",
    "Cyclists crossing an intersection near the Central Station of Utrecht, the Netherlands. [https://www.nytimes.com/2017/09/06/world/europe/bicycling-utrecht-dutch-love-bikes-worlds-largest-bike-parking-garages.html]")


    st.header("📈 Economics")

    st.markdown("""
    We intuitively assume that the costs associated with a bicycle are less than a vehicle, but how much less?
    """)

    plot_data = pd.DataFrame({" ":["Personal Vehicle","Bicycle","E-Bike","Bike Sharing","Rideshare"],
                               "Cost [USD]"  :   [5921, 300,518,240,18456],
                                })
                                
    #@Amin aquí deberían estar las gráficas de los temas economicos que creo que mandó yisus
    st.plotly_chart(px.bar(plot_data, x  ="Cost [USD]", y =" ",  orientation="h",
    title ="Total cost per comunig vehicle per year (logarithmic scale)",log_x=True ), use_container_width=True)
    st.write("""
    A thorough explanation of the calculations made to obtain this figure can be found [here]
    (https://docs.google.com/spreadsheets/d/1Z71tazN491rzIdnNvWWqFI-zk8twvNgIUo6BUs9BqMc/edit?usp=sharing).
    

    Looking at the graph we can see that cycling options for daily commuting are way 
    cheaper alternatives to commuting by car.
    """)


    st.markdown("""
    <div style="text-align: justify">

    The annual cost of owning a vehicle starts at 6.000$ for a common sedan, compared to 
    the 300$ that represents owning a commuting bicycle, based on the average commuting 
    distance of 16 miles on one way. The cost of owning a vehicle covers its maintenance, 
    insurance, licenses, the overall payment of the vehicle, and particularly gasoline 
    consumption. Car owners spend more than 1.200$ a year on gas, based on the average 
    commuting distance of U.S. citizens, a fuel economy of 23 MPG, and a total of 261 
    working days a year. Particularly, Pennsylvania reports gasoline prices up to 
    3.33 $/Gal, and also, this state reported the highest taxes to gasoline consumption 
    overall in the U.S., up to 0.777 $/Gal. Also, the study Transport transitions in 
    Copenhagen: Comparing the cost of cars and bicycles reach the conclusion that, on 
    average, bicycles corresponded to a 0.08 Euros/km of cost (considering the private 
    sector, social effects, and other aspects) compared to the 0.50 Euros/km of cost for 
    cars. These conclusions make bicycles a very attractive alternative.
    </div>

    """,unsafe_allow_html=True)


    st.markdown("""
    <div style="text-align: justify">

    But it’s not only the people who are getting an economical benefit out of bicycle riding, 
    around the world many cities have shown that bicycle usage as regular commuting means of 
    transportation can translate to an increase in tourism rates, like Amsterdam and Utrecht 
    in the Netherlands, Antwerp in Belgium, and Copenhagen in Denmark. Particularly, Copenhagen 
    has developed a strong bicycle culture for itself, and bicycle usage reaches 28% of the total 
    of trips reported in the country by 2019, according to the study [3]. With an overall 76% 
    of people feeling safe by using bicycles overall and aiming to reach 90% of acceptance by 
    2025, the city has gained popularity as one of the top destinations for bicycle usage. As 
    reflected in the study [4], the tourism value of being a bicycle-related country was 7.2 
    million Euros per year by 2008, representing 2% of the overall tourism of the country.
    
    </div>
    """,unsafe_allow_html=True)


    st.header("🦺✔️ Safety and Accessibility")


    st.image("https://d1q0twczwkl2ie.cloudfront.net/wp-content/uploads/2015/01/Rasmus-Hjortshoj-Cykelslangen-FRAME-13.jpg", "Elevated Bicycle Highway in Copenhagen Denmark")

    st.markdown("""
    <div style="text-align: justify">

    A very important fact that has to be mention is that 80% of people in Copenhagen have 
    access to bicyclesand adequate roads for their usage [5].  Basically,  almost 
    everyone can choose to ride a bike if theywant to use that alternative. This figure is
    reachable thanks to all the political decisions and economicalinvestment that Denmark 
    and the State of Copenhagen have done for the past 20 years. Because of this, new 
    infrastructures like bicycle highways are been developed to reduce the time cost of 
    commuting with these types of vehicles [5]. An economically accessible solution that 
    can, with the proper infrastructure,represent a widely geographically available 
    alternative for transportation for people in Allegheny County.
    
    </div>

    """,unsafe_allow_html=True)



    st.markdown("""
    <div style="text-align: justify">

    Looking at the data analysis results, there is an important effect of intersections 
    over bicycle accidents,as more than 70% of the total accident involving a bicycle in 
    Allegheny County happened in intersections.In order for people to start investing in 
    bicycle mobility, it is necessary that safety issues like these are addressed. Some 
    solutions have been proposed to solve this type of problem. A study made by the 
    Directory of Danish Roads [6] worked around 10 road applicable solutions for bicycle 
    mobility.  One ofthose solutions suggests that only by separating the traffic control 
    for bikes and for cars can reduce upto 75% the number of accidents in these situations
    .  Also, this scheme improve the sense of security of the public.
    
    </div>
    """,unsafe_allow_html=True)


    st.markdown("""
    <div style="text-align: justify">

    Another solution that is proposed by the Directory of Danish Roads [6] is the 
    development of a regularterminated cycle lane next to a separate right-turn lane for 
    vehicles.  These types of structures give the cyclers a greater sense of security as 
    they have their own space before entering the intersection. Also,forcing the car 
    lane for only right-turn decreases the number of accidents between bikes and cars by
    about 50% if previously the lane allowed for right-turn and straight-away passage. But 
    still, there arefar more impactful solutions that can improve safety for cyclers 
    in intersections. In San Francisco, aprotected intersection design resulted in 98% of 
    drivers yielding to people on bikes, and 100% yield topeople walking [7], and a study 
    in New York found that protected intersections had fewer vehicle-bikeconflicts than 
    even a dedicated turn lane with a dedicated bike signal phase [7]. The infrastructure 
    has to have the bicycle user in mind during its design. Roads are meant for cars, new
    solutions have to beapplied for better bicycle traffic.
    
    </div>
    """,unsafe_allow_html=True)

    st.header("🍃⚕️  Environment and Health")

    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col2:
        st.image("https://www.icebike.org/wp-content/uploads/2021/04/benefits-of-cycling.jpg")

    with col3:
        st.write("")

    st.markdown("""
    <div style="text-align: justify">

    A common subject of debate during the last couple of centuries has been climate change 
    and the role themobility industry plays in it. Bicycles usage is an evident 
    alternative that allows for easy access mobilityfor little to no emissions in the 
    process.  To change from a car to a bicycle as a commuting means oftransportation 
    can represent a reduction of 4.6 metric tons of carbon dioxide per year per person[8] 
    that are emitted to the atmosphere, greatly reducing the carbon footprint. The European 
    Union[8] statedthat, if car usage was reduced from 44% to 30%, there 
    would be 30% fewer traffic jams, a reduction of42% of the barrier effect of major 
    highways, 9% of people would not suffer more from noise, and otherconclusions, 
    based on a study on the city of Graz, Austria. 
    
    </div>

    """,unsafe_allow_html=True)


    st.markdown("""
    <div style="text-align: justify">
    
    But the environment is not the only one getting healthier from cycling, the World 
    Health Organization[3] recommends that healthy adults engage in, at least, 150 minutes 
    of moderate physical activity, or 75minutes of vigorous physical activity per week. 
    The European Union[8] stated also that men who cycleat least an hour a week going to 
    work had up to 50% less probability of suffering from coronary heartdisease. Also, a 
    study from [3] shows that not only man-powered bikes are good for your health, 
    e-bikeusage  during  commuting,  by  inactive  individuals,  resulted  in improvements 
    in  cardiovascular  fitnessand overall helping inactive people to 
    become physically active.  Health benefits arise even from natureexposure, resulting 
    in cognitive benefits including restoration of mental fatigue[3].
    
    </div>
    """,unsafe_allow_html=True)

    st.header("📜🛣️ Current Policies and Infrastructure")

    st.markdown("""
    <div style="text-align: justify">
    
    Being the city of Pittsburgh seat of the Allegheny County,  it’s interesting to study 
    the Bike(+) MasterPlan[9], which was published in June 2020 and it is currently being 
    implemented, one very important current project that has been developed around 
    alternatives means of transportation around the city. 
    
    </div>
    """,unsafe_allow_html=True)


    st.markdown("""
    <div style="text-align: justify">
    
    It is important to notice that the program is not only limited to bikes, the term is
    used to also include other personal mobility devices such as electric pedal-assist 
    bicycles, kick scooters or e-scooters, and another similar lightweight 
    (less than 150 pounds), low-speed (less than 20 MPH) vehicles without internal
    combustion engines[9].
    
    </div>
    """,unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: justify">

    Healthy Ride is a public bicycle sharing system that serves parts of Pittsburgh. 
    It offers three differentpayment options: 2$ / 30 min, 12$ / month and 20$ / month. 
    It has over 500 bikes at 113 Healthy Ridestations and 66,000 active users[9]. 
    
    </div>
    """,unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col2:
        st.image("images/proposal/Healthy Ride stations.png", "Map of the Healthy Ride Sations in Allegheny county")

    with col3:
        st.write("")
    

    




if st.session_state.current_page == "📊 Datasets":
    st.header(st.session_state.current_page)
    st.write("""
    
    <div style="text-align: justify">
    
    The data used for our study is the Allegheny County Crash Data from The Western 
    Pennsylvania Regional Data Center, it is a dataset containing information about 
    the different car crashes and accidents that occurred 
    in the County between the years 2004 and 2020. The data set is well structured and 
    contains lots of details about each accident.
    

    A dataset provided in the challenge by Gridwise was also employed to find some 
    complementary insights for our proposal. This dataset contianed a sample of 
    ride-share and delivery trips in Allegheny County between July 2019 and June 2020

    In both data set we found the following data types:				
    * Categorical
    * Numerical
    * Boolean
    * Geo-spacial


    </div>
    """,unsafe_allow_html=True)

    st.write("""
    The Allegheny County Crash Data Data set can be found in this [link](https://data.wprdc.org/dataset/allegheny-county-crash-data)
    """)



if st.session_state.current_page == "💡 Our proposal":
    
    st.header(st.session_state.current_page)
    st.markdown("""
    <div style="text-align: justify">
    
    Being the city of Pittsburgh seat of the Allegheny County, it’s interesting to study 
    the Bike(+) MasterPlan, which was published in June 2020 and is currently being 
    implemented. It is a very important current project that develops around alternative 
    means of transportation around the city. It is important to notice that the program is 
    not only limited to bikes, it also includes other personal mobility devices such as 
    electric pedal-assist bicycles, kick-scooters or e-scooters, and another similar 
    lightweight (less than 150 pounds), low-speed (less than 20 MPH) vehicles without 
    internal combustion engines.

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
   
    1. The East Allegheny, Strip District, and Downtown Pittsburgh areas
    2. Friendship, Bloomfield, and Shadyside.
    
    Which respectively account for 8.5% and 8.2% of the intersection crashes involving the 
    county. The goal of this proposal is to expand the Bike(+) Plan, focusing in critical 
    areas for bicyclist safety.

    </div>

    """,unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: justify">
    
    ## Delivery Companies

    We also propose to implement e-bikes as a means of delivery. The expansion of bicycle 
    infrastructure may lead to the introduction of new delivery workers who perform their 
    services using bicycles because, according to data analysis, 58% of delivery trips are 
    5 miles or less. This can be a benefit to the industry and workers because it lowers 
    the barrier to entry for a delivery job, as a car is no longer required to complete 
    customer orders. In addition, for delivery service workers, profits could increase by 
    52% by using e-bikes instead of cars to make deliveries. Because, although the number 
    of daily deliveries would decrease, the costs associated with fuel and regular vehicle 
    maintenance decrease significantly, and net profits would increase. Therefore, the 
    implementation of e-bicycles by delivery companies would mean traffic benefits within 
    the city, higher net profits for workers, and a healthier lifestyle.

    </div>

    """,unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: justify">
    
    ##  Traffic density

    To reduce traffic density, there should be noted that Mount Lebanon, Beechview and the 
    White Hall neighborhoods, located in the southern west part of the city, have high 
    traffic density during rush hour, and are not cover by the new bike rental locations 
    from the Bike(+) Plan, and so are important to be consider.
    
    </div>

    """,unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col2:
        st.image("images/proposal/Traffic density in Pittsburgh.png", 
    'Pittsburg traffic density map.')

    with col3:
        st.write("")

    




    st.markdown("""
    <div style="text-align: justify">
    
    ##  Obesity rates

    Our solution can positively affect the high obesity rates found in Allegheny County. 
    These are approximately 34%, 4% higher than the national average. That is why we 
    took into account the obesity distribution (shown in the figure below), to target 
    areas with high obesity rates, in the solution. Particularly, the northwest part of 
    the city reports obesity rates that are considerably higher than the rest of the city. 
    These neighborhoods should be taken into consideration for improving their health and 
    quality of life.
    
    </div>

    """,unsafe_allow_html=True)

    st.image("images/proposal/Obesity map.png", 
    'Pittsburg obesity distribution map.')


    st.markdown("""
    <div style="text-align: justify">
    
    ## Poverty density
    To increase accessibility to mobility, people need low-cost solutions for their daily 
    commuting means of transportation. The implementation of the Bike(+) Plan could be i
    mproved, taking into account those that cannot afford a car. In this regard, we 
    focused our proposal on the low moderate and high-moderate poverty zones.
    
    </div>

    """,unsafe_allow_html=True)

    st.image("images/proposal/Poverty density map.png", 
    'Pittsburg poverty density map: From this map we can see that entire city could benefit from this service, improving easy-access to mobility overall.')

    st.markdown("""
    <div style="text-align: justify">

    ## Traffic control systems
    
    Finally, we considered the implementation of traffic control using artificial 
    intelligence to monitor the status of traffic lights at intersections. These systems 
    can be based on computer vision for the detection of road agents (cars, bicycles, 
    motorcycles, pedestrians, etc.), and the control algorithm employed can be based on 
    reinforcement learning or traditional control theory. Currently, this style of 
    solution is used to reduce intersection delay time at traffic signals, but it could 
    also allow for a safer way to control bicycle and pedestrian traffic. However, it is 
    very important to implement measures to ensure that the systems do not violate 
    people's privacy and that appropriate tests are performed to corroborate their 
    robustness to high-risk situations.

    </div>

    """,unsafe_allow_html=True)

    st.image("https://www.artificialinventive.com/wp-content/uploads/elementor/thumbs/introducci%C3%B3n-a-visi%C3%B3n-por-computadora-oeoladq1ni8z945r0akzx7ofhs3l6jjmwslhfk9ie0.jpg",
    "Visual representation of a visual detection algorithm for dettecting objects in a street")




    


if st.session_state.current_page == "🧠 The Team":
    st.header(st.session_state.current_page)

    col1, col2, col3 = st.columns(3)
    
    col1.image("images/profile_pics/jesus.png", 
    'Jesús Pereira')
    col1.write("Mechanichal Engineering - USB")
    col1.write("[Linkedin Profile](https://www.linkedin.com/in/jeppires/?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACyfAuYBfdUUHjCot76aaeadm6q07bf6PjM)")
    col1.write("[Github Profile](https://github.com/jesusepp)")

    col1.image("images/profile_pics/amin.png", 
    'Amin Arriaga')
    col1.write("Computer Engineering - USB")
    col1.write("[Linkedin Profile](https://www.linkedin.com/in/amin-lorenzo-arriaga-utrera-8379b0177/)")
    col1.write("[Github Profile](https://github.com/ArriagaAmin)")

    col2.image("images/profile_pics/oriana.png", 
    'Oriana Petijean')
    col2.write("Production Engineering - USB")
    col2.write("[Linkedin Profile](https://www.linkedin.com/in/oriana-petitjean-a19a721b4/?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADH9wjUBYlhB96eYOzTEAbXyOI0x0Hdb-WY)")
    col2.markdown("ㅤ")

    col2.image("images/profile_pics/carlos.png", 
    'Carlos Correa')
    col2.write("Mechanichal Engineering - USB")
    col2.write("[Linkedin Profile](https://www.linkedin.com/in/carlosdanielcorrea/?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACpKGlIBIhYEqBtJmS78bEIBxPM4PU-aEzw)")
    col2.markdown("ㅤ")

    col3.image("images/profile_pics/barrera.png", 
    'José Barrera')
    col3.write("Computer Engineering - USB")
    col3.write("[Linkedin Profile](https://www.linkedin.com/in/jrbarreram/?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACvtuqIBvuk9GUtXxIB2-Vv7yyuIWQqekb4)")
    col3.write("[Github Profile](https://github.com/JRBarreraM)")

    col3.image("images/profile_pics/Eduardo.png", 
    'Eduardo López')
    col3.write("Mechanichal Engineering - USB")
    col3.write("[Linkedin Profile](https://www.linkedin.com/in/eduardo-lópez-a934ba15b/)")
    col3.write("[Github Profile](https://github.com/eduardo98m)")

    col2.write("Team Mentor")
    col2.image("images/profile_pics/ale.png", 
    'Alemayehu Admasu')
    col2.write("Research Engineer- Ford")
    col2.write("[Linkedin Profile](https://www.linkedin.com/in/alemayehu-solomon-admasu/)")
    

if st.session_state.current_page == "📚 References":
    st.header(st.session_state.current_page)
    st.markdown("""
  1. Best Place. (n.d.). Pittsburgh, Pennsylvania commuting. Retrieved October 13, 2021, from: <https://www.bestplaces.net/transportation/city/pennsylvania/pittsburgh>.
  
  2. Shumway, J. (2021, April 20). City of Pittsburgh to add hundreds of miles of new bike lanes to existing network. CBS Pittsburgh. Retrieved October 13, 2021, from: <https://pittsburgh.cbslocal.com/2021/04/20/city-of-pittsburgh-bike-lanes/>.
  
  3. Sundfør, H., Fyhri, A., & Bjørnarå, H. (2020). E-bikes—good for public health?. Advances In Transportation And Health, 251-266. doi: 10.1016/b978-0-12-819136-1.00011-5
  
  4. Københavns Kommune. (2021). Status på København 2020. Retrieved October 13, 2021,from: <https://www.kk.dk/sites/default/files/status_paa_koebenhavn_2020.pdf>
  
  5. Danish Road Directorate. (2020, June). Road Technical Solutions for Cyclists. Retrieved October 13, 2021, from: <https://cyclingsolutions.info/wp-content/uploads//2021/01/RoadTechnical-Solutions.pdf>
  
  6. Ink, S. (2020, October 16). Protected intersections. National Association of City Transportation Officials. Retrieved from: <https://nacto.org/publication/dont-give-up-at-the-intersection/protected-intersections/>.
  
  7. The environmental impacts of riding an Ebike. Aventon Bikes. (2021, February 19). Retrieved October 13, 2021, from: <https://www.aventon.com/blogs/aventon_bikes/the-environmental-impacts-of-riding-an-ebike>.
  
  8. (2016, October 19). Promoting cycling: Changes to expect. Mobility and transport - European Commission. Retrieved October 13, 2021, from: [https://ec.europa.eu/transport/road_safety/specialist/knowledge/pedestrians/
  promote_cycling_and_bicycle_helmets_or_not/promoting_cycling_changes_to_expect_en](https://ec.europa.eu/transport/road_safety/specialist/knowledge/pedestrians/promote_cycling_and_bicycle_helmets_or_not/promoting_cycling_changes_to_expect_en).
  
  9. City of Pittsburgh. (2020). Bike(+) Master Plan. Retrieved October 13, 2021 from: <https://apps.pittsburghpa.gov/redtail/images/9994_Pittsburgh_Bike+_Plan_06_15_2020.pdf>.
    """,unsafe_allow_html=True)

