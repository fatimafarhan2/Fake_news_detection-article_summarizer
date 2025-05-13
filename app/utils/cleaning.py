# in this txt file i will clean my data


import re
from bs4 import BeautifulSoup


def clean_txt(text : str)->str:

    # first remove the html 
    text=BeautifulSoup(text,"html.parser").get_text()
    # convert the text to lower case
    text=text.lower()
    # now we remove any kind of urls
    text=re.sub(r'http\S+|www\S+|https\S+', '', text)
    # only letters and punctuations are to be extracted
    text = re.sub(r'[^a-zA-Z\s.,!?]','',text)

    # remove any futile paces:
    text=re.sub(r'\s+',' ',text).strip()

    return text