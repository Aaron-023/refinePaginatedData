import os
import json
import logging
from jobPostingFetcher import JobPostingFetcher as Parent

class FilteredJobFetcher(Parent): 
    def __init__(self, name, custom_field_name, custom_field_id):
        super().__init__(name)
        self.custom_field_name = custom_field_name
        self.custom_field_id = custom_field_id

    def get_endpoint_url(self):
        return f"{super().get_endpoint_url()}&custom_field.{self.custom_field_id}"
    
    def save(self, data) -> None:
        """Overrides save method in parent class to use custom_field_name as the filename"""

        json_string = json.dumps(data)
        
        os.makedirs(self.payload_directory, exist_ok=True)

        with open(f'{self.payload_directory}{self.custom_field_name}.json', 'w') as file:
            file.write(json_string)
            logging.info(f'{self.custom_field_name} :: Ads {len(data)} :: written to directory\n')