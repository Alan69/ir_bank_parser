from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from googletrans import Translator
import json
import time
from bs4 import BeautifulSoup
import requests

def extract_firm_reference_numbers(soup):
    td_elements = soup.find_all(class_='gvwColumn')
    firm_reference_numbers = [td.get_text(strip=True) for td in td_elements if td.get_text(strip=True)]
    return firm_reference_numbers

def extract_firm_info(soup):
    name = soup.find(class_='f8_ctl00_cphRegistersMasterPage_c1wrptData').get_text(strip=True)
    entity_type = soup.find(class_='f2_ctl00_cphRegistersMasterPage_c1wrptData').find('a').get_text(strip=True)
    description = soup.find(class_='f3_ctl00_cphRegistersMasterPage_c1wrptData').get_text(strip=True)
    return {"Name": name, "Entity Type": entity_type, "Description": description}

def translate_to_russian(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='ru')
    return translated_text.text

def translate_extracted_data(extracted_data):
    translated_data = []
    for item in extracted_data:
        translated_item = {}
        translated_item["Name"] = item["Name"]
        for key, value in item.items():
            if key != "Name":
                translated_item[key] = translate_to_russian(value)
        translated_data.append(translated_item)
    return translated_data

def main():
    driver = webdriver.Chrome()

    search_url = "https://registers.centralbank.ie/FirmSearchResultsPage.aspx?searchEntity=Institution&searchType=Name&searchText=&registers=All&firmType=All"
    base_firm_url = "https://registers.centralbank.ie/FirmDataPage.aspx?firmReferenceNumber="

    extracted_data = []
    driver.get(search_url)

    while True:
        try:
            page_select = Select(driver.find_element(By.ID, 'ctl00_cphRegistersMasterPage_gvwSearchResults_ctl18_ddlPages'))
            total_pages = len(page_select.options) # для прода
            break
        except NoSuchElementException:
            time.sleep(1)
    test_num = 2 # для теста
    for page_num in range(1, test_num + 1):
        driver.get(search_url)
        while True:
            try:
                page_select = Select(driver.find_element(By.ID, 'ctl00_cphRegistersMasterPage_gvwSearchResults_ctl18_ddlPages'))
                break
            except NoSuchElementException:
                time.sleep(1)

        page_select.select_by_value(str(page_num))
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        firm_reference_numbers = extract_firm_reference_numbers(soup)

        for reference_number in firm_reference_numbers:
            firm_url = base_firm_url + reference_number
            page = requests.get(firm_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            firm_info = extract_firm_info(soup)
            extracted_data.append(firm_info)

    translated_data = translate_extracted_data(extracted_data)

    driver.quit()

    with open("main_extracted_data.json", "w", encoding='utf-8') as json_file:
        json.dump(translated_data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
