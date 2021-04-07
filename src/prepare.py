"""
prepare input data for further processing
"""

from gensim.summarization import keywords


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
        'mir','mein','meine','meiner','meines','meinem','meinen',
        'dir','dein','deine','deiner','deines','deinem','deinen',
        'ihn','ihm','sein','seine','seiner','seines','seinem','seinen',
        'ihr','ihre','ihrer','ihres','ihrem','ihren','ihnen',
        'uns','unser','unsere','unseres','unserem','unseren',
    ]
    fuellwoerter = [
        'und','oder','auch','aber','in','im','ins','an','am','ans',
        'um','ums','aus','wie','so','also','weil','für','fürs','nach',
        'vor','vorm','denn','dann','damit','darin','daraus','trotz',
        'trotzdem','sonst','seit','bis'
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