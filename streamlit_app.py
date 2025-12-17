import streamlit as st
import pandas as pd
import math
import altair as alt
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

gdp_df = get_gdp_data()

@st.cache_data
def get_employment():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/CES0000000001.csv'
    employment_df = pd.read_csv(DATA_FILENAME)
    employment_df['month'] = employment_df['year'].astype('str') + ' ' + employment_df['period']
    employment_df['Employment in Thousands'] = employment_df['value']

    return employment_df

employment_df = get_employment()

@st.cache_data
def get_cpi():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/CUUR0000SA0.csv'
    cpi_df = pd.read_csv(DATA_FILENAME)
    cpi_df['month'] = cpi_df['year'].astype('str') + ' ' + cpi_df['period']

    return cpi_df

cpi_df = get_cpi()

@st.cache_data
def get_unemployment():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/LNS14000000.csv'
    unemployment_df = pd.read_csv(DATA_FILENAME)
    unemployment_df['month'] = unemployment_df['year'].astype('str') + ' ' + unemployment_df['period']
    unemployment_df['Unemployment'] = unemployment_df['value']

    return unemployment_df

unemployment_df = get_unemployment()

@st.cache_data
def get_ppi():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/WPUFD49207.csv'
    ppi_df = pd.read_csv(DATA_FILENAME)
    ppi_df['month'] = ppi_df['year'].astype('str') + ' ' + ppi_df['period']

    return ppi_df

ppi_df = get_ppi()

def get_inflation():
    inflation_df = ppi_df
    inflation_df['cpi'] = cpi_df['value']
    inflation_df['ppi'] = inflation_df['value']
    return inflation_df

inflation_df = get_inflation()

def get_mom_inflation():
    inflation_df = ppi_df
    inflation_df['cpi'] = cpi_df['value']
    inflation_df['ppi'] = inflation_df['value']

    baseCPI = inflation_df['cpi'].head(1).item()
    basePPI = inflation_df['ppi'].head(1).item()

    mom_columns = ["month", "CPI_MoM", "PPI_MoM"]
    mom_data = []

    for i in range(len(inflation_df)):
        if i == 0:
            #Skip Base Case
            continue
        row = inflation_df.iloc[i]
        cpi = row['cpi'] - baseCPI
        ppi = row['ppi'] - basePPI 
        baseCPI = row['cpi']
        basePPI = row['ppi']
        mom_data.append({"month": row['month'], "CPI_MoM": cpi, "PPI_MoM": ppi})
    mom_inflation_df = pd.DataFrame(mom_data, columns=mom_columns)
    return mom_inflation_df

mom_inflation_df = get_mom_inflation()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: Economic Data Dashboard
'''

st.header('Total Employment in Thousands', divider='gray')

''

# Create the chart using Altair
chart = alt.Chart(employment_df).mark_line().encode(
    x='month',
    y=alt.Y('Employment in Thousands', scale=alt.Scale(domainMin=0)) # Set minimum to 0, maximum automatically determined
)

# Render the chart in Streamlit
st.altair_chart(chart, use_container_width=True)

st.header('Unemployment Rate', divider='gray')

''

st.line_chart(
    unemployment_df,
    x='month',
    y='Unemployment',
)

st.header('Inflation MoM', divider='gray')

''

st.line_chart(
    inflation_df,
    x='month',
    y=['cpi', 'ppi'],
)

st.header('Inflation', divider='gray')

''

st.line_chart(
    inflation_df,
    x='month',
    y=['cpi', 'ppi'],
)

st.header('Inflation MoM', divider='gray')
#Bonus Chart since I felt like I this was too little

''

st.line_chart(
    mom_inflation_df,
    x='month',
    y=['CPI_MoM', 'PPI_MoM'],
)

