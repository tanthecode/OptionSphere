#Import all neccessary modules
import requests
import py_vollib.black_scholes_merton.implied_volatility
import py_vollib_vectorized
import numpy as np
import pandas as pd
from datetime import datetime,time
import os
import google.generativeai as genai

#to login to upstox
client_id = "474959c1-1aad-42d7-aee8-e3ae166d53a5"
secret_key='wtqnlbansu'
redirect_uri = "https://api.upstox.com/v2/login"

url = f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
print(url)

#copy code from the url after login
code="yspCla"

url = 'https://api.upstox.com/v2/login/authorization/token'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
    'code': code,
    'client_id': client_id,
    'client_secret':secret_key ,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code',
}

response = requests.post(url, headers=headers, data=data)
access_token=response.json()['access_token']

#just to verify login

url = 'https://api.upstox.com/v2/user/profile'
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token}'
}
response = requests.get(url, headers=headers)


#all stocks/indexs/derivatives listed with trading symbol and instrument_key
scripts=pd.read_csv('https://assets.upstox.com/market-quote/instruments/exchange/NSE.csv.gz')

#function to extract instument_key providing name for indexes
def getinstrumentkeyindx(name):
  return scripts[scripts['name']== name]['instrument_key'].values[0]


#function to extract instument_key providing trading symbol for other instruments
def getinstrumentkey(symbol):
  return scripts[scripts['tradingsymbol']== symbol]['instrument_key'].values[0]



#all available option contracts for the underlying stock
instrument_key=getinstrumentkey("RELIANCE")
url = f'https://api.upstox.com/v2/option/contract?instrument_key={instrument_key}'
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(url, headers=headers)

# Convert only relevent data into data frame for further access

dat = response.json()['data']
d=pd.DataFrame(dat)
columns_needed = ['name', 'trading_symbol', 'strike_price', 'instrument_type', 'expiry','instrument_key' ]
df_filtered = d[columns_needed]

opt_instrument_key='NSE_FO|49945'
df_filtered["instrument_type"] = df_filtered["instrument_type"].str.replace("CE", "c").str.replace("PE", "p")
timestamp = df_filtered.loc[df_filtered['instrument_key'] == opt_instrument_key, 'expiry'].values[0]+'T15:15:00+05:30'
dt = datetime.fromisoformat(timestamp)
expiry = dt.strftime('%Y-%m-%d %H:%M:%S')
strike_price=df_filtered.loc[df_filtered['instrument_key'] == opt_instrument_key, 'strike_price'].values[0]
flag=df_filtered.loc[df_filtered['instrument_key'] == opt_instrument_key, 'instrument_type'].values[0]


trading_symbol = df_filtered["trading_symbol"].tolist()
new_fram=df_filtered.head(50)
#new_fram=df.ilog
new_fram




#to convert Expiry to years
def expiry_to_years(expiry_str):
    expiry_date = datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S')
    current_date = datetime.now()
    delta_seconds = (expiry_date - current_date).total_seconds()
    years = delta_seconds / (365.25 * 24 * 60 * 60)
    return years
time_to_expiry=expiry_to_years(expiry)
time_to_expiry




#to convert time into datetime
def convert_date(row):
  return datetime.fromisoformat(row.datetime).strftime('%Y-%m-%d %H:%M:%S')



#fetch historical data 30 minute time frame

def prices30min(instrument_key,from_date,to_date):
  url = f'https://api.upstox.com/v2/historical-candle/{instrument_key}/30minute/{to_date}/{from_date}'
  headers = {
      'Accept': 'application/json'
  }

  response = requests.get(url, headers=headers)

  # Check the response status
  if response.status_code == 200:
      # Do something with the response data (e.g., print it)
      print(response.json())
  else:
      # Print an error message if the request was not successful
      print("Data cannot be fetched for the provided instrument and/or time frame")

  #convert relevent data to dataframe
  candel_data=pd.DataFrame.from_dict(response.json()['data']['candles'])

  cols=['datetime','open','high','low','close','volume','open intrest']
  candel_data.columns=cols
  candel_data['datetime']=candel_data.apply(convert_date,axis=1)
  close=candel_data['close'].tolist()
  time=candel_data['datetime'].tolist()
  return close,time
from_date='2024-11-29'
to_date='2024-11-29'
opt_tup=prices30min(opt_instrument_key,from_date,to_date)
undr_tup=prices30min(instrument_key,from_date,to_date)
time=opt_tup[1]
time




#to find the last traded price (applicable for both options and their underlying)

def last_traded_price(instrument_key):
  url = f'https://api.upstox.com/v2/market-quote/ltp?instrument_key={instrument_key}'
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token}'
  }
  response = requests.get(url, headers=headers)
  response_data = response.json()
  key = next(iter(response_data['data']))
  last_price = response_data['data'][key]['last_price']
  return( float(last_price))

underlying_ltp=last_traded_price(instrument_key)
option_ltp=last_traded_price(opt_instrument_key)



#Calculation time to expiry
def subtract_datetimes(expiry, time):
    # Convert the strings to datetime objects
    expiry_datetime = datetime.strptime(expiry, '%Y-%m-%d %H:%M:%S')
    newtm=[]
    time_to_maturity=[]
    for i in time:
      newtm.append(datetime.strptime(i, '%Y-%m-%d %H:%M:%S'))
    for i in newtm:
      time_to_maturity.append( expiry_datetime - i)

    seconds_in_year = 365.25 * 24 * 60 * 60  # Approximate seconds in a year
    return [td.total_seconds() / seconds_in_year for td in time_to_maturity]


time_to_maturity=subtract_datetimes(expiry,time)




#Rewriting all variables to be passed in the function
strike_price;
flag;
time_to_maturity;
option_price=opt_tup[0];
underlying_price=undr_tup[0];
risk_free_rate=0.0675;
div_yield=0;




sigma = np.array(py_vollib_vectorized.vectorized_implied_volatility(option_price, underlying_price, strike_price, time_to_maturity, risk_free_rate, flag, div_yield, model='black_scholes_merton',return_as='numpy'))
# implied volatilities
print(sigma)




theoPrice = np.array(py_vollib_vectorized.models.vectorized_black(flag, underlying_price,strike_price,time_to_maturity,risk_free_rate, sigma, return_as='numpy'))
print(theoPrice)
#theoretical option prices




# for option greeks

delta = py_vollib.black_scholes.greeks.numerical.delta(flag, underlying_price[-1], strike_price, time_to_maturity[-1], risk_free_rate, sigma[-1], return_as='numpy')
gamma = py_vollib.black_scholes.greeks.numerical.gamma(flag, underlying_price[-1], strike_price, time_to_maturity[-1], risk_free_rate, sigma[-1], return_as='numpy')
vega = py_vollib.black_scholes.greeks.numerical.vega(flag, underlying_price[-1], strike_price, time_to_maturity[-1], risk_free_rate, sigma[-1], return_as='numpy')
rho = py_vollib.black_scholes.greeks.numerical.rho(flag, underlying_price[-1], strike_price, time_to_maturity[-1], risk_free_rate, sigma[-1], return_as='numpy')
theta = py_vollib.black_scholes.greeks.numerical.theta(flag, underlying_price[-1], strike_price, time_to_maturity[-1], risk_free_rate, sigma[-1], return_as='numpy')




#AI Model
import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyAv2kl83a0u9QFuN6bgBW1rzT77mJ6zdho")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="You need to give a one line summary/conclusion that should be understandable by a lay men whether to consider buying the option or not for which i will be providing option greeks, market price and theoritical value calculated using black scholes model and also information whether how can the future of that market go into",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "model",
      "parts": [
        "Given the market price (7.50) is slightly higher than the theoretical price (7.20),  further investigation into the market's future direction and the potential impact of the option Greeks (especially Vega) is warranted before considering a purchase.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "data = {\n    \"market_price\": 7.50,  # Observed price of the option in the market\n    \"theoretical_price\": 7.20,  # Price calculated using the Black-Scholes model\n    \"option_greeks\": {\n        \"delta\": 0.62,  # Sensitivity of option price to changes in the underlying asset price\n        \"gamma\": 0.025,  # Rate of change of delta with respect to the underlying price\n        \"theta\": -0.015,  # Rate of change of the option price with respect to time\n        \"vega\": 0.12,  # Sensitivity to changes in volatility\n        \"rho\": 0.05,  # Sensitivity to changes in the risk-free interest rate\n    }\n}\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The market price is slightly higher than the theoretical Black-Scholes price, suggesting it might be overvalued.  However, the significant Vega (0.12) indicates high sensitivity to volatility changes, meaning potential for large gains or losses depending on future market fluctuations.  More research into market outlook is crucial before buying.\n",
      ],
    },
  ]
)

market_price = option_price[-1]
theoretical_price = theoPrice[-1]


response = chat_session.send_message(
    f"""
    Given the following data:
    market_price: {market_price},  # Observed price of the option in the market
    theoretical_price: {theoretical_price},  # Price calculated using the Black-Scholes model
    delta: {delta},  # Sensitivity of option price to changes in the underlying asset price
    gamma: {gamma},  # Rate of change of delta with respect to the underlying price
    theta: {theta},  # Rate of change of the option price with respect to time
    vega: {vega},  # Sensitivity to changes in volatility
    rho: {rho},  # Sensitivity to changes in the risk-free interest rate
    """
)


res = response.text
print(res)

