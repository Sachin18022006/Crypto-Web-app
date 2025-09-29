import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import requests
import json
import os
from dotenv import load_dotenv
import datetime as dt
import yfinance as yf # Replaced cryptocmd with yfinance

# --- BASIC SETUP ---

# Load API key from .env file
load_dotenv()
CMC_API_KEY = os.getenv('CMC_API_KEY')

# Set Page to expand to full width
st.set_page_config(layout="wide")

# Image
try:
    image = Image.open('logo.jpg')
    st.image(image, width=500)
except FileNotFoundError:
    st.warning("logo.jpg not found. Please make sure it's in the same folder as the script.")

# Title and About section
st.title('Crypto Web App ')
st.markdown("This app retrieves cryptocurrency data from the **CoinMarketCap API**!")
expander_bar = st.expander('About')
expander_bar.markdown("""
* **Made By:** Sachin B S
* **Data source:** [CoinMarketCap API](http://coinmarketcap.com/api) and [Yahoo Finance](https://finance.yahoo.com).
""")

# --- SIDEBAR AND INPUTS ---
col1 = st.sidebar
col1.header('Input Options')
currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC'))


# --- DATA LOADING (API FUNCTIONS) ---

@st.cache_data(ttl=600) # Cache data for 10 minutes
def load_api_data():
    if not CMC_API_KEY:
        st.error("API key not found. Please create a .env file with your CMC_API_KEY.")
        return pd.DataFrame()

    listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }
    
    try:
        listings_response = requests.get(listings_url, params={'limit': '100', 'convert': currency_price_unit}, headers=headers)
        listings_response.raise_for_status()
        listings_data = listings_response.json()
        
        df = pd.json_normalize(listings_data['data'])

        rename_map = {
            'name': 'coin_name', 'symbol': 'coin_symbol',
            f'quote.{currency_price_unit}.market_cap': 'market_cap',
            f'quote.{currency_price_unit}.percent_change_1h': 'percent_change_1h',
            f'quote.{currency_price_unit}.percent_change_24h': 'percent_change_24h',
            f'quote.{currency_price_unit}.percent_change_7d': 'percent_change_7d',
            f'quote.{currency_price_unit}.price': 'price',
            f'quote.{currency_price_unit}.volume_24h': 'volume_24h'
        }
        df = df.rename(columns=rename_map)
        
        required_columns = list(rename_map.values())
        return df[required_columns]

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()

# --- APP LOGIC ---
df = load_api_data()

if not df.empty:
    sorted_coin = sorted(df['coin_symbol'])
    selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, ['BTC', 'ETH', 'ADA', 'DOGE', 'BNB'])
    selected_coin_df = df[df['coin_symbol'].isin(selected_coin)]

    percent_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
    selected_percent_timeframe = f'percent_change_{percent_timeframe}'

    # --- Main Page Layout ---
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        st.subheader(f'Bar plot of % Price Change (Last {percent_timeframe})')
        if not selected_coin_df.empty:
            bar_chart_df = selected_coin_df.sort_values(by=[selected_percent_timeframe])
            bar_chart_df['positive'] = bar_chart_df[selected_percent_timeframe] > 0
            plt.style.use('seaborn-v0_8-darkgrid')
            fig, ax = plt.subplots(figsize=(6,4))
            ax.barh(bar_chart_df['coin_symbol'], bar_chart_df[selected_percent_timeframe],
                    color=bar_chart_df['positive'].map({True: 'lightblue', False: 'pink'}))
            ax.set_xlabel('Percent Change')
            st.pyplot(fig)

    with row1_col2:
        st.subheader('Bar plot of Market Cap (Selected Cryptos)')
        if not selected_coin_df.empty:
            plt.style.use('seaborn-v0_8-darkgrid')
            fig, ax = plt.subplots(figsize=(6,4))
            ax.bar(selected_coin_df['coin_symbol'], selected_coin_df['market_cap'])
            ax.set_ylabel('Market Cap')
            ax.ticklabel_format(style='plain', axis='y')
            plt.xticks(rotation=45)
            st.pyplot(fig)

    with row2_col1:
        st.subheader('Market Share of Top Cryptos')
        btc_market_cap = df.loc[df['coin_symbol'] == 'BTC', 'market_cap'].iloc[0]
        eth_market_cap = df.loc[df['coin_symbol'] == 'ETH', 'market_cap'].iloc[0]
        total_market_cap_top100 = df['market_cap'].sum()
        
        btc_dominance = (btc_market_cap / total_market_cap_top100) * 100
        eth_dominance = (eth_market_cap / total_market_cap_top100) * 100
        alt_coins_share = 100 - (btc_dominance + eth_dominance)
        
        percentages = [btc_dominance, eth_dominance, alt_coins_share]
        labels = ['Bitcoin', 'Ethereum', 'Alt Coins']
        colors = ['#66b3ff','#ff9999','#99ff99']
        
        fig, ax = plt.subplots(figsize=(6,4))
        ax.pie(percentages, labels=labels, autopct='%.1f%%', startangle=90, colors=colors)
        ax.axis('equal')
        ax.legend(labels, loc="best")
        st.pyplot(fig)

    # --- Historical Line Graph (Using yfinance) ---
    with row2_col2:
        st.subheader('Historical Price Data')
        
        @st.cache_data
        def get_historical_data(symbol, start, end):
            # Format ticker for Yahoo Finance (e.g., BTC -> BTC-USD)
            ticker = f"{symbol}-{currency_price_unit}"
            try:
                data = yf.download(ticker, start=start, end=end)
                if data.empty:
                    st.warning(f"Could not retrieve historical data for {symbol}. Ticker may be incorrect.")
                    return pd.DataFrame()
                return data
            except Exception as e:
                st.warning(f"Could not retrieve historical data for {symbol}. Error: {e}")
                return pd.DataFrame()

        selected_crypto_hist = st.selectbox('Select crypto', sorted_coin)
        
        if selected_crypto_hist:
            today = dt.date.today()
            thirty_days_ago = today - dt.timedelta(days=30)
            
            hist_df = get_historical_data(selected_crypto_hist, thirty_days_ago, today)
            
            if not hist_df.empty:
                plt.style.use('seaborn-v0_8-darkgrid')
                fig, ax = plt.subplots(figsize=(6,4))
                ax.plot(hist_df.index, hist_df['Close'], color='green') # Use hist_df.index for dates
                ax.set_title(f'{selected_crypto_hist} over the last 30 days')
                ax.set_ylabel(f'Closing Price ({currency_price_unit})')
                plt.xticks(rotation=45)
                st.pyplot(fig)

    # --- Data Tables ---
    st.markdown("---")
    st.header('**Tables**')
    
    st.subheader('Price Data of Selected Cryptocurrencies')
    price_cols = ['coin_name', 'coin_symbol', 'market_cap', 'price', 'volume_24h']
    st.dataframe(selected_coin_df[price_cols])
    
    def filedownload(df_to_download):
        csv = df_to_download.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="crypto_data.csv">Download CSV File</a>'
        return href

    if not selected_coin_df.empty:
        st.markdown(filedownload(selected_coin_df), unsafe_allow_html=True)

    st.subheader('Percent Change Data of Select Cryptocurrencies')
    percent_cols = ['coin_name', 'coin_symbol', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d']
    st.dataframe(selected_coin_df[percent_cols])