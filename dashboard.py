from matplotlib.pyplot import hist
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

data_url='D:\Codes\Streamlit\SF Crime\Police_Department_Incident_Reports__2018_to_Present (1).csv'

st.title("Crime Statistics in San Francisco")
st.markdown("This application is a streamlit dashboard that can be"
"used to analyze Crime Statistics in San Francisco")


@st.cache(persist=True)
def data_load(nrows):
    data= pd.read_csv(data_url, nrows=nrows, parse_dates=[['Incident Date', 'Incident Time']])
    data.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'incident date_incident time':'date/time'}, inplace=True)
    return data


data=data_load(300000)

st.header('How many crimes occur during a given time of day?')
hour = st.slider('Hour to look at', 0, 23)
data = data[data['date/time'].dt.hour==hour]
st.markdown('Crimes between %i:00 and %i:00' % (hour, (hour+1)))
midpoint = (np.average(data['latitude']), np.average([data['longitude']]))

st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state={
        'latitude':midpoint[0],
        'longitude': midpoint[1],
        'zoom': 10.5,
        'pitch': 50,
    },
    layers=[
        pdk.Layer(
        'HexagonLayer',
        data=data[['date/time','latitude','longitude']],
        get_position = ['longitude','latitude'],
        radius =100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))


st.subheader('Breakdown by minute between %i:00 and %i:00' % (hour, (hour+1)%24))
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour+1))
]
hist=np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data=pd.DataFrame({'minute':range(60), 'crashes':hist})
fig=px.bar(chart_data, x='minute', y='crashes', hover_data=['minute','crashes'], height=400)
st.write(fig)


st.header('Division by type of crime')
select = st.selectbox('Type of Crime',['Arson', 'Suspicious Occ', 'Other Miscellaneous',
       'Motor Vehicle Theft', 'Non-Criminal', 'Burglary', 'Larceny Theft',
       'Malicious Mischief', 'Assault', 'Weapons Carrying Etc',
       'Weapons Offense', 'Lost Property', 'Recovered Vehicle', 'Warrant',
       'Fraud', 'Drug Offense',
       'Offences Against The Family And Children', 'Disorderly Conduct',
       'Other Offenses', 'Miscellaneous Investigation', 'Missing Person',
       'Suspicious', 'Traffic Violation Arrest', 'Robbery', 'Other',
       'Traffic Collision', 'Drug Violation', 'Stolen Property',
       'Courtesy Report', 'Case Closure', 'Fire Report', 'Vandalism',
       'Forgery And Counterfeiting', 'Sex Offense', 'Vehicle Impounded',
       'Suicide', 'Vehicle Misplaced',
       'Human Trafficking (A), Commercial Sex Acts', 'Civil Sidewalks',
       'Prostitution', 'Homicide', 'Embezzlement', 'Liquor Laws', 'Rape',
       'Weapons Offence', 'Motor Vehicle Theft?', 'Gambling',
       'Human Trafficking, Commercial Sex Acts'])


# st.write(data.query('injured_pedestrians >= 1')[['on_street_name','injured_pedestrians']].sort_values(by=['injured_pedestrians'],ascending=False).dropna(how='any')[:5])
data['Crime Count']=1
x=data.groupby(['analysis neighborhood','incident category']).count().reset_index()
st.write((x[x['incident category']==select][['analysis neighborhood','Crime Count']]).sort_values(by=['Crime Count'],ascending=False).dropna(how='any'))