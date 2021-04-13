"""
prepare input data for further processing
"""

from gensim.summarization import keywords
import pandas as pd
from fuzzywuzzy import process

def generate_keywords_from_text(text_in, nr_kw_out=10):
    """
    Generate a list of keywords from text input with the help of the gensim library

    Find more information in the docs:
    https://radimrehurek.com/gensim_3.8.3/summarization/keywords.html

    Args:
        - text_in (str): input text as string
        - nr_kw_out (int): number of outputted keywords

    Returns:
        - list of str objects and scores
    """

    # manipulate incoming text
    text = text_in
    text = text.lower()

    satzzeichen = [".",",","!","?","\n","-"]
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
    ]
    fuellwoerter = [
        'und','oder','auch','aber','in','im','ins','an','am','ans',
        'um','ums','aus','wie','so','also','weil','für','fürs','nach',
        'vor','vorm','denn','dann','damit','darin','daraus','trotz',
        'trotzdem','sonst','seit','bis','über','unter','auf'
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

    # call gensim function
    outlist = keywords(text, words = nr_kw_out, scores = True, lemmatize = True, split = True)

    # transform results list
    outlist_flat = []
    for i,j in outlist:
        for ii in i.split(" "):
            keyword_score_tuple = (ii,j)
            outlist_flat.append(keyword_score_tuple)
    
    return outlist_flat


def generate_market_from_location(location_in, location_scope='gemeindename', location_radius=0, break_down=False):
    """
    generate population of market given the location and scope

    Args:
        - location_in (str, list): inputted location name
        - location_scope (str, optional): 'kreis', 'vb', or default value 'gemeindename'
        - location_radius (int, optional): radius in km for searching locations, default value is 0
        - break_down (bool, optional): breaks down output in 'gemeindename' and total pop by gender

    Returns:
        - local population data as dict, or pd.DataFrame object if break_down=True
    """

    # match location input data
    loc_list, location_scope = match_location(location_in, location_scope)

    # read gvd data as geography input
    filepath = "data/processed/gv100ad.csv"
    geo = pd.read_csv(filepath)

    # return population values
    if break_down == True:
        population_df = geo[geo[location_scope].isin(loc_list)].groupby("gemeindename").agg(
            {
                'bev_gesamt': 'sum',
                'bev_maennl': 'sum',
                'bev_weibl': 'sum',
            }
        ).sort_values("bev_gesamt", ascending=False).reset_index()
        return population_df
    else:
        population_int = geo[geo[location_scope].isin(loc_list)]['bev_gesamt'].sum()
        population_dict = {
            'location_name': loc_list[0],
            'location_scope': location_scope,
            'location_radius': location_radius,
            'total_population': population_int,
        }
        return population_dict


def match_location(location_in, location_scope='gemeindename'):
    """
    get a matched location name from gemeindeverzeichnis database

    Args:
        - location_in (str, list): inputted location name
        - location_scope (str, optional): 'kreis', 'vb', or default value 'gemeindename'

    Returns:
        - location name as list
        - lcoation_scope if checks passed
    """

    # take input location
    if type(location_in) == str:
        loc_in = []
        loc_in.append(location_in)
    elif type(location_in) == list:
        loc_in = location_in
    else:
        raise ValueError(f'location_in value {location_in} is of type {type(location_in)}. We only accept int or list objects.')  

    # take input scope
    if location_scope in ['kreis','vb','gemeindename']:
        pass
    else:
        raise ValueError(f"location_scope must be either 'kreis', 'vb', or 'gemeindename'. Given value is '{location_scope}'.")

    # read gvd data as geography input
    filepath = "data/processed/gv100ad.csv"
    geo = pd.read_csv(filepath)

    # fuzzy match location input
    location_options = list(geo[location_scope].unique())
    loc_list = []
    for location_name in loc_in:
        if location_name in location_options:
            literal_match = [i for i in location_options if i == location_name]
            loc_list.append(literal_match[0])
        else:
            print(f">> Alert: The location name '{location_name}' does not match literally with our {location_scope} database.")
            match_tuple = process.extractOne(location_name, location_options)
            print(f">> Alert: We were able to retrieve the value '{match_tuple[0]}' with an accuracy of {match_tuple[1]} of 100 points.")
            loc_list.append(match_tuple[0])

    return loc_list, location_scope