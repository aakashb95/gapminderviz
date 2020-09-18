import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


def choice_wise(df, choice):
    # st.sidebar.title(f"{choice} wise yearly trend of feature")

    cr = st.sidebar.selectbox(f"Select {choice}", ['All',*df[choice].unique()])
    col_list =  ['population','fertility', 'life', 'child_mortality',
        'gdp']
    column = st.sidebar.selectbox("Select Features",col_list)

    if cr!='All':
        fig = px.line(df[df[choice]==cr], x = 'Year', y = column, color = 'Country')
    else :
        fig = px.line(df, x = 'Year', y = column, color = choice)


    st.title(f'{choice.capitalize()} - {column.capitalize()} vs Year')
    st.plotly_chart(fig)


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

if __name__ == "__main__":
    
    @st.cache
    def load_data():
        df = pd.read_csv('gapminder_tidy.csv')
        return df

    df = load_data()
    st.sidebar.title('Select Country/Region')
    choice = st.sidebar.selectbox('',['Country','region'])
    st.sidebar.title(f"{choice.capitalize()} wise yearly trend of feature")
    choice_wise(df, choice)
        
    population_pie(df)
    gdp_life(df)