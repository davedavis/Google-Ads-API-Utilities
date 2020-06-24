#!/usr/bin/env python
# This program contains a single method that takes a ga client object and an MCC ID from the YAML
# file and returns a list of customers in the hierarchy by using the
# customer_client_link service:
# https://developers.google.com/google-ads/api/fields/v2/customer_client_link#customer_client_link.client_customer

import sys
import yaml

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def get_hierarchy(client, customer_id):
    ga_service = client.get_service('GoogleAdsService', version='v3')

    query = "SELECT customer_client_link.client_customer FROM customer_client_link"

    # Issues a search request using streaming.
    response = ga_service.search_stream(customer_id, query)

    try:
        for batch in response:
            for row in batch.results:
                # row.customer_client_link.client_customer contains additional trailing and leading text, but is
                # non-subscriptable so we need to cast it directly then slice the result.
                customer = str(row.customer_client_link.client_customer)
                # Remove the sliding to get the full resource name.
                print(customer[18:-2])

    # Required boilerplate API exception block.
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)


# My personal setup.
# Create the client with the YAML file as expected by the Google Ads client.
google_ads_client = GoogleAdsClient.load_from_storage('config/google-ads.yaml')
# Load the YAML file so we can pass it the MCC ID (In this case, the same as the login customer id)
with open('config/google-ads.yaml', 'r') as f:
    # Load the YAML file with SafeLoader (Subset of YAML features) as we don't need full functionality.
    yaml_file = yaml.load(f, Loader=yaml.SafeLoader)

# Finally, call the main method, passing the client we created and a string representation of the account ID
get_hierarchy(google_ads_client, str(yaml_file['login_customer_id']))

