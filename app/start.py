import requests
import json

import config # customer data

def write_file(data, brand): 
    json_string = json.dumps(data)

    with open(f'./payloads/{brand}.json', 'w') as file: 
        file.write(json_string)


def get_target_data(urls, brand) -> None:
    target_data = []
    
    for url in urls:
        json_response = requests.get(url)
        json_text = json_response.text
        json_data = json.loads(json_text)

        target_data.append(json_data)

        write_file(target_data, brand)


def paginated_data(url) -> None:
    page_offset = 0
    data = []

    while True:
        json_response = requests.get(f'{url}?offset={page_offset}')
        json_text = json_response.text
        json_data = json.loads(json_text)

        data.extend(json_data.get('content', []))

        if json_data['totalFound'] <= json_data['offset']: 
            return data

        page_offset += 100


def refine_paginated_data(brands, endPoint) -> None:

    for brand in brands:
        url = f'{endPoint}{brand}/postings'
        postings_data = paginated_data(url)

        if not postings_data: 
            print(f'No data found for brand: {brand}')
            continue

        job_refs = []

        for item in postings_data:
            job_ref = item.get("ref")
            if job_ref:
                job_refs.append(job_ref)
            else:
                print(f'Missing "ref" key in data for brand: {brand} item: {item}')

        get_target_data(job_refs, brand)


refine_paginated_data(config.brands, config.endPoint)