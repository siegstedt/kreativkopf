"""
modules for setting up targeting with FB API
"""

import requests

def load_target_location(access_token, search_query):
    """
    retrieve geographical data for city
    
    Args:
        access_token (str): Graph API access token with appropriate permissions 
        search_query (str): Key word(s) for searching location data
    
    Returns:
        FB API response (dict): request response converted in a json dict
    """

    params = (
        ('location_types', '["city"]'),
        ('type', 'adgeolocation'),
        ('q', search_query),
        ('access_token', access_token),
    )

    res = requests.get('https://graph.facebook.com/v10.0/search', params=params)
    return res.json()


def select_target_location(location_dict, search_query):
    """
    Selects a target location from the generated choices of locations
    
    Args:
        - location_dict: dictionary created by target location load
        - search_query: location search query
    Returns:
        - key value for target location
        - name value for target location
    """
    data = location_dict['data']
    if not data:
        raise ValueError('The inputted data is empty.')

    if len(data) > 1:
        print(f">> Alert! Your input location '{search_query}' created {len(data)} results with FB target location search.")
        print(f">> Options are: {', '.join([i['name']+' ('+i['region']+')' for i in data])}.")
        print(f">> We will pick the first result ('{data[0]['name']}', {data[0]['region']}) as it has the best fit with the input query {search_query}.")
    return data[0]['key'], data[0]['name']


def load_target_interest(access_token, search_query):
    """
    Calls FB API to load interest groups based on a search string
    
    Args:
        access_token (str): Graph API access token with appropriate permissions 
        search_query (str): Key word(s) for searching audience data
    
    Returns:
        FB API response (dict): request response converted in a json dict
    """

    params = (
        ('type', 'adinterest'),
        ('q', search_query),
        ('access_token', access_token),
    )

    res = requests.get('https://graph.facebook.com/v10.0/search', params=params)
    return res.json()


def load_targeting_spec(location_key, location_radius=None, target_interest=None, age_min=None, age_max=None):
    """
    load target
    """
    targeting_spec = {}
    targeting_spec['geo_locations'] = {
        'cities':[
            {'key':key} 
            if location_radius is None 
            else {'key':key,'radius':location_radius,'distance_unit':'kilometer'}
            for key in [location_key]
        ]
    }
    if target_interest is not None:
        targeting_spec['interests'] = target_interest
    if age_min is not None:
        targeting_spec['age_min'] = age_min
    if age_max is not None:
        targeting_spec['age_max'] = age_max
    return targeting_spec


def strip_reach_estimate(reach_cursor_obj):
    """
    Strips the AdAccountReachEstimate Cursor object to reach value
    
    Args:
        reach_cursor_obj (Cursor object): AdAccountReachEstimate Cursor object
    
    Returns:
        reach estimate (int): estimated amount of reached users
    """
    string = str(reach_cursor_obj).replace('\n','').replace(r'<AdAccountReachEstimate>','').replace(' ','')[2:-2]
    return int(string[string.find("users")+7:])