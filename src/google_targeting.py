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


