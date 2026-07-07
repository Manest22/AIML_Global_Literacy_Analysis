CREATE TABLE literacy_rates (
    Country TEXT,
    Country_Code TEXT,
    Year INTEGER,
    adult_literacy_rate REAL,
    youth_literacy_male REAL,
    youth_literacy_female REAL,
    Region TEXT,
    illiteracy_rate REAL,
    literacy_rate REAL,
    gdp_per_capita REAL,
    world_region TEXT,
    avg_years_schooling REAL,
    Illiteracy_Percentage REAL,
    Literacy_Gender_Gap REAL,
    GDP_per_Schooling_Year REAL,
    Education_Index REAL,
    Youth_Literacy_Average REAL,
    Literacy_Growth_Rate REAL
);

CREATE TABLE illiteracy_population (
    entity TEXT,
    code TEXT,
    year INTEGER,
    illiteracy_rate REAL,
    literacy_rate REAL
);