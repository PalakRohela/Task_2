#!/usr/bin/env python
# coding: utf-8

# In[18]:


import os
import requests
import re


# In[19]:


pip install beautifulsoup4


# In[20]:


from bs4 import BeautifulSoup


# In[23]:


import re
import os
import requests
from bs4 import BeautifulSoup

def get_page(url):
    # Handling possible error - Check if the URL is a valid Medium article URL
    if not re.match(r'https?://medium.com/', url):
        print('Please enter a valid Medium article URL.')
        return None
    
    try:
        # Make an HTTP GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the BeautifulSoup object of the article
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Failed to fetch the article. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>": "\n"}
    rep = dict((re.escape(k), v) for k, v in rep)
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('<(.*?)>', '', text)
    return text

def collect_text(soup, url):
    text = f'url: {url}\n\n'
    para_text = soup.find_all('p')
    for para in para_text:
        text += f"{para.text}\n\n"
    return text

def save_file(text, url):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
    name = url.split("/")[-1]
    fname = f'scraped_articles/{name}.txt'
    
    # Write the file using the 'with' statement
    with open(fname, 'w', encoding='utf-8') as file:
        file.write(text)
    
    print(f'File saved in directory {fname}')

if __name__ == '__main__':
    url = input("Enter the URL of a Medium article: ")
    soup = get_page(url)

    if soup:
        text = collect_text(soup, url)
        save_file(text, url)
    else:
        print("Failed to fetch HTML source text.")


# In[ ]:




