from dotenv import load_dotenv
import requests
import json
import os
import logging

# Load enviroment variables
load_dotenv()

class JobPostingFetcher: 
    """
    The client class instantiates objects that are used to:
    1: Retrieve paginated offset data from an endpoint
    2: Filter that data then retrieve payload data via mutiple endpoints
    3: Write that data to directory as .json
    """
    def __init__(self, name) -> None:
        self.name = name
        self.base_url = os.getenv('BASE_URL')
        self.postings = '/postings?offset='
        self.offset = 0
        self.payload_directory = os.getenv('PAYLOAD_DIRECTORY')
        self.logging_directory = os.getenv('LOGGING_DIRECTORY')

        os.makedirs(self.logging_directory, exist_ok=True)

        logging.basicConfig(
            filename=f'{self.logging_directory}mylogs.log',
            encoding='utf-8', 
            format='%(asctime)s %(message)s', 
            datefmt='%d/%m/%Y %I:%M:%S %p', 
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

    def __str__(self) -> str:
        print(f"DEBUG: __str__() was called for {self.name}")
        return f'Type: Class. This class is used to create client instances'

    def get_endpoint_url(self) -> str:
        """Gets the endpoint url"""
        return f'{self.base_url}{self.name}{self.postings}{self.offset}'
    
    # instance method
    def refine_endpoint_data(self, url, paginated_data=None) -> list:
        """
        refine endpoint data collates offset paginated data
        it then extracts the ad urls and returns that value
        """
        if paginated_data is None:
            paginated_data = []

        while True:

            try:
                r = requests.get(url) #request reponse obj
                j = json.loads(r.text) #change the response text to a json string

            except (requests.ReadTimeout, 
                    requests.ConnectionError, 
                    requests.HTTPError, 
                    json.JSONDecodeError
                ) as err: 

                logging.warning(f'There was a requests error for {self.name} :: {url}The ERROR_is: {err}')
                continue
                        
            if r.status_code == 200 and j["totalFound"] > 0:
                if self.offset < j['totalFound']:
                    
                    for item in j['content']:
                        paginated_data.append(item['ref'])

                    self.offset += 100
                    return self.refine_endpoint_data(self.get_endpoint_url(), paginated_data)
                else:
                    if not paginated_data:
                        return None
                    else: 
                        logging.info(f'Processing {self.name}')
                        return paginated_data
            else:
                return paginated_data

    # instance method    
    def process_data(self, data) -> list:
        """
        This method runs multiple get requests to get
        client ads then returns the data
        """
        data_to_write = []

        for url in data: 
            try:
                r = requests.get(url)
            except (requests.ReadTimeout, 
                    requests.ConnectionError, 
                    requests.HTTPError, 
                    json.JSONDecodeError
                ) as err: 
                
                logging.warning(f'There was a requests error for {self.name} :: {url} The ERROR_is: {err}')
                continue

            if r.status_code == 200: 
                data_to_write.append(json.loads(r.text)) # Deserialize and append in one step

            else:
                logging.warning(f'There was a server error when getting ad {url} for {self.name}')
                continue
        
        # logging.debug(f'Writing {self.name} data to storage')
        return data_to_write
        

    # instance method    
    def save(self, data) -> None:
        json_string = json.dumps(data)
        
        os.makedirs(self.payload_directory, exist_ok=True)

        with open(f'{self.payload_directory}{self.name}.json', 'w') as file:
            file.write(json_string)
            logging.info(f'{self.name} :: Ads {len(data)} :: written to directory\n')