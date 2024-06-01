import streamlit as st
import pandas as pd
import plotly_express as px
cars = pd.read_csv('vehicles_us.csv')
cars['make'] = cars['model'].str.split().str[0]
st.header('Data Viewer')
st.dataframe(cars)
st.header('Vehicle Types by Make')
fig1 = px.histogram(cars, x='make', color='type')
st.write(fig1)
st.header('Histogram of Condition vs Model Year')
fig2 = px.histogram(cars, x='model_year', color='condition')
st.write(fig2)
st.header('Compare Price Distribution between Makes')
make_list = sorted(cars['make'].unique())
make_1 = st.sidebar.selectbox(
    label = 'Select Make 1',
    options=make_list,
    index=make_list.index('honda')
)
make_2 = st.sidebar.selectbox(
    label='Select Make 2',
    options=make_list,
    index=make_list.index('toyota')
)
mask_filter = (cars['make'] == make_1) | (cars['make'] == make_2)
cars_filtered = cars[mask_filter]
normalize = st.sidebar.checkbox('Normalize Histogram', value=True, key=1)
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
st.header('Average Cost by Make')
cars_ppm = cars.groupby('make').agg(avg_price=('price', 'mean')).reset_index()
fig4 = px.bar(cars_ppm, x='make', y='avg_price')
st.write(fig4)
st.header('Price Distribution by Make (All)')
fig5 = px.box(cars, x='price', y='make')
st.write(fig5)
st.header('Average Cost by Model Year')
cars_ppmy = cars.groupby('model_year').agg(avg_price=('price', 'mean')).reset_index()
fig6 = px.scatter(cars_ppmy, x='model_year', y='avg_price')
st.write(fig6)
st.header('Cost by Condition')
normalize = st.sidebar.checkbox('Normalize Histogram', value=True, key=2)
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
