import requests
import pandas as pd
import mplfinance as mpf
from datetime import datetime


def get_crypto_data(crypto_id, days=1):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['prices']
def process_data(prices):
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.resample('6H').agg({
        'price': ['first', 'max', 'min', 'last']
    })
    df.columns = ['Open', 'High', 'Low', 'Close']
    df.dropna(inplace=True)
    return df
def plot_and_save_candlestick(df, crypto_name, filename='crypto_candle.png'):
    style = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=mpf.make_marketcolors(volume="yellow"),facecolor='black', edgecolor='white',gridcolor='gray')
    mpf.plot(
        df,
        type='line',
        style=style,
        title=f'{crypto_name} Chart',
        ylabel='Price (USD)',
        
        savefig=filename
    )
    print(f"نمودار با موفقیت به عنوان {filename} ذخیره شد.")

crypto_id = "tron" 
prices = get_crypto_data(crypto_id, days=30)

df = process_data(prices)

plot_and_save_candlestick(df, "tron", filename='bitcoin.png')