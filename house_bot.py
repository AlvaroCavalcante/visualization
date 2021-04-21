from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 

driver = webdriver.Chrome('/home/alvaro/Downloads/chromedriver')
driver.get("https://www.vivareal.com.br/aluguel/")
time.sleep(2)
elem = driver.find_element_by_xpath('//*[@id="filter-location-search-input"]')
elem.send_keys("Rio Claro - SP")
time.sleep(3)
elem.send_keys(Keys.ENTER)
time.sleep(2)

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

count = 1
while True:
    house_link = get_house_link(count)
    driver.get(house_link)
    time.sleep(3)

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

    aluguel = add_value('//*[@id="js-site-main"]/div[2]/div[2]/div[1]/div/div[1]/h3')
    condominio = add_value('//*[@id="js-site-main"]/div[2]/div[2]/div[1]/div/div[2]/ul/li[1]/span[2]')
    iptu = add_value('//*[@id="js-site-main"]/div[2]/div[2]/div[1]/div/div[2]/ul/li[3]/span[2]')
    fotos = add_value('//*[@id="js-site-main"]/div[1]/div[2]/span')
    endereco = add_value('//*[@id="js-site-main"]/div[2]/div[1]/div[1]/section/div/div/p')
    description = add_value('//*[@id="js-site-main"]/div[2]/div[1]/div[4]/div[1]/div/div/p')
    description_len = 0 if not description else len(description.split(' '))

    features.extend([aluguel, condominio, iptu, fotos, endereco, description_len])

    driver.back()
    count+= 1

# driver.close()