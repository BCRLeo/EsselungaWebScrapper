#####This file will gather the extra data asside from the data from esselunga
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
####Weather imports
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from openai import OpenAI
from models import Indicators
# Set up your OpenAI API key
#!!!!!!!!!!!!!!!!REMOVE WHEN PUBLISHING TO GITHUB!!!!!!!!!!!!!!!!!!!!!!!!!





def FindEconomicData():
    chrome_options = Options()
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-search-engine-choice-screen")

    service = Service(executable_path='C:/Users/leona/Desktop/ML stuff/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://tradingeconomics.com/italy/indicators")
    def Scrape(Object):
        
        tab = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.nav-link[href="{}"]'.format(Object.Button))))
        
        tab.click()

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')


        tbody = soup.select_one('{} tbody'.format(Object.Button))

            
        for row in tbody.find_all('tr'):
            
            cells = row.find_all('td')
            
            if len(cells) >= 7:
                Object.IndicatorName.append(cells[0].find('a').get_text(strip=True))
                Object.IndicatorLatest.append(cells[1].get_text(strip=True))
                Object.IndicatorPrevious.append(cells[2].get_text(strip=True))
                Object.IndicatorUnit.append(cells[5].get_text(strip=True))
                Object.IndicatorDate.append(cells[6].get_text(strip=True))
                
        return Object
    GDP = Scrape(Indicators("GDP", "#gdp"))
    Labour = Scrape(Indicators("Labour", "#labour"))
    Prices = Scrape(Indicators("Prices", "#prices"))
    Money = Scrape(Indicators("Money", "#money"))
    Trade = Scrape(Indicators("Trade", "#trade"))
    Government = Scrape(Indicators("Government", "#government"))
    Business = Scrape(Indicators("Business", "#business"))
    Consumer = Scrape(Indicators("Consumer", "#consumer"))
    Housing = Scrape(Indicators("Housing", "#housing"))
    Energy = Scrape(Indicators("Energy", "#energy"))
    Health = Scrape(Indicators("Health", "#health"))

    driver.close()
    return [GDP, Labour, Prices, Money, Trade, Government, Business, Consumer, Housing, Energy, Health]

    
    #returns consumer confidence index
    #CPI, producer price index, purchasing Manger's index,
    #retail sales index, wholesale price index,
    #industrial production index
    #Business confidence index, stock market indices (FTSE MIB for ita),
    #Supply chain indices, transportation indices,
    #Leading economic index (LEI), consumer expectation index,
    #corruption perception index
    pass
#def FindEconomicData():
    #this returns all data that isnt an index: unemployment rate, GDP growth rate,
    # inflation rate, balance of trade (M-X),  labor costs, interest rates
    #exchnage rates (euro to: dollars, yen, chinese yuan etc),
    #money suply, cosummer and corporate debt levels, tax rates, savings rates,
    #Capacity utilisation rate, Consumer spending data,import export tarrifs,
    #consumer credit availability, gov fiscal policy indicators
    
    pass

def FindWeatherData():
    #https://open-meteo.com/en/docs
    #access this website and scrape, provides code
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
            "latitude": 45.4685,
            "longitude": 9.1824,
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "daylight_duration", "sunshine_duration", "uv_index_max", "precipitation_sum", "rain_sum", "showers_sum", "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max"],
            "timezone": "Europe/Berlin",
            "past_days": 7,
            "temporal_resolution": "hourly_6",
            "models": "best_match"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
    daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
    daily_daylight_duration = daily.Variables(5).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(6).ValuesAsNumpy()
    daily_uv_index_max = daily.Variables(7).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(8).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(9).ValuesAsNumpy()
    daily_showers_sum = daily.Variables(10).ValuesAsNumpy()
    daily_precipitation_hours = daily.Variables(11).ValuesAsNumpy()
    daily_precipitation_probability_max = daily.Variables(12).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(13).ValuesAsNumpy()
    daily_wind_gusts_10m_max = daily.Variables(14).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
    daily_data["daylight_duration"] = daily_daylight_duration
    daily_data["sunshine_duration"] = daily_sunshine_duration
    daily_data["uv_index_max"] = daily_uv_index_max
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["showers_sum"] = daily_showers_sum
    daily_data["precipitation_hours"] = daily_precipitation_hours
    daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max

    daily_dataframe = pd.DataFrame(data = daily_data)
    return daily_dataframe
    print(daily_dataframe.to_string())
    pass
"""
def FindSeasonalData():
    client = OpenAI(
    api_key = 
)
    response = client.chat.completions.create(
    model="gpt-4o-mini",  # You can use "gpt-3.5-turbo" for GPT-3.5
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "List all national holidays and the top 10 important non-holiday events in Lombardy in the next three months in the format 'Holiday/Event (in italian and english) - dd/mm/yyyy'."}
    ]
)

# Print the response
    print(response['choices'][0]['message']['content'])

    #returns upcoming holidays (HolidayInterval = 4 weeks
    pass
"""
def FindStrikes():
    #when scrapping italian twitter search for #shioperoMilano
    #returns up coming strikes in europe, as well as strikes that ended up happening in
    #the previous week and the how much it affected the population (rating out of 10)
    pass
def FindComodityPrices():

    #Most of this will be covered in Indexes
    
    #returns price of different types of fule/petrol, natural gas, price of energy,
    #wheat? livestock feed? if findable
    pass
def FindTrends():
    #this will import from the social media trend analysis project sentiment as
    #well as trends, this includes reviews and other online metrics
    pass
def FindDemand():
    #If possible this will return sales volume and demand data
    pass



#FindIndexes()
#FindWeatherData()
#FindSeasonalData()















    
