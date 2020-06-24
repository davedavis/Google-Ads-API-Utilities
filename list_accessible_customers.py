#!/usr/bin/env python
# This program contains a single method that receives a ga client and a customer id and returns the list of MCC IDs
# that we have access to (as fully qualified resource names), AND accounts where we've been added as admins directly,
# but not the entire list  or hierarchy of customer IDs. For that, see the get_account_hierarchy file.

import sys
import yaml
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def get_mccs_and_direct_admin_only_accounts(client):
    customer_service = client.get_service('CustomerService', version='v3')

    try:
        accessible_customers = customer_service.list_accessible_customers()

        resource_names = accessible_customers.resource_names
        for resource_name in resource_names:
            print('Customer resource name: "%s"' % resource_name)
    except GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)


# My personal setup.
# Create the client with the YAML file as expected by the Google Ads client.
google_ads_client = GoogleAdsClient.load_from_storage('config/google-ads.yaml')
# Load the YAML file so we can pass it the MCC ID (In this case, the same as the login customer id)
with open('config/google-ads.yaml', 'r') as f:
    # Load the YAML file with SafeLoader (Subset of YAML features) as we don't need full functionality.
    yaml_file = yaml.load(f, Loader=yaml.SafeLoader)

# Finally, call the main method, passing the client we created
get_mccs_and_direct_admin_only_accounts(google_ads_client)
