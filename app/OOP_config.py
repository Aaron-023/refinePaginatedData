import requests
import json

class Client: 
    """
    This client class instantiates objects for calling data from
    multiple end points
    """
    def __init__(self, name) -> None:
        #instance variables
        self.name = name
        self.base_url = 'https://api.smartrecruiters.com/v1/companies/'
        self.postings = '/postings?offset='
        self.offset = 0

    def __str__(self) -> str:
        return f'Type: Class. This class is used to create client instances'

    # get_url is an instance method
    def get_endpoint_url(self) -> str:
        return f'{self.base_url}{self.name}{self.postings}{self.offset}'
    
    # this is an instance method
    def refine_endpoint_data(self, url, paginated_data=None) -> list:

        while True:
            if paginated_data is None:
                paginated_data = []

            r = requests.get(url) #request reponse obj
            j = json.loads(r.text) #change the response text to a json string

            # if the json's totalfound value is less than the offset value
            if  self.offset < j['totalFound']:

                for item in j['content']:
                    paginated_data.append(item['ref'])

                self.offset += 100
                self.refine_endpoint_data(self.get_endpoint_url(), paginated_data)
            else:
                # n = 0 
                # for item in paginated_data:
                #     print(f'{n} :: {item}')
                #     n += 1
                break
        return paginated_data

    # this is an instance method    
    def process_data(self, data) -> list:

        data_to_write = []

        for url in data: 
            r = requests.get(url) #request reponse obj
            j = json.loads(r.text) #deserialise to a python string
            # jd = json.dumps(j) # serialise to a JSON formatted string
            data_to_write.append(j)

        return data_to_write

    # this is an instance method    
    def save(self, data) -> None:
            json_string = json.dumps(data)

            with open(f'./app/payloads/{self.name}.json', 'w') as file:
                file.write(json_string)