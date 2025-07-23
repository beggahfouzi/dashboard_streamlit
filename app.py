import streamlit as st
import plotly.express as px
import pandas as pd


co2_df = pd.read_csv("./data/CO2_per_capita.csv", sep=";")
co2_df.dropna(inplace=True)

def top_n_emitters(df, start_year=2008, end_year=2011, nb_displayed=10):
    
    #years filter
    df = df[(df["Year"] >= start_year) & (df["Year"]<= end_year)]
   
    #do the mean for each country
    df =df.groupby("Country Name", as_index=False)["CO2 Per Capita (metric tons)"].mean()
   
    #sort the values and keep nb_displayed
    df = df.sort_values("CO2 Per Capita (metric tons)", ascending=False).head(nb_displayed)
    #create the fig
    fig = px.bar(df, x="Country Name", y="CO2 Per Capita (metric tons)", 
                 title=f"Top {nb_displayed} Emitters ({start_year}-{end_year})",
                 labels={"CO2 Per Capita (metric tons)": "CO2 Per Capita (metric tons)"})
    #return the fig
    return fig



st.title("CO2 Emissions Dashboard")


start_year, end_year = st.slider( "Select Year Range", min_value=int(co2_df["Year"].min()),  max_value=int(co2_df["Year"].max()), value=(2008, 2011))

nb_displayed = st.selectbox( "# of countries displayed", [3, 5, 10, 20, 30])


fig = top_n_emitters(co2_df, start_year, end_year, nb_displayed)
st.plotly_chart(fig)

fig = px.scatter_geo(co2_df, locations= "Country Code", size="CO2 Per Capita (metric tons)", animation_frame="Year")
st.plotly_chart(fig)
