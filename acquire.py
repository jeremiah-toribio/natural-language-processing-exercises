# parser
from bs4 import BeautifulSoup
# data
import pandas as pd
import numpy as np
# requests
import requests
import os
# random
import random
# error ignore
import contextlib

# headers Will now return a random agent
user_agents = [
  "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
  "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
  "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
  'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36,gzip(gfe)']
random_user_agent = random.choice(user_agents)
headers = {'User-Agent': random_user_agent}


# acquire inshort df
def get_inshorts():
    '''
    Iterably retrieves the Business, Technology, Sports & Entertainment portion of inshorts articles.
    '''
    base_url = 'https://inshorts.com/en/read/'
    categories = ['business','technology','sports','entertainment']
    soups = []
    articles = []

    # retrieving the soup blurbs from url cycling for category subpage
    for u in categories:
        url = base_url + u
        # randomized user agents along with our iterated urls
        response = requests.get(url, headers= headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        soups.append(soup)
        print(f'Saving soup for: {url}')

    # looping through soups with their respective category
    for s, cat in zip(soups, categories):
            headline = s.find_all('span', attrs={'itemprop':'headline'})
            body = s.find_all('div', attrs={'itemprop':'articleBody'})
            for i, h in enumerate(headline):
                # h is unused just needed the enumaration to iterate and count
                print(f'Appending {cat} website {i}th headline / body')
                articles.append({'title': headline[i].text, 'category': cat, 'body': body[i].text})
                print(f'{headline[i].text}, {body[i].text}\n\n+ + + + + + + + + +\n')

    articles_df = pd.DataFrame(articles)
    return articles_df
            
        
    
# get codeup function

def get_codeup():
    '''
    Returns codeup blog articles.
    '''
    # retrieving blog names as list
    blog_dict = {}
    # url/ response/ soup
    url = 'https://codeup.edu/blog/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    blog_titles = soup.select('h2')
    list_blog = list(blog_titles)

    for i,blog in enumerate(list_blog):
    # ignore IndexError for aesthetics
        with contextlib.suppress(IndexError):
        # extracting titles of blogs
            t = blog_titles[i].text
            # list comprehension to retrieve urls
            urls = [title.a['href'] for title in blog_titles if title.a]
            url = urls[i]
            blog_dict.__setitem__(t,url)

    # setting df
    codeup_blog = pd.DataFrame([blog_dict]).T.reset_index().rename(columns={'index':'title',0:'url'})

    # now that it has been determined that the content of every blog post is within the same schema, run a for loop to save it all -- could probably be done in a function
    read = []
    for url in codeup_blog['url']:
        print(f'This is the URL USED: {url}')
        response = requests.get(url, headers= headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('p', class_='entry-content')

        # pulling every line
        for i, c in enumerate(content):
            word = content[i].text
            read.append(word)

    # manually setting every description for post - yes there is a better way
    article1 = read[0:26]
    article2 = read[38:45]
    article3 = read[57:65]
    article4 = read[77:83]
    article5 = read[95:101]
    article6 = read[113:121]

    # article body list
    blog_content = [article1,article2,article3,article4,article5,article6]

    # body content column
    codeup_blog['content'] = blog_content
    codeup_blog.content = codeup_blog.content.astype(str)

    return codeup_blog