import streamlit as st
import pandas as pd
import pickle as pkl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

st.beta_set_page_config(layout="centered", initial_sidebar_state="expanded")

def devuelveDataSet(dataSelected):
    if dataSelected == "Pipetas":
        dataSet = pd.read_csv('./data_pip.csv', index_col="Fecha",parse_dates=[0])
    elif dataSelected == "Sedantes":
        dataSet = pd.read_csv('./data_sed.csv', index_col="Fecha",parse_dates=[0])
    elif dataSelected == "T4":
        dataSet = pd.read_csv('./data_t4.csv', index_col="Fecha",parse_dates=[0])
    elif dataSelected == "T4P":
        dataSet = pd.read_csv('./data_t4p.csv', index_col="Fecha",parse_dates=[0])
    return dataSet

def devuleveGraph(dataSetTrain,dataSetTest,predict,nPeriods):
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')
    datafile = pd.concat([dataSetTrain,dataSetTest])
    fig, ax = plt.subplots(num=None, figsize=(7, 7), dpi=160, facecolor='w', edgecolor='k')
    ax.plot(dataSetTrain.index, dataSetTrain, label='observed')
    ax.plot(dataSetTest.iloc[0:nPeriods].index, forecast, color='r', label='forecast')
    ax.plot(dataSetTest.iloc[0:nPeriods].index, dataSetTest.iloc[0:nPeriods], label='test')
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    datemin = datetime.date(datafile.index.min().year, 1, 1)
    datemax = datetime.date(datafile.index.max().year + 1, 1, 1)
    ax.set_xlim(datemin, datemax)
    ax.grid(True, axis='x')
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    ax.legend()
    plt.xlabel('Date')
    plt.ylabel('Venta de Sedantes')
    return plt

header1, header2, header3 = st.beta_columns(3)
st.sidebar.title("Opciones para el Modelo")
st.sidebar.write("**Elige un Modelo**")

modelSelected = st.sidebar.selectbox("",("SARIMA","XGBOOST","Prophet"))
st.sidebar.write("**Elige el Data Set**")
dataSelected = st.sidebar.selectbox("",("Sedantes","Pipetas","T4","T4P"))
dataSet = devuelveDataSet(dataSelected)

with header1:
    st.title("")
with header2:
    st.markdown("<h1 style='text-align: center; color: black;'>Time Series</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>Primer app en Stremalit</h3>", unsafe_allow_html=True)
with header3:
    st.title("")

st.write("### Una muestra de los datos para el producto " + dataSelected.lower() + " es:")
st.write("Los primeros 10 registros del data de " + dataSelected.lower() + " son:")
st.write(dataSet.head(10))
st.write("*Como se puede obervar cada fila del data set corresponde a el último día de cada mes*")
st.write("Gráficamente los últimos 30 registros " + dataSelected.lower() + " son:")

st.line_chart(dataSet['Cant'].tail(30))

dataSetTrain = dataSet.loc[:'2018',['Cant']]
dataSetTest = dataSet.loc['2019':, ['Cant']]

if modelSelected == "SARIMA" and dataSelected == "Sedantes":
    model = pkl.load(open('/Users/jclaps/dhds/ds_blend_students_2020/JMC/model_SARIMA.pkl','rb'))
    st.sidebar.write("**Elige la cantidad de periodos a estimar**")
    nPeriods = st.sidebar.slider("",min_value=2,max_value=12)
    dynamic_forecast = model.predict(n_periods=nPeriods)
    forecast = [0 if dynamic_forecast[i] < 0 else dynamic_forecast[i] for i in range(len(dynamic_forecast))]
    plt = devuleveGraph(dataSetTrain,dataSetTest, forecast, nPeriods)
    st.write("***Las predicciones y diagnosticos para " + str(nPeriods) + " períodos con un modelo " + modelSelected + " del producto " + dataSelected.lower() + " serían las siguientes:***")
    graph1, graph2 = st.beta_columns(2)
    with graph1:
        st.pyplot(plt)
    with graph2:
        st.pyplot(model.plot_diagnostics())
else:
    nPeriods = st.sidebar.slider("Periods",min_value=2,max_value=12)
    st.write("## Las predicciones para " + str(nPeriods) + " períodos con un modelo " + modelSelected + " del producto " + dataSelected.lower() + " serían las siguientes:")
    st.image('./meme.jpg')