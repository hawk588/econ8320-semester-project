import streamlit as st
import pandas as pd
import math
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

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

st.header('Total Employment', divider='gray')

''

st.line_chart(
    employment_df,
    x='month',
    y='value',
)

st.header('Unemployment Rate', divider='gray')

''

st.line_chart(
    unemployment_df,
    x='month',
    y='value',
)

st.header('Inflation MoM', divider='gray')

''

st.line_chart(
    inflation_df,
    x='month',
    y=['cpi', 'ppi'],
)

