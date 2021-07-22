from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import time 

driver = webdriver.Chrome('/home/alvaro/Downloads/chromedriver')

state = 'sp'
city = 'piracicaba'

navigate_url = "https://www.vivareal.com.br/aluguel/{}/{}".format(state, city)
driver.get(navigate_url)
time.sleep(2)

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

# apply_search_filters(driver)

# elem = driver.find_element_by_xpath('//*[@id="filter-location-search-input"]')
# elem.send_keys("Piracicaba - SP")
# time.sleep(3)
# elem.send_keys(Keys.ENTER)
# time.sleep(2)

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

def house_scraping(driver, page_number=2):
    count = 1
    visited_pages = []

    while True:
        house_link = get_house_link(count)

        if house_link:
            driver.get(house_link)

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
        else:
            elem = driver.find_element_by_css_selector('#js-site-main > div.results__container > div.results__content > section > div.results-main__panel.js-list > div.js-results-pagination > div > ul > li:nth-child(2)')
            actions = ActionChains(driver)
            actions.move_to_element(elem).perform()

            try:
                list_pages = driver.find_element_by_class_name('pagination__wrapper')
                list_pages = list_pages.find_elements_by_tag_name("li")  
   
                page_number = 2 if page_number + 1 == 9 else page_number + 1

                last_number_elem = '//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[{}]'.format(page_number)    
                last_number_elem = driver.find_element_by_xpath(last_number_elem)

                last_number_elem.click()
                time.sleep(2) 

                house_scraping(driver, page_number)
            except Exception as e:
                print(e)
                return ''

house_scraping(driver)
pages_to_visit = []

def add_pages_to_visit(pages_to_visit):
    list_pages = driver.find_element_by_class_name('pagination__wrapper')
    list_pages = list_pages.find_elements_by_tag_name("li")     
    last_number_elem = '//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[{}]'.format(len(list_pages) - 1)    
    last_number_elem = driver.find_element_by_xpath(last_number_elem)
    last_number = last_number_elem.text

    last_number_elem.click()

    if not pages_to_visit:
        pages_to_visit.extend(list_pages[1:(int(last_number) + 1)])
        return True, pages_to_visit
    elif last_number != pages_to_visit[-1].text:
        pages_to_visit.extend(list_pages[1:(int(last_number) + 1)])
        return True, pages_to_visit
    else:
        return False, pages_to_visit

try:
    getting_page = True

    while getting_page:
        getting_page, pages_to_visit = add_pages_to_visit(pages_to_visit)
except Exception as e:
    print(e)
        

# driver.close()
# find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[6]')
# //*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[6]
# //*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[7]
# //*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[2]

# //*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]

# //*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]