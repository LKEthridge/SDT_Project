import streamlit as st
import pandas as pd
import plotly_express as px

#import and clean data
cars = pd.read_csv('vehicles_us.csv')
cars['make'] = cars['model'].str.split().str[0]
cars['is_4wd'] = cars['is_4wd'].fillna('0')
cars['model_year'] = cars[['model_year', 'model']].groupby('model').transform(lambda x:x.fillna(x.median()))
cars['cylinders'] = cars[['cylinders', 'model']].groupby('model').transform(lambda x:x.fillna(x.median()))
cars['odometer'] = cars[['odometer', 'condition']].groupby('condition').transform(lambda x:x.fillna(x.mean()))
cars = cars.fillna('Unknown')

#Data Viewer
st.header('Data Viewer')
st.dataframe(cars)

#Figure 1
st.header('Figure 1: Vehicle Types by Make')
fig1 = px.histogram(cars, x='make', color='type')
st.write(fig1)

#figure 2
st.header('Figure 2: Histogram of Condition vs Model Year')
fig2 = px.histogram(cars, x='model_year', color='condition')
st.write(fig2)

#figure 3
st.header('Figure 3: Compare Price Distribution between Makes')
make_list = sorted(cars['make'].unique())
make_1 = st.sidebar.selectbox(
    label = 'Figure 3: Select Make 1',
    options=make_list,
    index=make_list.index('honda')
)
make_2 = st.sidebar.selectbox(
    label='Figure 3: Select Make 2',
    options=make_list,
    index=make_list.index('toyota')
)
mask_filter = (cars['make'] == make_1) | (cars['make'] == make_2)
cars_filtered = cars[mask_filter]
normalize = st.sidebar.checkbox('Normalize Histogram for Figure 3', value=True, key=1)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
fig3 = px.histogram(cars_filtered,
                   x='price',
                   nbins=30,
                   color='make',
                   histnorm=histnorm,
                   barmode='overlay')
st.write(fig3)

#figure 4
st.header('Figure 4: Average Cost by Make')
cars_ppm = cars.groupby('make').agg(avg_price=('price', 'mean')).reset_index()
fig4 = px.bar(cars_ppm, x='make', y='avg_price')
st.write(fig4)

#figure 5
st.header('Figure 5: Price Distribution by Make (All)')
fig5 = px.box(cars, x='price', y='make')
st.write(fig5)

#figure 6
st.header('Figure 6: Average Cost by Model Year')
cars_ppmy = cars.groupby('model_year').agg(avg_price=('price', 'mean')).reset_index()
fig6 = px.scatter(cars_ppmy, x='model_year', y='avg_price')
st.write(fig6)

#figure 7
st.header('Figure 7: Cost by Condition')
normalize = st.sidebar.checkbox('Normalize Histogram for Figure 7', value=True, key=2)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
fig7 = px.histogram(cars_filtered,
                    x='price',
                    nbins=30,
                    color='condition',
                    histnorm=histnorm,
                    barmode='overlay')
st.write(fig7)
