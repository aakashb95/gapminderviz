import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

def population_pie(df):
    #PIE
    st.sidebar.title('Year wise population')
    st.sidebar.header('Pie Chart')
    year = st.sidebar.selectbox("Select Year",df.Year.unique(), key = 'pie')
    region = st.sidebar.selectbox("Select Region",['All', *df.region.unique()],key = 'pie')

    if region != 'All':
        st.title(f'Population distribution of {region} in {year}')
        pie = px.pie(df[(df['Year']==year) & (df['region']==region)] , values='population', names='Country')
        pie.update_traces(textposition='inside', textfont_size=14)
    else:
        st.title(f'Population distribution of the World in {year}')
        pie = px.pie(df[(df['Year']==year)] , values='population', names='Country')
        pie.update_traces(textposition='inside', textfont_size=14)


    st.plotly_chart(pie)

def gdp_life(df):
    # GDP vs Life Expectancy by Region
    st.sidebar.title('GDP per capita and Life Expectancy by Region and Year')
    st.sidebar.header('Scatter Plot')
    
    gdp_year = st.sidebar.selectbox("Select Year ",df.Year.unique(), key = 'gdp')
    gdp_region = st.sidebar.selectbox("Select Region",df.region.unique(), key = 'gdp')

    gy_df = df[(df['Year']==gdp_year) & (df['region']==gdp_region)]
    # gr_df = df[df['region']==gdp_region]

    gdp_le = px.scatter(gy_df, x="gdp", y="life", text="Country", log_x=True, size_max=60)
    gdp_le.update_traces(textposition='top center')

    st.title(f'GDP per capita and Life Expectancy in {gdp_region} in {gdp_year}')
    st.plotly_chart(gdp_le)
    
def study_country(country):    
    global df
    cdf = df[df['Country']==country]

    fig = make_subplots(rows=3, cols=2)

    le = px.line(cdf, x = 'Year', y = 'life')

    gdp = px.line(cdf, x = 'Year', y = 'gdp')

    pop = px.line(cdf, x = 'Year', y = 'population')

    cm = px.line(cdf, x = 'Year', y = 'child_mortality')

    fertility = px.line(cdf, x = 'Year', y = 'fertility')

    fig.add_trace(le.data[0], row = 1, col = 1)
    fig.add_trace(gdp.data[0], row = 1, col = 2)
    fig.add_trace(pop.data[0], row = 2, col = 1)
    fig.add_trace(cm.data[0], row = 2, col = 2)
    fig.add_trace(fertility.data[0], row = 3, col = 1)

    fig.update_xaxes(title_text="Year", row=1, col=1)
    fig.update_xaxes(title_text="Year",  row=1, col=2)
    fig.update_xaxes(title_text="Year", row=2, col=1)
    fig.update_xaxes(title_text="Year",  row=2, col=2)
    fig.update_xaxes(title_text="Year",  row=3, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="Life Expectancy", row=1, col=1)
    fig.update_yaxes(title_text="GDP Per Capita",  row=1, col=2)
    fig.update_yaxes(title_text="Population",  row=2, col=1)
    fig.update_yaxes(title_text="Child Mortality", row=2, col=2)
    fig.update_yaxes(title_text="Fertility", row=3, col=1)

    fig.update_layout(title_text=f"Studying {country}", height=700, width = 850)
    st.plotly_chart(fig)

if __name__ == "__main__":
    
    @st.cache
    def load_data():
        df = pd.read_csv('gapminder_tidy.csv')
        return df

    df = load_data()
    
    st.sidebar.title(f"Trends of all features for Country of your choice")
    country_choice = st.sidebar.selectbox('Select Country',df.Country.unique())
    
    study_country(country_choice)
        
    population_pie(df)
    gdp_life(df)