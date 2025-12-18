import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Economic Data Dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

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

    mom_columns = ["month", "CPI_MoM", "PPI_MoM", "year"]
    mom_data = []

    for i in range(len(inflation_df)):
        if i == 0:
            #Skip Base Case
            continue
        row = inflation_df.iloc[i]
        cpi = row['cpi'] - baseCPI
        ppi = row['ppi'] - basePPI 
        year = row['year']
        baseCPI = row['cpi']
        basePPI = row['ppi']
        mom_data.append({"month": row['month'], "CPI_MoM": cpi, "PPI_MoM": ppi, "year": year})
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

min_value = employment_df['year'].min()
max_value = employment_df['year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

employ, unemploy, cpippi, mom = st.tabs(["Total Employment", "Unemployment", "CPI/PPI", "CPI/PPI MoM"])

with employ:
    st.header("Total Employment")
    # Create the chart using Altair
    employment_df = employment_df[(employment_df['year'] >= from_year) & (employment_df['year'] <= to_year)]
    chart = alt.Chart(employment_df).mark_line().encode(
        x=alt.X('month',axis=alt.Axis(tickCount=12)),
        y=alt.Y('Employment in Thousands') # Set minimum to 0, maximum automatically determined
    )

    # Render the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

with unemploy:
    st.header('Unemployment Rate', divider='gray')

    ''
    unemployment_df = unemployment_df[(unemployment_df['year'] >= from_year) & (unemployment_df['year'] <= to_year)]
    st.line_chart(
        unemployment_df,
        x='month',
        y='Unemployment',
    )

with cpippi:
    st.header('Inflation', divider='gray')

    ''
    inflation_df = inflation_df[(inflation_df['year'] >= from_year) & (inflation_df['year'] <= to_year)]
    st.line_chart(
        inflation_df,
        x='month',
        y=['cpi', 'ppi'],
    )

with mom:
    st.header('Inflation MoM', divider='gray')
    #Bonus Chart since I felt like I this was too little

    ''
    mom_inflation_df = mom_inflation_df[(mom_inflation_df['year'] >= from_year) & (mom_inflation_df['year'] <= to_year)]
    st.line_chart(
        mom_inflation_df,
        x='month',
        y=['CPI_MoM', 'PPI_MoM'],
    )









