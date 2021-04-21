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

count = 1
while True:
    house_link = driver.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[1]/div[{}]'.format(count))
    house_link = house_link.find_elements_by_tag_name('a')[0]
    house_link = house_link.get_attribute('href')

    driver.get(house_link)
    time.sleep(3)

    features = []

    list_features = driver.find_element_by_class_name('features')
    list_features = list_features.find_elements_by_tag_name("li")

    for feature in list_features:
        features.append(feature.text) 

    try:
        button_features = driver.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[1]/div[3]/button')
        button_features.click()

        more_features = driver.find_element_by_class_name('amenities__list')
        list_extra_features = more_features.find_elements_by_tag_name('li')

        for feature in list_extra_features:
            features.append(feature.text)
    
    except Exception as e:
        print(e)

    aluguel = driver.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[2]/div[1]/div/div[1]/h3').text
    condominio = driver.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[2]/div[1]/div/div[2]/ul/li[1]/span[2]').text
    iptu = driver.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[2]/div[1]/div/div[2]/ul/li[3]/span[2]').text 
    fotos = driver.find_element_by_xpath('//*[@id="js-site-main"]/div[1]/div[2]/span').text
    endereco = driver.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[1]/div[1]/section/div/div/p').text
    description = driver.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[1]/div[4]/div[1]/div/div/p').text
    description_len = len(description.split(' '))

    features.extend([aluguel, condominio, iptu, fotos, endereco, description_len])
    count+= 1

# driver.close()