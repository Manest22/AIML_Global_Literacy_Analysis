# 📚 Global Literacy Analysis using SQL & Streamlit

## 📖 Project Overview

This project analyzes global literacy, illiteracy, education, and economic indicators using Python, SQL, and Streamlit. The objective is to clean real-world datasets, store them in a SQLite database, perform SQL queries, and build an interactive Streamlit dashboard with multiple visualizations.

The application helps users explore literacy trends across countries, compare education indicators, analyze gender gaps, and understand the relationship between literacy and economic development.

---

# 🎯 Objectives

- Clean and preprocess literacy datasets.
- Store cleaned data in SQLite database.
- Perform SQL queries for data analysis.
- Build interactive Streamlit dashboard.
- Visualize literacy trends using charts.
- Analyze country-wise education statistics.

---

# 📂 Project Structure

copy


Literacy_Analysis_App/
│
├── database/
│   └── literacy_analysis.db
│
├── pages/
│   ├── 1_SQL_Query_Executor.py
│   ├── 2_EDA_Visualizations.py
│   └── 3_Country_Profile.py
│
├── data/
│   ├── literacy_rates.csv
│   ├── illiteracy_population.csv
│   └── education_indicators.csv
│
├── Home.py
├── requirements.txt
└── README.md
---

# 🛠 Technologies Used

- Python
- Pandas
- NumPy
- SQLite
- Streamlit
- Matplotlib
- Seaborn
- Plotly
- SQL

---

# 📊 Features

### SQL Query Executor

- Execute custom SQL queries
- Display query results
- Download query results as CSV
- Automatic chart generation

---

### EDA Visualizations

The dashboard contains:

1. Trend Comparison between Literacy & Illiteracy
2. Adult vs Youth Literacy Gap
3. Gender Disparity in Literacy
4. Literacy vs GDP Per Capita
5. Schooling Years vs Literacy
6. Top & Bottom Performing Countries
7. Regional Literacy Analysis
8. Illiteracy Population Analysis
9. Literacy Growth Projection
10. Impact of Conflict on Literacy

---

### Country Profile

Users can:

- Select any country
- View literacy indicators
- View GDP
- View schooling years
- Compare literacy trends over time

---

# 🗄 Database Tables

The SQLite database contains three tables:

- literacy_rates
- illiteracy_population
- education_indicators

---

# 📈 Visualizations Used

- Line Chart
- Bar Chart
- Scatter Plot
- Heatmap
- Box Plot
- Histogram
- Area Chart

---

# 📦 Project Deliverables

- Three cleaned datasets
- SQLite database
- SQL scripts
- Streamlit application
- EDA Visualizations
- Jupyter Notebook
- Project Report

---

# 🚀 Installation

Install dependencies

Bash


pip install -r requirements.txt
Run Streamlit

Bash


streamlit run Home.py
---

# 📊 Key Insights

- Global literacy has improved significantly over the years.
- Youth literacy is generally higher than adult literacy.
- Female literacy has improved but gender gaps still exist in some regions.
- Countries with higher GDP per capita generally show higher literacy rates.
- More years of schooling are associated with higher literacy.
- Regional differences highlight unequal access to education.
- Literacy projections indicate continued global improvement.

---

# 👨‍💻 Developed By

Mani Bharathi

B.E. Computer Science & Engineering

GUVI – HCL Data Science Project

Global Literacy Analysis using SQL & Streamlit

---