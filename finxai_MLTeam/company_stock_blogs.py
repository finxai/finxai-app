import requests
from bs4 import BeautifulSoup
import re
import os
import json

response = requests.get("https://stockrow.com/api/companies.json")
companies = response.json()

def get_company_stcok_blogs(company):
  response = requests.get("https://www.cnbc.com/quotes/" + company['ticker']);
  doc = BeautifulSoup(response.text, 'html.parser')
  latest_blogs = doc.find_all("a", {'class': "LatestNews-headline"})

  blogs = []

  for blog in latest_blogs:

    blog_res = requests.get(blog['href']);
    blog_res_doc = BeautifulSoup(blog_res.text, 'html.parser') 
    blog_content = blog_res_doc.find("div", {"class": "PageBuilder-col-9 PageBuilder-col PageBuilder-article"})

    if blog_content:
      blogs.append({
          'company_code': company['ticker'],
          'company_name': company['company_name'],
          'blog_title': blog.text,
          'blog_link': blog['href'],
          'blog_content': str(re.sub('<[^<]+?>', '', str(blog_content)).strip()),
      })

  return blogs;

os.makedirs('data', exist_ok=True)

all_stock_news = []
count = 0
for company in companies:
  count = count + 1
  path = 'data/{}.json'.format(company['ticker'])
  path_empty = 'data/empty/{}.json'.format(company['ticker'])

  if os.path.exists(path) or os.path.exists(path_empty):
    print("The file {} already exists. Skipping...".format(path))
    continue
  news = get_company_stcok_blogs(company)

  if len(news) > 0:
    all_stock_news = all_stock_news + news
    with open(path, 'w') as f:
        json.dump(news, f)
  else:
     with open(path_empty, 'w') as f:
        json.dump(news, f)   
  print("Count", count)

len(all_stock_news)


print(len(companies))

