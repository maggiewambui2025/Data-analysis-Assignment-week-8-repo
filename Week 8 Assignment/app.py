# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_option('deprecation.showPyplotGlobalUse', False)

# Title and description
st.title("CORD-19 Data Explorer")
st.write("A simple Streamlit app for exploring COVID-19 research metadata.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('metadata.csv')
    df = df.dropna(subset=['title', 'publish_time'])
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    return df

df = load_data()

# Sidebar filter
year_range = st.slider("Filter by year", 2019, 2023, (2020, 2021))
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Show filtered data
st.subheader("Sample Data")
st.dataframe(filtered_df[['title', 'authors', 'journal', 'year']].head())

# Publications by year
st.subheader("Publications Over Time")
pubs_by_year = filtered_df['year'].value_counts().sort_index()
st.bar_chart(pubs_by_year)

# Top journals
st.subheader("Top Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
st.bar_chart(top_journals)

# Word Cloud
st.subheader("Word Cloud of Titles")
titles = ' '.join(filtered_df['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titles)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot()
