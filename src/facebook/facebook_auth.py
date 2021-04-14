"""
modules for running authentification scripts with FB API
"""

import requests
from datetime import datetime, timedelta
import pandas as pd
import os


def retrieve_long_lived_token(app_id, app_secret, short_lived_token):
    """
    get long lived usr access token
    docs at https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing

    Args:
        app_id (str): FB app id
        app_secret(str): FB app secret key
        short_lived_token(str): short lived token retrieved from Graph API Explorer

    Returns:
        FB API response (dict): request response converted in a json dict
    """

    import requests

    params = (
        (' grant_type', 'fb_exchange_token'),
        (' client_id', app_id),
        (' client_secret', app_secret),
        (' fb_exchange_token', short_lived_token),
    )

    res = requests.get('https://graph.facebook.com/v10.0/oauth/access_token', params=params)
    return res.json()


def store_token(id_dict, long_lived_token_dict, outfile_path='auth/facebooktoken.txt'):
    """
    """
    # prepare dataframe
    auth_dict = {**id_dict,**long_lived_token_dict}
    auth_dict['token_create_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    auth_dict['token_expiry_date'] = (datetime.now() + timedelta(seconds=auth_dict['expires_in'])).strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame.from_dict(auth_dict, orient='index').transpose()

    # append if output file exists
    if os.path.isfile(outfile_path):
        df.to_csv(outfile_path, mode='a', header=False, index=False)
        print('Token data attached to', outfile_path)

    # copy content if no output file yet
    else:
        df.to_csv(outfile_path, index=False)
        print('Token data written to', outfile_path)


def get_latest_token(token_file_oath='auth/facebooktoken.txt'):
    """
    """
    # read in token file
    df = pd.read_csv(token_file_oath)

    # select max expiry date
    latest_expiry_str = df['token_expiry_date'].max()
    latest_expiry_ts = datetime.strptime(latest_expiry_str, '%Y-%m-%d %H:%M:%S')

    # check whether expiry date is not exceeded
    if datetime.now() < latest_expiry_ts:
        access_token = df[df['token_expiry_date'] == latest_expiry_str]['access_token'].values[0]
        return access_token
    else:
        raise ValueError(f'Long lived access token has expired on {latest_expiry_str}. Please retrieve a new one.')

