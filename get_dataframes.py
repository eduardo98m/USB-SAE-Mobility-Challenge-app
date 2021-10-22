
import pandas as pd
import streamlit as st

@st.cache()
def get_crash_data_df():

    try:

        df = pd.read_csv("datasets/Allegheny County Crash Data Clean.csv")

    except FileNotFoundError: 

    
        url  ='https://drive.google.com/file/d/1qKICn7Jtw9b9RDv4ACgZVypAamAAFpFE/view?usp=sharing'
        path ='https://drive.google.com/uc?id=' + url.split('/')[-2]

        df = pd.read_csv(path)


        #Data set is trated
        
        # bool features

        df['SCH_BUS_IND'] = df['SCH_BUS_IND'].replace({
                        'N':0, '0':0, '0.0':0, 0:0, 0.0:0, 
                        'Y':1, '1':1, '1.0':1, 1.0:1, 1:1
                    })
        bool_features=['AGGRESSIVE_DRIVING',
        'ALCOHOL_RELATED',
        'BICYCLE',
        'CELL_PHONE',
        'COMM_VEHICLE',
        'CROSS_MEDIAN',
        'CURVE_DVR_ERROR',
        'CURVED_ROAD',
        'DEER_RELATED',
        'DISTRACTED',
        'DRINKING_DRIVER',
        'DRIVER_16YR',
        'DRIVER_17YR',
        'DRIVER_65_74YR',
        'DRIVER_75PLUS',
        'FATAL',
        'FATIGUE_ASLEEP',
        'FIRE_IN_VEHICLE',
        'HAZARDOUS_TRUCK',
        'HIT_BARRIER',
        'HIT_BRIDGE',
        'HIT_DEER',
        'HIT_EMBANKMENT',
        'HIT_FIXED_OBJECT',
        'HIT_GDRAIL',
        'HIT_GDRAIL_END',
        'HIT_POLE',
        'HIT_TREE_SHRUB',
        'HO_OPPDIR_SDSWP',
        'HVY_TRUCK_RELATED',
        'ICY_ROAD',
        'ILLEGAL_DRUG_RELATED',
        'ILLUMINATION_DARK',
        'IMPAIRED_DRIVER',
        'INJURY',
        'INJURY_OR_FATAL',
        'INTERSECTION',
        'INTERSTATE',
        'LANE_CLOSED',
        'LIMIT_65MPH',
        'LOCAL_ROAD',
        'LOCAL_ROAD_ONLY',
        'MOTORCYCLE',
        'NHTSA_AGG_DRIVING',
        'NO_CLEARANCE',
        'NON_INTERSECTION',
        'NTFY_HIWY_MAINT',
        'OVERTURNED',
        'PEDESTRIAN',
        'PHANTOM_VEHICLE',
        'PROPERTY_DAMAGE_ONLY',
        'PSP_REPORTED',
        'REAR_END',
        'SCHOOL_ZONE',
        'SCH_BUS_IND',
        'SIGNALIZED_INT',
        'SNOW_SLUSH_ROAD',
        'SPEEDING',
        'SPEEDING_RELATED',
        'STATE_ROAD',
        'STOP_CONTROLLED_INT',
        'SV_RUN_OFF_RD',
        'TAILGATING',
        'TRAIN',
        'TRAIN_TROLLEY',
        'TROLLEY',
        'TURNPIKE',
        'UNBELTED',
        'UNDERAGE_DRNK_DRV',
        'UNLICENSED',
        'UNSIGNALIZED_INT',
        'VEHICLE_FAILURE',
        'VEHICLE_TOWED',
        'WET_ROAD',
        'WORK_ZONE',
        'WORKERS_PRES',
        'WZ_CLOSE_DETOUR',
        'WZ_FLAGGER',
        'WZ_LAW_OFFCR_IND',
        'WZ_LN_CLOSURE',
        'WZ_MOVING',
        'WZ_OTHER',
        'WZ_SHLDER_MDN',
        ]


        for col in bool_features:
            df[col]=df[col].astype(bool)

        # Int features
        int_features=[
        'AUTOMOBILE_COUNT',
        'BELTED_DEATH_COUNT',
        'BICYCLE_COUNT',
        'BICYCLE_DEATH_COUNT',
        'BUS_COUNT',
        'COMM_VEH_COUNT',
        'CRASH_MONTH',
        'CRASH_YEAR',
        'DAY_OF_WEEK',
        'DRIVER_COUNT_16YR',
        'DRIVER_COUNT_17YR',
        'DRIVER_COUNT_65_74YR',
        'DRIVER_COUNT_75PLUS',
        'FATAL_COUNT',
        'HEAVY_TRUCK_COUNT',
        'HOUR_OF_DAY',
        'INJURY_COUNT',
        'MCYCLE_DEATH_COUNT',
        'MOTORCYCLE_COUNT',
        'OFFSET',
        'PED_COUNT',
        'PED_DEATH_COUNT',
        'PERSON_COUNT',
        'SUV_COUNT',
        'UNB_DEATH_COUNT',
        'UNK_INJ_DEG_COUNT',
        'UNK_INJ_PER_COUNT',
        'VAN_COUNT',
        'VEHICLE_COUNT',
                ]
        for col in int_features:
            print(col)
            df[col]=df[col].astype(int, errors='ignore')



        # Categorical fetures
        categorical_feature_dicts = {
            "COLLISION_TYPE":{  0 : 'Non collision',
                                1 : 'Rear-end',
                                2 : 'Head-on',
                                3 : 'Rear-to-rear (Backing)',
                                4 : 'Angle',
                                5 : 'Sideswipe (same dir.)',
                                6 : 'Sideswipe (Opposite dir.)',
                                7 : 'Hit fixed object',
                                8 : 'Hit pedestrian',
                                9 : 'Other or Unknown',
                                98 : 'Other',
                                99 : 'Unknown'},
            "DAY_OF_WEEK": {
                1 : 'Sunday',
                2 : 'Monday',
                3 : 'Tuesday',
                4 : 'Wednesday',
                5 : 'Thursday',
                6 : 'Friday',
                7 : 'Saturday',
                    },
            "ILLUMINATION":{
                1 : "Daylight",
                2 : "Dark - no street lights",
                3 : "Dark - street lights",
                4 : "Dusk",
                5 : "Dawn",
                6 : "Dark - unknown roadway lighting",
                8 : "Other",
                9 : "Unknown (expired)",
            },
            "INTERSECT_TYPE":{  0 : 'Mid-block',
                                1 : 'Four way intersection',
                                2 : '"T" intersection',
                                3 : '"Y" intersection',
                                4 : 'Traffic circle or Round About',
                                5 : 'Multi-leg intersection',
                                6 : 'On ramp',
                                7 : 'Off ramp',
                                8 : 'Crossover',
                                9 : 'Railroad crossing',
                                10 : 'Other',
                                99 : 'Unknown (expired)',
                                11: 'Unknown (expired)',
                                12: 'Unknown (expired)',
                            },
            "LN_CLOSE_DIR":{1 : "North",
                            2 : "South",
                            3 : "East",
                            4 : "West",
                            5 : "North and South",
                            6 : "East and West",
                            7 : "All",
            },
            "LOCATION_TYPE":{
                0 : 'Not applicable',
                1 : 'Underpass',
                2 : 'Ramp',
                3 : 'Bridge',
                4 : 'Tunnel',
                5 : 'Toll Booth',
                6 : 'Cross over related',
                7 : 'Driveway or Parking Lot',
                8 : 'Ramp and bridge',
                9 : 'Unknown',
            },

            'MAX_SEVERITY_LEVEL' :{
                                0 : 'Not injured',
                                1 : 'Killed',
                                2 : 'Major injury',
                                3 : 'Moderate injury',
                                4 : 'Minor injury',
                                8 : 'Injury/ Unknown Severity',
                                9 : 'Unknown'
                                },
            'RDWY_SURF_TYPE_CD':{
                1 : 'Concrete',
                2 : 'Blacktop',
                3 : 'Brick or Block',
                4 : 'Slag, Gravel, or Stone',
                5 : 'Dirt',
                8 : 'Other',
                9 : 'Unknown',
            },
            'RELATION_TO_ROAD':{
                1 : 'On roadway',
                2 : 'Shoulder',
                3 : 'Median',
                4 : 'Roadside (off trafficway; on vehicle area)',
                5 : 'Outside trafficway (in area not meant for vehicles)',
                6 : 'In parking lane',
                7 : 'Gore (intersection of ramp and highway)',
                9 : 'Unknown'
            },
            'ROAD_CONDITION':{
                0 : 'Dry',
                1 : 'Wet',
                2 : 'Sand/ mud/ dirt/ oil/ or gravel',
                3 : 'Snow covered',
                4 : 'Slush',
                5 : 'Ice',
                6 : 'Ice Patches',
                7 : 'Water - standing or moving',
                8 : 'Other',
                9 : 'Unknown (expired)',
                98 : 'Other',
                99 : 'Unknown' 
            },
            'ROAD_OWNER':{
                1 : 'Interstate - non turnpike',
                2 : 'State highway',
                3 : 'County road',
                4 : 'Local road or street',
                5 : 'East-West portion of turnpike',
                6 : 'Turnpike spur (extension)',
                7 : 'Private Road',
                9 : 'Other or Unknown'
            },
            'SPEC_JURIS_CD':{
                0 : 'No Special Jurisdiction',
                1 : 'National Park',
                2 : 'Military',
                3 : 'Indian Reservation',
                4 : 'College/University Campus',
                5 : 'Other Federal Sites',
                8 : 'Other',
                9 : 'Unknown'
                },
            'TCD_FUNC_CD':{
                0 : 'No Controls',
                1 : 'Device not Functioning',
                2 : 'Device Functioning improperly',
                3 : 'Device Functioning properly',
                4 : 'Emergency Preemptive Signal',
                9 : 'Unknown'
            },
            'TCD_TYPE':{
                0 : 'Not applicable',
                1 : 'Flashing traffic signal',
                2 : 'Traffic signal',
                3 : 'Stop sign',
                4 : 'Yield sign',
                5 : 'Active RR crossing controls',
                6 : 'Passive RR crossing controls',
                7 : 'Police officer or flagman',
                8 : 'Other Type TCD',
                9 : 'Unknown',
            },
        'WEATHER' :{1 : 'Blowing Sand, Soil, Dirt',
            2 : 'Blowing Snow',
            3 : 'Clear',
            4 : 'Cloudy',
            5 : 'Fog, Smog, Smoke',
            6 : 'Freezing Rain or Freezing Drizzle',
            7 : 'Rain',
            8 : 'Severe Crosswinds',
            9 : 'Sleet or Hail',
            10 : 'Snow',
            98 : 'Other',
            99 : 'Unknown'},

            'WORK_ZONE_LOC':{
                1 : 'Before the 1st work zone warning sign',
                2 : 'Advance warning area',
                3 : 'Transition area',
                4 : 'Activity area',
                5 : 'Termination area',
                8 : 'Other'
            },

            'WORK_ZONE_TYPE':{  1 : 'Construction',
                                2 : 'Maintenance',
                                3 : 'Utility company',
                                8 : 'Other'}
        }
        
                                

        for key in categorical_feature_dicts.keys():
            df[key] = df[key].replace(categorical_feature_dicts[key])
            df[key]=df[key].astype('category', errors='ignore')
        
        float_features = [
                    'SPEED_LIMIT',
                    'CONS_ZONE_SPD_LIM',
        ]   

        for key in float_features:
            df[key]=df[key].astype(float)


        str_features = ['ADJ_RDWY_SEQ',
                    "ACCESS_CTRL",
                    
        ]

        for key in str_features:
            df[key]=df[key].astype(str)

        df.to_csv("datasets/Allegheny County Crash Data Clean.csv")
    
    finally:

        return df



@st.cache()
def get_gridwise_data_df():
    try:

        df = pd.read_csv("datasets/gridwise_df.csv")

    except FileNotFoundError: 

    
        url  ='https://drive.google.com/file/d/19d-nOUl798BPI9bt9VjJUrUiklmq1BAN/view?usp=sharing'
        path ='https://drive.google.com/uc?id=' + url.split('/')[-2]

        df = pd.read_csv(path)

        df.to_csv("datasets/gridwise_df.csv")

    finally:

        return df


