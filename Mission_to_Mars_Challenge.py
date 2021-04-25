#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


## Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# code 'div.list_text' pinpoints the <div /> tag with the class of list_text
slide_elem


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
# We have created a new variable for the title, added the get_text() method, 
# and we’re searching within the parent element for the title.
news_title = slide_elem.find('div', class_='content_title').get_text()
#news_title = slide_elem.find('div', {'class': 'content_title'}).get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
#news_p = slide_elem.find("div", {'class': 'article_teaser_body'}).get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base url to create an absolute url
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


#creating a new DataFrame from the HTML table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()
#Here, we assign columns to the new DataFrame for additional clarity.
df.columns=['description', 'Mars', 'Earth']
#turning the Description column into the DataFrame's index,  updated index will remain in place
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# In[15]:


#browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[16]:


# 1. Use browser to visit the URL
base_url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/'
url= f"{base_url}index.html"
browser.visit(url)


# In[17]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
html_soup = soup(html, 'html.parser')
products_item = html_soup.find_all('a', class_='itemLink',href=True)
#products_item
for item in products_item:
    hemispheres = {}
    item_link = item['href']
    if not item.get_text() and item_link != '#':
        hemisphere_url = f"{base_url}{item_link}"
        browser.visit(hemisphere_url)
        html2 = browser.html
        html_soup2 = soup(html2, 'html.parser')
        #print(html_soup)
        image_title= html_soup2.find('h2', class_='title').get_text()
        image_link = html_soup2.find('img', class_='wide-image').get('src')
        #print(image_title)
        #print(image_link)
        hemispheres = dict([("img_url", f"{base_url}{image_link}"), ("title", image_title)])
        hemisphere_image_urls.append(hemispheres)


# In[18]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[19]:


# 5. Quit the browser
browser.quit()

