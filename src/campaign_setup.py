class CampaignSetup:
    """
    Set up the campaign by taking input infos and mapping it to client auth data
    """

    def __init__(self, campaign_name):
        self.campaign_name = campaign_name

    def read_input(
        self,
        company_name,
        company_desc,
        company_keywords,
        product_name,
        product_desc,
        product_keywords,
        persona_name,
        persona_desc,
        persona_keywords,
        campaign_desc,
        campaign_keywords,
        campaign_location,
        campaign_expense,
        campaign_time_start,
        campaign_time_end,
    ):
        """
        read in the input provided by the user
        """
        self.company_name = company_name
        self.company_desc = company_desc
        self.company_keywords = company_keywords
        self.product_name = product_name
        self.product_desc = product_desc
        self.product_keywords = product_keywords
        self.persona_name = persona_name
        self.persona_desc = persona_desc
        self.persona_keywords = persona_keywords
        self.campaign_desc = campaign_desc
        self.campaign_keywords = campaign_keywords
        self.campaign_location = campaign_location
        self.campaign_expense = campaign_expense
        self.campaign_time_start = campaign_time_start
        self.campaign_time_end = campaign_time_end

    # def map_input():
    # """map input data against older campaigns and try to retrieve information on missing values"""

    # def get_auth():
    #


    # def set_new_client():
    # def read_client():

    # def set_new_campaign():
    # def read_campaign():
    # 