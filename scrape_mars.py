# coding: utf-8
# import dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


mars_info = {}

# NASA Mars News


def scrape_mars_news():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    time.sleep(4)
    soup = bs(html, "html.parser")
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p
    return mars_info
    browser.quit()

# JPL Mars Space Images - Featured Image


def scrape_mars_image():
    browser = init_browser()
    mars_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_img_url)
    response = requests.get(mars_img_url)
    soup = bs(response.text, "html.parser")
    img_url = soup.find(class_='button fancybox')['data-fancybox-href']
    main_url = 'https://www.jpl.nasa.gov'
    featured_img_url = main_url + img_url
    mars_info['featured_img_url'] = featured_img_url
    return mars_info
    browser.quit()

# Mars Weather


def scrape_mars_weather():
    browser = init_browser()
    mars_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_url)
    html_mars = browser.html
    soup = bs(html_mars, "html.parser")
    soup.find('div', class_='js-tweet-text-container')
    # Assigns variable to the parsed HTML
    latest_tweet = soup.find('div', class_='js-tweet-text-container')
    try:
        latest_tweet.a.extract()
    except:
        latest_tweet = latest_tweet
    latest_tweet = latest_tweet.text
    mars_info['weather_tweet'] = latest_tweet
    return mars_info
    browser.quit()

# Mars Facts


def scrape_mars_facts():
    browser = init_browser()
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_table = pd.read_html(mars_facts_url)
    mars_facts_table
    df = mars_facts_table[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)
    df.head()
    html_table = df.to_html()
    # strip unwanted newlines
    html_table_cleaned = html_table.replace('\n', '')
    mars_info['mars_facts'] = html_table_cleaned
    return mars_info
    browser.quit()

# Mars Hemispheres


def scrape_mars_hemispheres():
    browser = init_browser()
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)
    html_mars_hemi = browser.html
    soup = bs(html_mars_hemi, "html.parser")
    soup.find_all('div', class_='item')
    hemispheres = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    main_url = 'https://astrogeology.usgs.gov'

    for e in hemispheres:
        title = e.find('h3').text
        title = title.replace(" Enhanced", "")
        e_url = e.find('a', class_='itemLink product-item')['href']
        browser.visit(main_url + e_url)
        e_html = browser.html
        soup = bs(e_html, 'html.parser')
        img_url = main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    mars_info['hiu'] = hemisphere_image_urls
    return mars_info
    browser.quit()
