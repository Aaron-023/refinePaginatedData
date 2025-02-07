import json
import logging
from jobPostingFetcher import JobPostingFetcher
from filteredJobFetcher import FilteredJobFetcher

def fetch_standard_jobs(client_name): 
    """Processing a single client using the appropriate class."""
    client = JobPostingFetcher(client_name)

    paginated_data = client.refine_endpoint_data(client.get_endpoint_url())
    
    if len(paginated_data) > 0:
        client.save(client.process_data(paginated_data))
    else:
        logging.warning(f'{client.name} has 0 ads. Skipping...')    

def fetch_filtered_jobs(client_name, custom_fields):
    """Processes a client that includes custom fields using the child class."""
    for custom_field_name, custom_field_id in custom_fields.items():
        client = FilteredJobFetcher(client_name, custom_field_name, custom_field_id)

        paginated_data = client.refine_endpoint_data(client.get_endpoint_url())

        if len(paginated_data) > 0:
            client.save(client.process_data(paginated_data))
        else:
            logging.warning(f'{client.custom_field_name} has 0 ads. Skipping...')   

def main():
    
    with open('/Users/aaroncrawford/Documents/Work/AaronTech/SmartRecruiters/vault/credentials.json', 'r') as file:
        all_client_credentials = json.load(file)

    """Process all clients"""
    for client_name, credentials in all_client_credentials.items():
        fetch_standard_jobs(client_name)

    """Process all clients that include the custom_filter key in credentials.json"""
    for client_name, credentials in all_client_credentials.items(): 
        if "custom_field" in credentials: # Check for custom fields
            fetch_filtered_jobs(client_name, credentials["custom_field"])

if __name__ == "__main__":
    main()