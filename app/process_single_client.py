
from client import Client
from client import logging

def main(task):

    client_name = task

    client = Client(client_name)

    paginated_data = client.refine_endpoint_data(client.get_endpoint_url())
    
    if len(paginated_data) > 0:
        client.save(client.process_data(paginated_data))
    else:
        logging.warning(f'{client.name} has 0 ads. Skipping...')

if __name__ == "__main__":
    main()