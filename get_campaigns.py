#!/usr/bin/env python
# This program contains a single method that receives a ga client and a customer id and returns all campaigns in
# that customer account.

import sys
import yaml
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def get_campaigns(client, customer_id):
    ga_service = client.get_service('GoogleAdsService', version='v3')

    query = ('SELECT campaign.id, campaign.name FROM campaign '
             'ORDER BY campaign.id')

    # Issues a search request using streaming.
    response = ga_service.search_stream(customer_id, query=query)

    try:
        for batch in response:
            for row in batch.results:
                print(f'Campaign with ID {row.campaign.id.value} and name '
                      f'"{row.campaign.name.value}" was found.')
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)


# Main
google_ads_client = GoogleAdsClient.load_from_storage('config/google-ads.yaml')
with open('config/google-ads.yaml', 'r') as f:
    yaml_file = yaml.load(f, Loader=yaml.SafeLoader)

get_campaigns(google_ads_client, str(yaml_file['login_customer_id']))


