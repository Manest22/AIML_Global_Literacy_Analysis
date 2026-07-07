import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px

st.title("🌍 Country Profile")

# Database Connection
conn = sqlite3.connect("database/literacy_analysis.db")

literacy = pd.read_sql("SELECT * FROM literacy_rates", conn)

# -------------------------------
# Select Country
# -------------------------------
country = st.selectbox(
    "Select Country",
    sorted(literacy["Country"].unique())
)

country_df = literacy[literacy["Country"] == country]

# -------------------------------
# Select Year
# -------------------------------
year = st.selectbox(
    "Select Year",
    sorted(country_df["Year"].unique())
)

profile = country_df[country_df["Year"] == year]

st.subheader(f"{country} - {year}")

st.dataframe(profile)

# -------------------------------
# Key Metrics
# -------------------------------
st.subheader("Key Indicators")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Adult Literacy",
    f"{profile.iloc[0]['adult_literacy_rate']:.2f}%"
)

col2.metric(
    "GDP per Capita",
    f"{profile.iloc[0]['gdp_per_capita']:.2f}"
)

col3.metric(
    "Avg Schooling",
    f"{profile.iloc[0]['avg_years_schooling']:.2f}"
)

# -------------------------------
# Literacy Trend
# -------------------------------
st.subheader("Adult Literacy Trend")

fig = px.line(
    country_df,
    x="Year",
    y="adult_literacy_rate",
    markers=True,
    title=f"{country} Adult Literacy Trend"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# GDP Trend
# -------------------------------
st.subheader("GDP per Capita Trend")

fig = px.line(
    country_df,
    x="Year",
    y="gdp_per_capita",
    markers=True,
    title=f"{country} GDP Trend"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Schooling Trend
# -------------------------------
st.subheader("Average Schooling Trend")

fig = px.bar(
    country_df,
    x="Year",
    y="avg_years_schooling",
    title=f"{country} Average Schooling"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Youth Literacy
# -------------------------------
st.subheader("Youth Literacy")

fig, ax = plt.subplots(figsize=(8,5))

ax.plot(
    country_df["Year"],
    country_df["youth_literacy_male"],
    marker="o",
    label="Male"
)

ax.plot(
    country_df["Year"],
    country_df["youth_literacy_female"],
    marker="o",
    label="Female"
)

ax.set_xlabel("Year")
ax.set_ylabel("Literacy Rate")
ax.legend()

st.pyplot(fig)
