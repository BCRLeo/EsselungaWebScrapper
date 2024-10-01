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

class Indicators:
    def __init__(self, button):
        self.Button = button
        self.IndicatorName = []
        self.IndicatorLatest = []
        self.IndicatorPrevious = []
        self.IndicatorUnit = []
        self.IndicatorDate = []



def FindIndexes():
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
    GDP = Scrape(Indicators("#gdp"))
    Labour = Scrape(Indicators("#labour"))
    Prices = Scrape(Indicators("#prices"))
    Money = Scrape(Indicators("#money"))
    Trade = Scrape(Indicators("#trade"))
    Government = Scrape(Indicators("#government"))
    Business = Scrape(Indicators("#business"))
    Consumer = Scrape(Indicators("#consumer"))
    Housing = Scrape(Indicators("#housing"))
    Energy = Scrape(Indicators("#energy"))
    Health = Scrape(Indicators("#health"))
    print(GDP.IndicatorName, Labour.IndicatorName, Prices.IndicatorName, Trade.IndicatorName, Government.IndicatorName, Business.IndicatorName,
          Consumer.IndicatorName, Housing.IndicatorName, Energy.IndicatorName, Health.IndicatorName)

    driver.close()
    #returns consumer confidence index
    #CPI, producer price index, purchasing Manger's index,
    #retail sales index, wholesale price index,
    #industrial production index
    #Business confidence index, stock market indices (FTSE MIB for ita),
    #Supply chain indices, transportation indices,
    #Leading economic index (LEI), consumer expectation index,
    #corruption perception index
    pass
def FindEconomicData():
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



    
    #returns last 7 days rainfall, expected rainfall, average temperature, highs and lows
    #sunlight?, extreme wind
    pass

def FindSeasonalData():
    #returns upcoming holidays (HolidayInterval = 4 weeks
    pass
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



FindIndexes()

















    
