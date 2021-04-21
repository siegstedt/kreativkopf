"""
module for text comprehension
"""

def _read_url_with_selenium(URL):
    pass


def _read_url_with_requests(URL):
    """
    """
    import requests
    
    return requests.get(URL).content
    

def _parse_hrefs_from_html(html):
    """
    """
    from scrapy import Selector
    sel = Selector(text=html)

    # select all links no the first page
    links = sel.xpath('//a/@href').extract()

    # deduplicate
    links = sorted(list(set(links)))

    return links


def childpages_from_page(in_url, try_selenium=False, include_socialmedia=True):
    """
    """
    # read html from url
    if try_selenium:
        html = _read_url_with_selenium(in_url)
    else:
        html = _read_url_with_requests(in_url)
    
    # parse all href links from html
    links = _parse_hrefs_from_html(html)

    # clear noise
    links = [i for i in links if not '/#' in i] # clear all page references
    links = [i for i in links if i[:4] == 'http'] # clear all non-http links
    links = [i for i in links if i != in_url] # clear references to home page

    # extract social media links
    facebook_links = [i for i in links if 'facebook' in i]
    instagram_links = [i for i in links if 'instagram' in i]
    linkedin_links = [i for i in links if 'linkedin' in i]
    socialmedia_links = facebook_links + instagram_links + linkedin_links

    # drop social media links
    childpages = [i for i in links if i not in socialmedia_links]

    if include_socialmedia:
        outdict = [
            {"childpages": childpages},
            {"facebook_links": facebook_links},
            {"instagram_links": instagram_links},
            {"linkedin_links": linkedin_links},
        ]
    else:
        outdict = [
            {"childpages": childpages},    
        ]

    return outdict


def _parse_text_from_html():
    """
    """
    # read the text of the whole page
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html)
    body_raw = soup.get_text()

    # format the text
    import re
    body_raw = re.compile(r"\n").sub(" ", body_raw)
    body_raw = re.compile(r"\t").sub(" ", body_raw)
    body_text = body_raw.strip()

    return body_text


def trim_german_text_to_tokens():
    """
    """

    # manipulate incoming text
    text = text_in
    text = text.lower()

    satzzeichen = [".",",","!","?","-"]
    for i in satzzeichen:
        text = text.replace(i, " ")
    artikel = [
        'ein','eine','einen','kein','keine','keinen','keines','keiner','keinem',
        'der','die','das','dem','den',
        'ich','du','er','sie','es','wir',
        'mich','mir','mein','meine','meiner','meines','meinem','meinen',
        'dich','dir','dein','deine','deiner','deines','deinem','deinen',
        'sich','ihn','ihm','sein','seine','seiner','seines','seinem','seinen',
        'ihr','ihre','ihrer','ihres','ihrem','ihren','ihnen',
        'uns','unser','unsere','unseres','unserem','unseren',
        'wer','wie','was','wen','wem','warum','wo','welche','welcher','welches',
        'dieses','dieser','diese',
    ]
    fuellwoerter = [
        'und','oder','auch','aber','in','im','ins','an','am','ans',
        'um','ums','aus','wie','so','also','weil','für','fürs','nach',
        'vor','vorm','denn','dann','damit','darin','daraus','trotz',
        'trotzdem','sonst','seit','bis','über','unter','auf',
        'mit','dass','als','da','dort',
    ]
    verben = [
        'bin','bist','ist','sind','seid',
        'habe','hast','hat','haben','habt'
    ]

    for i in artikel + fuellwoerter + verben:
        text = text.replace(" "+i+" ", " ")
        
    sonderzeichen = [
        ('ä','ae'),
        ('ü','ue'),
        ('ö','oe'),
        ('ß','ss'),
    ]
    for i,j in sonderzeichen:
        text = text.replace(i, j)
    
    text = text.strip()

# def trim_german_text_to_phrases():

def generate_keywords_from_text():
    pass

def keywords_from_page(url_in):
    pass

# def generate_phrases_from_text():
