import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ==========================================
# DATABASE CONNECTION
# ==========================================
conn = sqlite3.connect("database/literacy_analysis.db")
gdp_schooling = pd.read_sql(
    "SELECT * FROM gdp_schooling",
    conn
)
literacy = pd.read_sql("SELECT * FROM literacy_rates", conn)
illiteracy = pd.read_sql("SELECT * FROM illiteracy_population", conn)

# ==========================================
# PAGE TITLE
# ==========================================
st.title("EDA Visualization")
st.header("1. Trend Comparison Between Literate and Illiterate Population")

st.markdown("""
### Objective
Compare how literacy and illiteracy have changed over the years globally and for individual countries.
""")

# ==========================================
# GLOBAL TREND (MATPLOTLIB)
# ==========================================

global_lit = literacy.groupby("Year")["adult_literacy_rate"].mean().reset_index()

global_ill = illiteracy.groupby("year")["illiteracy_rate"].mean().reset_index()

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
    global_lit["Year"],
    global_lit["adult_literacy_rate"],
    marker="o",
    linewidth=2,
    color="green",
    label="Literacy Rate"
)

ax.plot(
    global_ill["year"],
    global_ill["illiteracy_rate"],
    marker="s",
    linewidth=2,
    color="red",
    label="Illiteracy Rate"
)

ax.set_title("Global Literacy vs Illiteracy Trend")
ax.set_xlabel("Year")
ax.set_ylabel("Average Percentage")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# ==========================================
# COUNTRY SELECTION
# ==========================================

st.subheader("Country-wise Trend")

country = st.selectbox(
    "Select Country",
    sorted(literacy["Country"].unique())
)

country_lit = literacy[
    literacy["Country"] == country
]

country_ill = illiteracy[
    illiteracy["entity"] == country
]

# ==========================================
# COUNTRY TREND (SEABORN)
# ==========================================

fig, ax = plt.subplots(figsize=(10,5))

sns.lineplot(
    data=country_lit,
    x="Year",
    y="adult_literacy_rate",
    marker="o",
    linewidth=2,
    label="Literacy",
    ax=ax
)

sns.lineplot(
    data=country_ill,
    x="year",
    y="illiteracy_rate",
    marker="o",
    linewidth=2,
    label="Illiteracy",
    ax=ax
)

ax.set_title(f"{country} Literacy vs Illiteracy")
ax.set_xlabel("Year")
ax.set_ylabel("Percentage")
ax.grid(True)

st.pyplot(fig)

# ==========================================
# PLOTLY INTERACTIVE CHART
# ==========================================

st.subheader("Interactive Literacy Trend")

fig = px.line(
    country_lit,
    x="Year",
    y="adult_literacy_rate",
    markers=True,
    title=f"{country} Adult Literacy Trend"
)

st.plotly_chart(fig, use_container_width=True)
# ==========================================
# VISUALIZATION 2
# Adult vs Youth Literacy Gap
# ==========================================

st.header("2. Adult vs Youth Literacy Gap")

st.markdown("""
Compare adult literacy with youth literacy to identify
generational improvements in education.
""")

# Country Selection
country = st.selectbox(
    "Select Country",
    sorted(literacy["Country"].unique()),
    key="adult_youth"
)

df = literacy[literacy["Country"] == country]

# ==========================================
# MATPLOTLIB LINE CHART
# ==========================================

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
    df["Year"],
    df["adult_literacy_rate"],
    marker="o",
    linewidth=2,
    label="Adult Literacy"
)

ax.plot(
    df["Year"],
    df["youth_literacy_male"],
    marker="s",
    linewidth=2,
    label="Youth Male"
)

ax.plot(
    df["Year"],
    df["youth_literacy_female"],
    marker="^",
    linewidth=2,
    label="Youth Female"
)

ax.set_title(f"Adult vs Youth Literacy - {country}")
ax.set_xlabel("Year")
ax.set_ylabel("Literacy Rate (%)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ==========================================
# SEABORN BAR CHART
# ==========================================

st.subheader("Latest Year Comparison")

latest = df[df["Year"] == df["Year"].max()]

compare = pd.DataFrame({
    "Category": [
        "Adult",
        "Youth Male",
        "Youth Female"
    ],
    "Rate": [
        latest["adult_literacy_rate"].iloc[0],
        latest["youth_literacy_male"].iloc[0],
        latest["youth_literacy_female"].iloc[0]
    ]
})

fig, ax = plt.subplots(figsize=(7,4))

sns.barplot(
    data=compare,
    x="Category",
    y="Rate",
    ax=ax
)

ax.set_title(f"{country} Literacy Comparison")

st.pyplot(fig)

# ==========================================
# PLOTLY INTERACTIVE CHART
# ==========================================

st.subheader("Interactive Comparison")

plot_df = df[[
    "Year",
    "adult_literacy_rate",
    "youth_literacy_male",
    "youth_literacy_female"
]]

plot_df = plot_df.melt(
    id_vars="Year",
    var_name="Category",
    value_name="Literacy Rate"
)

fig = px.line(
    plot_df,
    x="Year",
    y="Literacy Rate",
    color="Category",
    markers=True,
    title=f"{country} Adult vs Youth Literacy"
)

st.plotly_chart(fig, use_container_width=True)
# ============================================================
# VISUALIZATION 3 : Gender Disparities in Literacy
# ============================================================

st.header("3. Gender Disparities in Literacy")

st.markdown("### Compare Male vs Female Youth Literacy")

country = st.selectbox(
    "Select Country",
    sorted(literacy["Country"].unique()),
    key="gender_country"
)

gender_df = literacy[literacy["Country"] == country]

# -----------------------------
# Matplotlib
# -----------------------------
st.subheader("Matplotlib")

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
    gender_df["Year"],
    gender_df["youth_literacy_male"],
    marker="o",
    linewidth=2,
    label="Male"
)

ax.plot(
    gender_df["Year"],
    gender_df["youth_literacy_female"],
    marker="o",
    linewidth=2,
    label="Female"
)

ax.set_title(f"Youth Literacy Gender Gap - {country}")
ax.set_xlabel("Year")
ax.set_ylabel("Literacy Rate (%)")
ax.legend()

st.pyplot(fig)

# -----------------------------
# Seaborn
# -----------------------------
st.subheader("Seaborn")

fig, ax = plt.subplots(figsize=(10,5))

sns.lineplot(
    data=gender_df,
    x="Year",
    y="youth_literacy_male",
    marker="o",
    label="Male",
    ax=ax
)

sns.lineplot(
    data=gender_df,
    x="Year",
    y="youth_literacy_female",
    marker="o",
    label="Female",
    ax=ax
)

ax.set_title("Male vs Female Youth Literacy")

st.pyplot(fig)

# -----------------------------
# Plotly
# -----------------------------
st.subheader("Plotly")

plot_df = gender_df.melt(
    id_vars="Year",
    value_vars=[
        "youth_literacy_male",
        "youth_literacy_female"
    ],
    var_name="Gender",
    value_name="Literacy Rate"
)

fig = px.line(
    plot_df,
    x="Year",
    y="Literacy Rate",
    color="Gender",
    markers=True,
    title=f"Youth Literacy Gender Gap - {country}"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Gender Gap Table
# -----------------------------
st.subheader("Gender Gap Table")

gap_df = gender_df.copy()

gap_df["Gender Gap"] = (
    gap_df["youth_literacy_male"]
    - gap_df["youth_literacy_female"]
).abs()

st.dataframe(
    gap_df[
        [
            "Year",
            "youth_literacy_male",
            "youth_literacy_female",
            "Gender Gap"
        ]
    ]
)

# -----------------------------
# Region-wise Average Gender Gap
# -----------------------------
st.subheader("Region-wise Average Gender Gap")

region_gap = literacy.copy()

region_gap["Gender Gap"] = (
    region_gap["youth_literacy_male"]
    - region_gap["youth_literacy_female"]
).abs()

region_gap = (
    region_gap.groupby("Region")["Gender Gap"]
    .mean()
    .reset_index()
)

fig = px.bar(
    region_gap,
    x="Region",
    y="Gender Gap",
    color="Gender Gap",
    title="Average Gender Gap by Region"
)

st.plotly_chart(fig, use_container_width=True)
# ============================================================
# VISUALIZATION 4 : Link Between Literacy and Economic Indicators
# ============================================================

st.header("4. Link Between Literacy and Economic Indicators")

# Merge literacy and GDP tables
merged = pd.merge(
    literacy,
    gdp_schooling,
    left_on=["Country", "Year"],
    right_on=["Entity", "Year"],
    how="inner"
)

# -----------------------------
# Matplotlib Scatter Plot
# -----------------------------
st.subheader("Matplotlib")

fig, ax = plt.subplots(figsize=(10,6))

ax.scatter(
    merged["GDP per capita"],
    merged["adult_literacy_rate"],
    alpha=0.7
)

ax.set_xlabel("GDP per Capita")
ax.set_ylabel("Adult Literacy Rate (%)")
ax.set_title("Literacy Rate vs GDP per Capita")

st.pyplot(fig)

# -----------------------------
# Seaborn Scatter Plot
# -----------------------------
st.subheader("Seaborn")

fig, ax = plt.subplots(figsize=(10,6))

sns.scatterplot(
    data=merged,
    x="GDP per capita",
    y="adult_literacy_rate",
    hue="Region",
    ax=ax
)

st.pyplot(fig)

# -----------------------------
# Plotly Interactive Scatter
# -----------------------------
st.subheader("Plotly")

fig = px.scatter(
    merged,
    x="GDP per capita",
    y="adult_literacy_rate",
    color="Region",
    hover_name="Country",
    title="GDP per Capita vs Adult Literacy Rate"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Correlation
# -----------------------------
st.subheader("Correlation")

corr = merged[["GDP per capita", "adult_literacy_rate"]].corr()

fig, ax = plt.subplots(figsize=(5,4))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)

# -----------------------------
# Possible Outliers
# -----------------------------
st.subheader("Countries with High Literacy but Low GDP")

outliers = merged[
    (merged["adult_literacy_rate"] > 90) &
    (merged["GDP per capita"] < 5000)
]

st.dataframe(
    outliers[
        ["Country", "Year", "adult_literacy_rate", "GDP per capita"]
    ]
)
# ============================================================
# VISUALIZATION 5 : Schooling Years vs Literacy Levels
# ============================================================

st.header("5. Schooling Years vs Literacy Levels")

# Merge literacy and GDP/Schooling tables
school_df = pd.merge(
    literacy,
    gdp_schooling,
    left_on=["Country", "Year"],
    right_on=["Entity", "Year"],
    how="inner"
)

# --------------------------------------------------
# Matplotlib Scatter Plot
# --------------------------------------------------
st.subheader("Matplotlib")

fig, ax = plt.subplots(figsize=(10,6))

ax.scatter(
    school_df["Average years of schooling"],
    school_df["adult_literacy_rate"],
    alpha=0.7
)

ax.set_xlabel("Average Years of Schooling")
ax.set_ylabel("Adult Literacy Rate (%)")
ax.set_title("Schooling vs Literacy")

st.pyplot(fig)

# --------------------------------------------------
# Seaborn Scatter Plot
# --------------------------------------------------
st.subheader("Seaborn")

fig, ax = plt.subplots(figsize=(10,6))

sns.scatterplot(
    data=school_df,
    x="Average years of schooling",
    y="adult_literacy_rate",
    hue="Region",
    ax=ax
)

st.pyplot(fig)

# --------------------------------------------------
# Plotly Interactive Scatter
# --------------------------------------------------
st.subheader("Plotly")

fig = px.scatter(
    school_df,
    x="Average years of schooling",
    y="adult_literacy_rate",
    color="Region",
    hover_name="Country",
    title="Schooling Years vs Adult Literacy"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Countries with High Schooling but Low Literacy
# --------------------------------------------------
st.subheader("Countries with High Schooling but Low Literacy")

outliers = school_df[
    (school_df["Average years of schooling"] > 10) &
    (school_df["adult_literacy_rate"] < 80)
]

st.dataframe(
    outliers[
        [
            "Country",
            "Year",
            "Average years of schooling",
            "adult_literacy_rate"
        ]
    ]
)
# ============================================================
# 6. TOP & BOTTOM PERFORMERS RANKING
# ============================================================

st.header("6. Top & Bottom Performers Ranking")

# Merge literacy and illiteracy tables
ranking_df = literacy.copy()
ranking_df["youth_avg"] = (
    ranking_df["youth_literacy_male"] +
    ranking_df["youth_literacy_female"]
) / 2

latest_year = ranking_df["Year"].max()

latest = ranking_df[ranking_df["Year"] == latest_year]

# Average Youth Literacy
ranking_df["youth_avg"] = (
    ranking_df["youth_literacy_male"] +
    ranking_df["youth_literacy_female"]
) / 2

# Select latest year
latest_year = ranking_df["Year"].max()

latest = ranking_df[ranking_df["Year"] == latest_year]

# ---------------------------------------------------------
# Top 10 Adult Literacy
# ---------------------------------------------------------
st.subheader("Top 10 Countries - Adult Literacy")

top10 = latest.sort_values(
    "adult_literacy_rate",
    ascending=False
).head(10)

fig, ax = plt.subplots(figsize=(10,6))

sns.barplot(
    data=top10,
    x="adult_literacy_rate",
    y="Country",
    palette="Greens_r",
    ax=ax
)

st.pyplot(fig)

# ---------------------------------------------------------
# Bottom 10 Adult Literacy
# ---------------------------------------------------------
st.subheader("Bottom 10 Countries - Adult Literacy")

bottom10 = latest.sort_values(
    "adult_literacy_rate"
).head(10)

fig, ax = plt.subplots(figsize=(10,6))

sns.barplot(
    data=bottom10,
    x="adult_literacy_rate",
    y="Country",
    palette="Reds",
    ax=ax
)

st.pyplot(fig)

# ---------------------------------------------------------
# Top 10 Youth Literacy
# ---------------------------------------------------------
st.subheader("Top 10 Countries - Youth Literacy")

top_youth = latest.sort_values(
    "youth_avg",
    ascending=False
).head(10)

fig = px.bar(
    top_youth,
    x="Country",
    y="youth_avg",
    color="youth_avg",
    title="Top Youth Literacy Countries"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# Top 10 Illiteracy
# ---------------------------------------------------------
st.subheader("Top 10 Countries - Illiteracy")

top_ill = latest.sort_values(
    "illiteracy_rate",
    ascending=False
).head(10)

fig = px.bar(
    top_ill,
    x="Country",
    y="illiteracy_rate",
    color="illiteracy_rate",
    title="Highest Illiteracy Countries"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# Heatmap
# ---------------------------------------------------------
st.subheader("Heatmap of Literacy Indicators")

heat = latest[
    [
        "Country",
        "adult_literacy_rate",
        "youth_avg",
        "illiteracy_rate"
    ]
].set_index("Country").head(20)

fig, ax = plt.subplots(figsize=(12,8))

sns.heatmap(
    heat,
    cmap="YlGnBu",
    annot=True,
    fmt=".1f",
    ax=ax
)

st.pyplot(fig)
# ============================================================
# 7. CONTINENTAL AND REGIONAL PATTERNS
# ============================================================

st.header("7. Continental and Regional Patterns")

# Average Literacy by Region
st.subheader("Average Adult Literacy Rate by Region")

region_avg = literacy.groupby("Region")["adult_literacy_rate"].mean().reset_index()

fig, ax = plt.subplots(figsize=(10,6))

sns.barplot(
    data=region_avg,
    x="Region",
    y="adult_literacy_rate",
    palette="viridis",
    ax=ax
)

plt.xticks(rotation=45)
plt.xlabel("Region")
plt.ylabel("Average Adult Literacy Rate")
plt.title("Average Adult Literacy Rate by Region")

st.pyplot(fig)


# Average Illiteracy by Region
st.subheader("Average Illiteracy Rate by Region")

region_ill = literacy.groupby("Region")["illiteracy_rate"].mean().reset_index()

fig, ax = plt.subplots(figsize=(10,6))

sns.barplot(
    data=region_ill,
    x="Region",
    y="illiteracy_rate",
    palette="Reds",
    ax=ax
)

plt.xticks(rotation=45)
plt.xlabel("Region")
plt.ylabel("Average Illiteracy Rate")
plt.title("Average Illiteracy Rate by Region")

st.pyplot(fig)


# Heatmap
st.subheader("Regional Literacy Heatmap")

heat = literacy.groupby("Region")[[
    "adult_literacy_rate",
    "illiteracy_rate",
    "gdp_per_capita",
    "avg_years_schooling"
]].mean()

fig, ax = plt.subplots(figsize=(10,6))

sns.heatmap(
    heat,
    annot=True,
    cmap="YlGnBu",
    fmt=".1f",
    ax=ax
)

plt.title("Regional Comparison")

st.pyplot(fig)
# ============================================================
# 8. ILLITERACY AND POPULATION SIZE
# ============================================================

st.header("8. Illiteracy and Population Size")

# ------------------------------------------------------------
# A. Top Countries with Highest Illiteracy Rate
# ------------------------------------------------------------

st.subheader("A. Countries with Highest Illiteracy Rate")

latest_year = literacy["Year"].max()

top10 = literacy[literacy["Year"] == latest_year] \
    .sort_values("illiteracy_rate", ascending=False) \
    .head(10)

fig, ax = plt.subplots(figsize=(10,6))

sns.barplot(
    data=top10,
    x="illiteracy_rate",
    y="Country",
    palette="Reds_r",
    ax=ax
)

ax.set_xlabel("Illiteracy Rate (%)")
ax.set_ylabel("Country")
ax.set_title(f"Top 10 Countries with Highest Illiteracy Rate ({latest_year})")

st.pyplot(fig)

# ------------------------------------------------------------
# B. Small Percentage but High Illiteracy
# ------------------------------------------------------------

st.subheader("B. Literacy Rate vs Illiteracy Rate")

fig, ax = plt.subplots(figsize=(8,6))

sns.scatterplot(
    data=literacy,
    x="literacy_rate",
    y="illiteracy_rate",
    hue="Region",
    s=80,
    ax=ax
)

ax.set_xlabel("Literacy Rate (%)")
ax.set_ylabel("Illiteracy Rate (%)")
ax.set_title("Literacy Rate vs Illiteracy Rate")

st.pyplot(fig)
# ============================================================
# 9. LONG-TERM LITERACY PROJECTIONS
# ============================================================

from sklearn.linear_model import LinearRegression
import numpy as np

st.header("9. Long-term Literacy Projections")

country = st.selectbox(
    "Select Country for Projection",
    sorted(literacy["Country"].unique()),
    key="projection_country"
)

df = literacy[literacy["Country"] == country].copy()

df = df.sort_values("Year")

X = df[["Year"]]
y = df["adult_literacy_rate"]

model = LinearRegression()
model.fit(X, y)

future_years = np.arange(df["Year"].max() + 1,
                         df["Year"].max() + 11)

future_df = pd.DataFrame({"Year": future_years})

future_df["Predicted Literacy Rate"] = model.predict(future_df)

fig, ax = plt.subplots(figsize=(10,6))

# Actual data
ax.plot(
    df["Year"],
    df["adult_literacy_rate"],
    marker="o",
    linewidth=2,
    label="Actual"
)

# Prediction
ax.plot(
    future_df["Year"],
    future_df["Predicted Literacy Rate"],
    marker="o",
    linestyle="--",
    linewidth=2,
    color="red",
    label="Predicted"
)

ax.set_xlabel("Year")
ax.set_ylabel("Adult Literacy Rate")
ax.set_title(f"{country} Literacy Projection")
ax.legend()

st.pyplot(fig)

st.dataframe(future_df)
# ============================================================
# 10. IMPACT OF CONFLICT OR CRISES ON LITERACY
# ============================================================

st.header("10. Impact of Conflict or Crises on Literacy")

st.write(
    "Select a country and observe whether literacy growth slowed or declined during certain periods."
)

country = st.selectbox(
    "Select Country",
    sorted(literacy["Country"].unique()),
    key="conflict_country"
)

df = literacy[literacy["Country"] == country].sort_values("Year")

fig, ax = plt.subplots(figsize=(10,6))

sns.lineplot(
    data=df,
    x="Year",
    y="adult_literacy_rate",
    marker="o",
    linewidth=2,
    color="blue",
    ax=ax
)

ax.set_title(f"Adult Literacy Trend - {country}")
ax.set_xlabel("Year")
ax.set_ylabel("Adult Literacy Rate (%)")

st.pyplot(fig)

# Growth analysis
df = df.copy()
df["Growth"] = df["adult_literacy_rate"].diff()

st.subheader("Year-wise Literacy Growth")

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    data=df,
    x="Year",
    y="Growth",
    palette="viridis",
    ax=ax
)

ax.axhline(0, color="red", linestyle="--")
ax.set_ylabel("Growth Rate")
ax.set_title("Annual Literacy Growth")

st.pyplot(fig)

st.dataframe(df[["Year", "adult_literacy_rate", "Growth"]])


# ==========================================
# CLOSE DATABASE
# ==========================================

conn.close()