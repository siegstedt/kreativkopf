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


