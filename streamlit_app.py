import pandas as pd
import plotly.express as px
import streamlit as st

# Verileri CSV dosyasından yükle

url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(url)

# Ülkeler listesi
countries = df['location'].unique()

# Streamlit uygulamasını oluştur
st.title("Dünya Çapında COVID-19 Vakaları Haritası ve Ülke Verileri")

# Vaka Sayısı Tipi Dropdown
case_type = st.selectbox(
    "Vaka Sayısı Tipi:",
    ['total_cases', 'total_deaths', 'total_recovered'],
    index=0
)

# Ülkeleri Seçin Dropdown
selected_countries = st.multiselect(
    "Ülkeleri Seçin:",
    countries,
    default=['Turkey', 'Germany']
)

# Dünya Haritası
fig_map = px.choropleth(
    df[df['location'].isin(selected_countries)],
    locations='iso_code',
    color=case_type,
    hover_name='location',
    animation_frame='date',
    projection='natural earth',
    color_continuous_scale='Viridis',
    title=f"Dünya Genelinde COVID-19 {case_type.capitalize()} Haritası"
)

st.plotly_chart(fig_map)

# Daire Dilimli Grafik
filtered_df = df[df['location'].isin(selected_countries)]
total_values = filtered_df.groupby('location')[case_type].max().reset_index()

fig_pie = px.pie(
    total_values,
    values=case_type,
    names='location',
    title=f"{', '.join(selected_countries)} Ülkelerinde COVID-19 {case_type.capitalize()} Dağılımı",
    labels={'location': 'Ülke'}
)

st.plotly_chart(fig_pie)

