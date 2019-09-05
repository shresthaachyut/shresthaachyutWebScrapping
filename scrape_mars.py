def scrape():
    from splinter import Browser
    from splinter.exceptions import ElementDoesNotExist
    import numpy as np
    from bs4 import BeautifulSoup
    import pandas as pd
    import requests
    executable_path = {'executable_path': 'Resources/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # 1.1 Scraping News Title and Paragraphs
    url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url1)
    news_title = []
    news_para = []
    for pages in range(10):
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.find_all(class_ = 'content_title')
        paragraphs = soup.find_all(class_ = 'article_teaser_body')
        for title in titles:    
            news_title.append(title.a.text)
        for paragraph in paragraphs:
            news_para.append(paragraph.text)
        try:
            browser.click_link_by_partial_text('MORE')         
        except:
            print("Scraping Complete")
    np_news_title = np.unique(np.array(news_title))
    np_news_para = np.unique(np.array(news_para))

    # 1.2 Get Images JPL Mars Space Images - Featured Image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    featured_image_url = []
    for pages in range(5):
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        url_imgs = soup.find_all(class_ = 'img')
        for url_img in url_imgs:    
            image = url_img.img['src']
            featured_image_url.append('https://www.jpl.nasa.gov' + image)
        try:
            browser.click_link_by_partial_text('Next')
        except:
            print("Scraping Complete")
    np_featured_image_url = np.unique(np.array(featured_image_url))

    # 1.3 Mars Weather
    url3 = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url3)
    soup = BeautifulSoup(response.text, 'html.parser')
    mars_weather = []
    results = soup.find_all('div', class_="js-tweet-text-container")
    for result in results:
        try:
            weather = result.p.text
            mars_weather.append(weather)
        except AttributeError as e:
            print(e)
    mars_weather = mars_weather[1]

    # 1.4 Mars Facts
    url4 = 'https://space-facts.com/mars/'
    marsFacts = pd.read_html(url4)[0]
    marsFacts.drop(columns = 'Earth', inplace = True)
    marsFacts.columns = ['MarsFacts', 'Value']
    marsFacts.head()

    # 1.5 Mars Hemispheres
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    image_url = []
    title = []
    href_container = []

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    href_url_divs = soup.find_all('div', class_ = 'item')
    for div in href_url_divs:
        href_container.append('https://astrogeology.usgs.gov' + div.a['href'])
    for links in href_container:
        try:
            browser.visit(links)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            browser.click_link_by_partial_text('Open')
            img = soup.find('img', class_ = 'wide-image')
            title = soup.find('h2', class_ = 'title')
            print(img)
            image_url.append({'title': title.text.replace(' Enhanced',''),'img_url' : 'https://astrogeology.usgs.gov/' + img['src']})
        except:
            print('scraping complete')

    scrapped = {
        'NewsTitle': np_news_title,
        'NewsParagraps' : np_news_para,
        'FeaturedImages' : np_featured_image_url,
        'Facts': marsFacts,
        'Weather': mars_weather,
        'Hemispheres': image_url
    }
    return(scrapped)

scrape_value = scrape()