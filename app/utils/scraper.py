# import requests
import trafilatura
import json
# import newspaper3k
# from bs4 import BeautifulSoup


#  this is a function whihc willfetch the webpage
# def fetch_pg(url):
#     response=requests.get(url)
#     if response == 200:
#         return response.content
#     else:
#         return None

# web scraping
def scrape_article_content(url):
    page_content=trafilatura.fetch_url(url)
    if page_content:
        result=trafilatura.extract(
            page_content,
            output_format='json',
            with_metadata=True,
            include_comments=False,
            include_tables=False,
            include_images=False)
        if result:
            return json.loads(result)
    return None

# output_format='json': gives you title, author, date, and text
# safe_json_loads: converts it into a usable Python dict
# include_comments=False, include_tables=False: to keep content clean



    # soup=BeautifulSoup(page_content,'html.parser')
    # article_body=soup.find('main')
    # if not article_body:
    #     article_body = soup.find('article')

    # if article_body:
    #     return article_body.get_text(strip=True)
    # return None




#  web crawling part :
# def extract_article_links(hmpg_cont):
#     # parser is an engine which takes html and cnverts in structured manner
#     soup=BeautifulSoup(hmpg_cont,'html.parser')

# # /* Takes this:<html><body><p>Hello!</p></body></html>
# #  Converts to structure form that we can work with easily like:soup.find(p).text  */
    
#     # Now to extract links:
#     links=[]
#     for a_tag in soup.find_all('a',href=True):