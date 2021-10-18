# Scrapes the Dragon City / All Dragons page for all of the names of the Dragons

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

def config_chrome_driver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
    return driver

def get_dragons(driver) -> dict:
    url = "http://dragoncity.fandom.com/wiki/Dragons/All"
    url = url.encode('ascii','ignore').decode('unicode_escape')
    driver.get(url)
    
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "eggs-filter"))
        )
    except Exception:
        driver.quit()
    
    soup = BeautifulSoup(driver.page_source, "html.parser")

    table = soup.find_all("div", class_="eggs-filter")
    #print(f"\n\n\n\n{'='*20}\nTable: {list(t for t in table)}\n{'='*30}\n\n\n")

    dragon_data = {}
    dragon_names = []
    cleaned_names = []
    for div in table:
        dragon_div = div.select('div[class*="bm_dragon_name"]')
        for ddiv in dragon_div:
            #dragon_data[ddiv.get('id')] = ddiv.span.text
            name = ddiv.span.text
            dragon_names.append(name)
            split_name = name.split(" ")
            name = " ".join(split_name[:-1])
            cleaned_names.append(name)
            #print(f"ID: {ddiv.get('id')}\tName: {ddiv.span.text}")
    #print(dragon_data)
    #return dragon_data
    #return dragon_names
    return cleaned_names

def main():
    driver = config_chrome_driver()
    data = get_dragons(driver)
    #with open("dragon_data.txt","w") as f:
    #with open("dragon_names.txt","w") as f:
    with open("cleaned_dragon_names.txt","w") as f:
        for i in range(len(data)):
            f.write(str(data[i])+"\n")
        #f.write(json.dumps(data, indent=3))
    driver.quit()

if __name__=='__main__':
    main()