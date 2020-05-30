from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def scrape():
    # Storage for Scraped Data
    data={}

    # Initialize Driver
    driver_path = r'C:/Users/PaulB/Documents/Drivers/chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path)

    # Scrape NASA Mars News
    driver.get("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")
    time.sleep(2)

    newest_title_xpath = '/html/body/div[3]/div/div[3]/div[3]/div/article/div/section/div/ul/li[1]/div/div/div[2]/a'
    newest_paragraph_xpath = '/html/body/div[3]/div/div[3]/div[3]/div/article/div/section/div/ul/li[1]/div/div/div[3]'
    newest_title = driver.find_elements_by_xpath(newest_title_xpath)[0].text
    data['newsTitle'] = newest_title
    newest_paragraph = driver.find_elements_by_xpath(newest_paragraph_xpath)[0].text
    data['newsText'] = newest_paragraph

    # Scrape Mars Featured Image
    driver.get("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    time.sleep(2)
    driver.find_element_by_css_selector('.button').click()

    time.sleep(2)
    img_site_html = driver.find_elements_by_class_name("fancybox-inner")
    image_title = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]").text
    image_title = image_title.split('\n')[0]
    data['featuredTitle'] = image_title
    image_url = driver.find_element_by_class_name("fancybox-image").get_attribute('src')
    data['featuredURL'] = image_url

    # Scrape Mars Weather
    driver.get("https://twitter.com/marswxreport?lang=en")
    time.sleep(2)
    tweet_xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div[2]/section/div/div/div/div[1]/div/div/div/div/article/div/div[2]/div[2]/div[2]/div[1]/div/span'
    newestTweet = driver.find_element_by_xpath(tweet_xpath).text
    data['marsWeather'] = newestTweet

    # Scrape Mars Facts
    driver.get("https://space-facts.com/mars/")
    time.sleep(2)
    table_id = driver.find_element(By.ID, 'tablepress-p-mars-no-2')
    rows = table_id.find_elements(By.TAG_NAME, "tr")
    marsFacts=[]
    for row in rows:
        col1 = row.find_elements(By.TAG_NAME, "td")[0].text
        col2 = row.find_elements(By.TAG_NAME, "td")[1].text
        marsFact = [col1,col2]
        marsFacts.append(marsFact)
    marsFactDF = pd.DataFrame(marsFacts[1:], columns=marsFacts[0])
    marsFactDF = marsFactDF.to_html(index=False)
    data['marsFacts'] = marsFactDF

    # Scrape Mars Hemispheres
    driver.get("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    time.sleep(2)
    hrefs = driver.find_elements_by_css_selector('.item .description a')
    href_list = [h.get_attribute('href') for h in hrefs]

    hemisphere_titles = [hrefs[i].text[:-9] for i in range(len(href_list))]
    hemisphere_urls = []
    for i in range(len(href_list)):
        driver.get(href_list[i])
        time.sleep(2)
        hemisphere_urls.append(driver.find_element_by_css_selector('.container .downloads a').get_attribute('href'))
    hemisphere_dictionary = [{"title":hemisphere_titles[i], "url":hemisphere_urls[i]} for i in range(len(href_list))]
    data['marsHemispheres'] = hemisphere_dictionary

    return data
