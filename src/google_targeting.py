from googleads import adwords


def load_targeting_locations(client, location_in):
    """
    Args:
        - client
        - location_in (str, list): inputted location name
    Returns:
        -
    """

    # take input location
    if type(location_in) == str:
        loc_in = []
        loc_in.append(location_in)
    elif type(location_in) == list:
        loc_in = location_in
    else:
        raise ValueError(f'location_in value {location_in} is of type {type(location_in)}. We only accept int or list objects.')

    # Initialize appropriate service.
    location_criterion_service = client.GetService('LocationCriterionService', version='v201809')

    # Create the selector.
    selector = {
        'fields': ['Id', 'LocationName', 'DisplayType', 'CanonicalName',
                 'ParentLocations', 'Reach', 'TargetingStatus'],
        'predicates': [{
          'field': 'LocationName',
          'operator': 'IN',
          'values': loc_in
        }, {
          'field': 'Locale',
          'operator': 'EQUALS',
          'values': ['de']
        }]
    }

    # Make the get request.
    return location_criterion_service.get(selector)


def select_target_location(location_criteria, display_type):
    """
    Args:
        - client
        - location_in (str, list): inputted location name
    Returns:
        -
    """
    sel_dict = {}
    for index, i in enumerate(location_criteria):
        if i['location']['displayType'] == display_type:
            sel_dict[index] = {
                'location_name': i['location']['locationName'],
                'location_id': i['location']['id'],
                'location_reach': i['reach'],
            }
    return sel_dict


def prepare_keyword(keyword, is_negative=False, match_type='BROAD'):
    """


    Args:
        - 
    Returns:
        - 
    """
    if not is_negative:
        keyword_estimate_requests = {
            'keyword': {
                'xsi_type': 'Keyword',
                'matchType': match_type,
                'text': keyword
            }
        }
    else:
        keyword_estimate_requests = {
            'keyword': {
                'xsi_type': 'Keyword',
                'matchType': match_type,
                'text': keyword
            },
            'isNegative': 'true'
        }
    return keyword_estimate_requests


def prepare_location(location_ids):
    location_list = [
        {'xsi_type': 'Location', 'id': location_id}
        for location_id in location_ids
    ]
    language = [{'xsi_type': 'Language','id': '1001'}]
    return location_list + language


def load_campaign_estimate(
    client, 
    keyword_estimate_requests, 
    location_criteria, 
    platform_segments=False,
    max_cpc = 1
):
    """
    Args:
        - 
    Returns:
        - 
    """
    
    # Initialize appropriate service.
    traffic_estimator_service = client.GetService(
      'TrafficEstimatorService', version='v201809')

    # Create ad group estimate requests.
    adgroup_estimate_requests = [{
      'keywordEstimateRequests': keyword_estimate_requests,
      'maxCpc': {
          'xsi_type': 'Money',
          'microAmount': str(max_cpc * 1000000) # which is equal to 1 EUR
      }
    }]

    # Create campaign estimate requests.
    campaign_estimate_requests = [{
      'adGroupEstimateRequests': adgroup_estimate_requests,
      'criteria': location_criteria,
    }]

    # Create the selector.
    selector = {
      'campaignEstimateRequests': campaign_estimate_requests,
    }

    # Optional: Request a list of campaign-level estimates segmented by platform.
    selector['platformEstimateRequested'] = platform_segments

    # Get traffic estimates.
    estimates = traffic_estimator_service.get(selector)
    
    return estimates


def _CalculateMean(min_est, max_est):
    if min_est and max_est:
        return (float(min_est) + float(max_est)) / 2.0
    else:
        return None


def _FormatMean(mean):
    if mean:
        return '%.4f' % mean
    else:
        return 'N/A'


def select_campaign_estimates(estimates, keyword_estimate_requests):
    """
    Args:
        -
    Returns:
        -
    """
    campaign_estimate = estimates['campaignEstimates'][0]

    if 'adGroupEstimates' in campaign_estimate:
        ad_group_estimate = campaign_estimate['adGroupEstimates'][0]
        if 'keywordEstimates' in ad_group_estimate:
            keyword_estimates = ad_group_estimate['keywordEstimates']

            keyword_estimates_and_requests = zip(keyword_estimates, keyword_estimate_requests)

            estimates_out = []
            for keyword_tuple in keyword_estimates_and_requests:
                if keyword_tuple[1].get('isNegative', False):
                    continue
                keyword = keyword_tuple[1]['keyword']
                keyword_estimate = keyword_tuple[0]

                min_estimate = keyword_estimate['min']
                max_estimate = keyword_estimate['max']

                mean_avg_cpc = (
                    _CalculateMean(min_estimate['averageCpc']['microAmount'],
                                   max_estimate['averageCpc']['microAmount'])
                    if 'averageCpc' in min_estimate and min_estimate['averageCpc'] 
                    else None
                )
                mean_avg_pos = (
                    _CalculateMean(min_estimate['averagePosition'],
                                   max_estimate['averagePosition'])
                    if 'averagePosition' in min_estimate and min_estimate['averagePosition'] 
                    else None
                )
                mean_clickthrough = _CalculateMean(min_estimate['clickThroughRate'],
                                                  max_estimate['clickThroughRate'])
                mean_clicks = _CalculateMean(min_estimate['clicksPerDay'],
                                             max_estimate['clicksPerDay'])
                mean_impressions = _CalculateMean(min_estimate['impressionsPerDay'],
                                                  max_estimate['impressionsPerDay'])
                mean_total_cost = _CalculateMean(min_estimate['totalCost']['microAmount'],
                                                 max_estimate['totalCost']['microAmount'])
                estimates_dict = {
                    'keyword': keyword['text'],
                    'match_type': keyword['matchType'],
                    'avg_cpc': _FormatMean((mean_avg_cpc/1000000 if mean_avg_cpc else None )),
                    'avg_pos': _FormatMean(mean_avg_pos),
                    'click_through': _FormatMean(mean_clickthrough),
                    'daily_clicks': _FormatMean(mean_clicks),
                    'daily_impressions': _FormatMean(mean_impressions),
                    'daily_cost': _FormatMean((mean_total_cost/1000000 if mean_total_cost else None)),
                }
                estimates_out.append(estimates_dict)
    return estimates_out
