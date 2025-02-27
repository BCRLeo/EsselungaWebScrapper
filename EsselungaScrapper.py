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


def FindPromotions(product):

    discount_description = None
    discount_start_date = None
    discount_end_date = None
    promotion_div = product.find('div', class_='product-promotional')

    if promotion_div:
        
        discount_img = promotion_div.find('img', attrs={'el-tooltip': True})
        
        if discount_img:

            discount_info = discount_img['el-tooltip']
            description_match = re.search(r"^(.*?)\s*\(dal", discount_info)
            
            if description_match:
                
                discount_description = description_match.group(1).strip()
            
            date_match = re.search(r"\(dal\s+([\d/]+)\s+al\s+([\d/]+)\)", discount_info)
            
            if date_match:
                
                start_date_str = date_match.group(1)
                end_date_str = date_match.group(2)
                discount_start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
                discount_end_date = datetime.strptime(end_date_str, '%d/%m/%Y').date()
        return [discount_description, discount_start_date, discount_end_date]

def Main(ProdObject):

    start = time.time() 
    
    chrome_options = Options()
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")   
    chrome_options.add_argument("--disable-search-engine-choice-screen")

    service = Service(executable_path='C:/Users/leona/Desktop/ML stuff/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(ProdObject.ProductsPage)
    
    WebDriverWait(driver, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    last_height = 0
    scrolltime = time.time()
    
    while True:
        
        html = driver.page_source
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5) 
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                time.sleep(3)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print("No more content to load.")
                    break
            
        last_height = new_height
        
    print("scroll time = {}".format(scrolltime-time.time()))


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all("div", class_="product")
    
    for product in products:
        
        attributes = product.attrs
        
        name = product.find('a', class_='el-link').get('title', product.find('img').get('alt'))
        price_span = product.find('span', class_='product-label-price-unit')
        price = price_span.text.strip() if price_span else "Price not available"
        PromotionInfo = FindPromotions(product)
        
        ProdObject.ProductsIDs.append(int(product.get('id', '-1')))
        ProdObject.ProductsNames.append(name)
        ProdObject.ProductsPrices.append(price)
        ProdObject.ProductsDiscounts.append(PromotionInfo[0])
        ProdObject.ProductsDiscountsStart.append(PromotionInfo[1])
        ProdObject.ProductsDiscountsEnd.append(PromotionInfo[2])
     
    driver.quit()
    print(time.time()-start)
    
    return ProdObject

if __name__ == "__main__":
    temp = Main('https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002315/frutta-fresca')
    for i in range(len(temp[0])):
        print("""Product ID = {}
Name = {}
Price = {}
Discount Description = {}
Duration = {} to {}""".format(temp[0][i], temp[1][i], temp[2][i], temp[3][i], temp[4][i], temp[5][i]))
        print("-" * 40) 









 

