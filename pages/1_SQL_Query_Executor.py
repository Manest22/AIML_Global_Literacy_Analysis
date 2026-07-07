import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="SQL Query Executor",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ SQL Query Executor")
st.write("Execute predefined SQL queries on the Literacy Analysis Database.")

# -------------------------------------------------------
# Database Connection
# -------------------------------------------------------

DB_PATH = "database/literacy_analysis.db"

conn = sqlite3.connect(DB_PATH)

# -------------------------------------------------------
# Query Categories
# -------------------------------------------------------

category = st.sidebar.selectbox(
    "Select Category",
    [
        "Literacy Rates",
        "Illiteracy Population",
        "GDP & Schooling",
        "JOIN Queries"
    ],
    key="category"
)

# -------------------------------------------------------
# Literacy Queries
# -------------------------------------------------------

literacy_queries = {

"Top 5 Adult Literacy (2020)": """
SELECT Country,
adult_literacy_rate
FROM literacy_rates
WHERE Year=2020
ORDER BY adult_literacy_rate DESC
LIMIT 5;
""",

"Female Youth Literacy <80%": """
SELECT Country,
youth_literacy_female
FROM literacy_rates
WHERE youth_literacy_female<80
ORDER BY youth_literacy_female;
""",

"Average Adult Literacy by Region": """
SELECT Region,
AVG(adult_literacy_rate) AS Average_Literacy
FROM literacy_rates
GROUP BY Region
ORDER BY Average_Literacy DESC;
""",

}
# -------------------------------------------------------
# Illiteracy Population Queries
# -------------------------------------------------------

illiteracy_queries = {

"Countries with Illiteracy >20% (2000)": """
SELECT entity,
year,
illiteracy_rate
FROM illiteracy_population
WHERE Year=2000
AND illiteracy_rate>20
ORDER BY illiteracy_rate DESC;
""",

"India Illiteracy Trend": """
SELECT year,
illiteracy_rate
FROM illiteracy_population
WHERE entity='India' AND year BETWEEN 2000 AND 2020
ORDER BY Year ASC;
""",

"Top 10 Illiterate Population": """
SELECT entity,
illiteracy_rate
FROM illiteracy_population
ORDER BY illiteracy_rate DESC
LIMIT 10;
""",

}

# -------------------------------------------------------
# GDP & Schooling Queries
# -------------------------------------------------------

gdp_queries = {

"Countries with Schooling >7 and GDP <5000": """
SELECT Entity,
Year,
"Average years of schooling",
"GDP per capita"
FROM gdp_schooling
WHERE "Average years of schooling" > 7
AND "GDP per capita" < 5000
ORDER BY "GDP per capita";
""",

"GDP Ranking (2020)": """
SELECT
    Entity,
    "GDP per capita",
    "Average years of schooling"
FROM gdp_schooling
WHERE Year = 2020
ORDER BY "GDP per capita" DESC;
""",

"Average Schooling Per Year": """
SELECT
    Year,
    ROUND(AVG("Average years of schooling"),2) AS Avg_Schooling
FROM gdp_schooling
GROUP BY Year
ORDER BY Year;
"""

}

# -------------------------------------------------------
# JOIN Queries
# -------------------------------------------------------

join_queries = {

   "High GDP Low Schooling": """
SELECT
    Entity,
    Year,
    "GDP per capita",
    "Average years of schooling"
FROM gdp_schooling
WHERE Year = 2020
AND "Average years of schooling" < 6
ORDER BY "GDP per capita" DESC
LIMIT 10;
""",

    "High Illiteracy Despite Schooling": """
SELECT
    i.Entity,
    i.Year,
    i.illiteracy_rate,
    g."Average years of schooling"
FROM illiteracy_population i
INNER JOIN gdp_schooling g
ON i.Entity = g.Entity
AND i.Year = g.Year
WHERE g."Average years of schooling" > 10
AND i.illiteracy_rate0
ORDER BY i.illiteracy_rate DESC;
""",

    "India Literacyvs GDP Trend": """
SELECT
    l.Year,
    l.adult_literacy_rate,
    g."GDP per capita"
FROM literacy_rates l
INNER JOIN gdp_schooling g
ON l.Country = g.Entity
AND l.Year = g.Year
WHERE l.Country = 'India'
AND l.Year BETWEEN 2000 AND 2020
ORDER BY l.Year;
""",

    "Youth Literacy Gender Gap": """
SELECT
    l.Country,
    l.Year,
    l.youth_literacy_male,
    l.youth_literacy_female,
    ROUND(
        l.youth_literacy_male - l.youth_literacy_female,
        2
    ) AS Gender_Gap,
    g."GDP per capita"
FROM literacy_rates l
INNER JOIN gdp_schooling g
ON l.Country = g.Entity
AND l.Year = g.Year
WHERE l.Year = 2020
AND g."GDP per capita" > 30000
ORDER BY Gender_Gap DESC;
"""


}
# -------------------------------------------------------
# Select Query Dictionary
# -------------------------------------------------------

if category == "Literacy Rates":
    queries = literacy_queries

elif category == "Illiteracy Population":
    queries = illiteracy_queries

elif category == "GDP & Schooling":
    queries = gdp_queries

else:
    queries = join_queries


# -------------------------------------------------------
# Query Selection
# -------------------------------------------------------

selected_query = st.selectbox(
    "Select SQL Query",
    list(queries.keys()),
    key="query_select"
)

# -------------------------------------------------------
# SQL Editor
# -------------------------------------------------------

sql = st.text_area(
    "SQL Statement",
    value=queries[selected_query],
    height=220,
    key=f"sql_{selected_query}"
)

# -------------------------------------------------------
# Run Query
# -------------------------------------------------------

run = st.button(
    "▶ Run Query",
    key="run_query"
)

# -------------------------------------------------------
# Execute SQL
# -------------------------------------------------------

if run:

    try:

        df = pd.read_sql_query(sql, conn)

        st.success(f"{len(df)} records found")

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download CSV",
            csv,
            "query_result.csv",
            "text/csv",
            key="download_csv"
        )

        numeric = df.select_dtypes(include="number").columns

        if len(numeric) > 0:

            x = st.selectbox(
                "X Axis",
                df.columns,
                key="x_axis"
            )

            y = st.selectbox(
                "Y Axis",
                numeric,
                key="y_axis"
            )

            chart = st.selectbox(
                "Chart Type",
                [
                    "Bar",
                    "Line",
                    "Scatter"
                ],
                key="chart_type"
            )
# -------------------------------------------------------
# Plot Chart
# -------------------------------------------------------

            if chart == "Bar":
                fig = px.bar(
                    df,
                    x=x,
                    y=y,
                    title=f"{y} by {x}"
                )

            elif chart == "Line":
                fig = px.line(
                    df,
                    x=x,
                    y=y,
                    markers=True,
                    title=f"{y} by {x}"
                )

            else:
                fig = px.scatter(
                    df,
                    x=x,
                    y=y,
                    title=f"{y} vs {x}"
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    except Exception as e:
        st.error(e)

# -------------------------------------------------------


# -------------------------------------------------------
# Close Database
# -------------------------------------------------------

conn.close()
