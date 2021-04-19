class Client:
    """
    Set a new client object, store it, retrieve it, view it, edit it.
    """

    def __init__(self, name):
        """
        Initiate a new client object by calling its name

        Args:
            - name (str): client name
        
        Returns
            - client object

        Example:
            >>> Client("Best Company Ever Established")
        """
        self.name = name


    def set_new_client(self, locations, home_url, childpages=None, socialmedia_pages=None):
        """
        Set up a new client from user input

        Args:
            - locations (str, list): str or list object of chosen target locations
            - home_url (str): full url of home page address
            - childpages (str, optional): full url of child pages
            - socialmedia_pages (dict, optional): map of social media channel and full url of page
        
        Returns:
            - client object
        
        Example:
            >>> Client.set_new_client(['Eschau','Elsenfeld'], 'https://www.kreativbox.io')
        """
        self.locations = locations
        self.home_url = home_url
        self.childpages = childpages
        self.socialmedia_pages = socialmedia_pages

    
    def _issue_client_id():
        pass
    
    
    def _prepare_dict(self):
        """
        Helper funtion to prepare a dictionary from object instance
        """
        data = [
            {  
                'id': self.id,
                'name': self.name,
                'locations': self.locations,
                'home url': self.home_url,
                'childpages': self.childpages,
                'social media pages': self.socialmedia_pages,
            }
        ]
        return data


    def store_client_data(self, outfile_path='data/client.json'):
        """
        Store changes to client data to database

        Args:
            - outfile_path (str): file path to client.json file
        
        Returns:
            - json file
        
        Example:
            >>> Client.store_client_data()
        """

        import json
        import os

        # prepare a dictionary from client object instance
        data = self._prepare_dict()

        # store data
        if not os.path.isfile(outfile_path):
            # if no client.json data yet, write a new file
            with open(outfile_path, 'w') as fp:
                json.dump(data, fp, indent=4)
        else:
            # read the current client.json file
            with open(outfile_path, 'r') as fr:
                upload = json.load(fr)
                # append data to it
                upload.append(data[0])   
                # write appended data back to file
                with open(outfile_path, 'w') as fw:
                    json.dump(upload, fw, indent=4)


    def retrieve_client_data():
        """
        Retrieve client data from database

        Args:
            - 
        Returbs:
            -
        """
        with open(outfile, 'r') as fr:
            data = json.load(fr)
        return data
        
    
    def view_client_data():
        """
        Represent client data in tabular view
        """
        pass
    
    def edit_client_data():
        """
        Write changes to chosen client data object
        """
        pass
