import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os
import pandas as pd
import time 

def get_driver():
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options)
    return driver

def get_data():
    if 'house_data.csv' in os.listdir('data'):
        house_df = pd.read_csv('data/house_data.csv')
        data = {
            'aluguel': list(house_df['aluguel'].values),
            'condominio': list(house_df['condominio'].values),
            'iptu': list(house_df['iptu'].values),
            'fotos': list(house_df['fotos'].values),
            'endereco': list(house_df['endereco'].values),
            'description': list(house_df['description'].values),
            'description_len': list(house_df['description_len'].values),
            'features': list(house_df['features'].values),
            'url': list(house_df['url'].values)
        }
    else:
        data = {
            'aluguel': [],
            'condominio': [],
            'iptu': [],
            'fotos': [],
            'endereco': [],
            'description': [],
            'description_len': [],
            'features': [],
            'url': []
        }
    return data

def apply_search_filters(driver):
    driver.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[1]/nav/div/div/form/fieldset[1]/div[3]/div/div/label').click()

    list_pages = driver.find_element_by_class_name('select-multiple__list')
    list_pages = list_pages.find_elements_by_tag_name("li") 

    for i in range(len(list_pages)):
        list_pages = driver.find_element_by_class_name('select-multiple__list')
        list_pages = list_pages.find_elements_by_tag_name("li") 
        if i not in [3, 7, 10]:
            list_pages[i].click()
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, {})".format(str(60 + (i*10))))

def get_house_link(count):
    try:
        house_link = driver.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[1]/div[{}]'.format(count))
        house_link = house_link.find_elements_by_tag_name('a')[0]
        return house_link.get_attribute('href')
    except:
        return ''

def add_features(list_features, features):
    for feature in list_features:
        features.append(feature.text) 
    
    return features

def add_value(xpath):
    try:
        return driver.find_element_by_xpath(xpath).text
    except:
        return ''

def house_scraping(driver, data):
    count = 1
    try:
        while True:
            house_link = get_house_link(count)

            if house_link:
                if house_link in data['url']:
                    count += 1
                    continue

                driver.get(house_link)
                time.sleep(1.5)
                features = []

                list_features = driver.find_element_by_class_name('features')    
                features = add_features(list_features.find_elements_by_tag_name("li"), features)

                try:
                    button_features = driver.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[1]/div[3]/button')
                    button_features.click()

                    more_features = driver.find_element_by_class_name('amenities__list')
                    features = add_features(more_features.find_elements_by_tag_name('li'), features)   
                except Exception as e:
                    print(e)

                data['url'].append(house_link)

                rent_value = add_value('//*[@id="js-site-main"]/div[2]/div[2]/div[1]/div/div[1]/h3')
                if 'mês' not in rent_value.split('/'):
                    rent_value = add_value('//*[@id="js-site-main"]/div[2]/div[2]/div[1]/div/div[2]/div/h3')

                data['aluguel'].append(rent_value)               
                data['condominio'].append(add_value('//*[@id="js-site-main"]/div[2]/div[2]/div[1]/div/div[2]/ul/li[1]/span[2]'))
                data['iptu'].append(add_value('//*[@id="js-site-main"]/div[2]/div[2]/div[1]/div/div[2]/ul/li[3]/span[2]'))
                data['fotos'].append(add_value('//*[@id="js-site-main"]/div[1]/div[2]/button/span'))
                data['endereco'].append(add_value('//*[@id="js-site-main"]/div[2]/div[1]/div[1]/section/div/div/p'))
                data['description'].append(add_value('//*[@id="js-site-main"]/div[2]/div[1]/div[4]/div[1]/div/div/p'))
                data['description_len'].append(0 if not data['description'][-1] else len(data['description'][-1].split(' ')))
                data['features'].append(features)
                driver.back()
                time.sleep(2)
                count+= 1
            else:
                elem = driver.find_element_by_css_selector('#js-site-main > div.results__container > div.results__content > section > div.results-main__panel.js-list > div.js-results-pagination > div > ul > li:nth-child(2)')
                actions = ActionChains(driver)
                actions.move_to_element(elem).perform()

                list_pages = driver.find_element_by_class_name('pagination__wrapper')
                list_pages = list_pages.find_elements_by_tag_name("li")  

                next_page_elem = '//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[{}]'.format(9)    
                next_page_elem = driver.find_element_by_xpath(next_page_elem)

                next_page_elem.click()
                time.sleep(2) 

                return house_scraping(driver, data)
    except Exception as e:
        print(e)
        house_df = pd.DataFrame(data)
        house_df.to_csv('data/house_data.csv', index=False)
        return ''

state = 'sp'
city = 'bauru'

while True:
    navigate_url = "https://www.vivareal.com.br/aluguel/{}/{}".format(state, city)
    driver = get_driver()
    driver.get(navigate_url)
    time.sleep(2)
    data = get_data()
    driver.find_element_by_xpath('//*[@id="cookie-notifier-cta"]').click()
    apply_search_filters(driver)

    house_scraping(driver, data)
    driver.close()
