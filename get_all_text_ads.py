#!/usr/bin/env python
# This program contains a single method that receives a ga client and a customer id and returns an text ad report with
# all text ad fields, spanning multiple search ad formats, including DSAs and RSAs.

import sys
import yaml
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def get_ad_report(client, customer_id):
    ga_service = client.get_service('GoogleAdsService', version='v3')

    # Build the report we want.
    query = ('SELECT campaign.name, ad_group.name, customer.id, '
             'ad_group_ad.ad.expanded_text_ad.headline_part1, '
             'ad_group_ad.ad.expanded_text_ad.headline_part2, '
             'ad_group_ad.ad.expanded_text_ad.headline_part3, '
             'ad_group_ad.ad.expanded_text_ad.description, '
             'ad_group_ad.ad.expanded_text_ad.description2, '
             'ad_group_ad.ad.expanded_dynamic_search_ad.description, '
             'ad_group_ad.ad.expanded_dynamic_search_ad.description2, '
             'ad_group_ad.ad.responsive_search_ad.headlines, '
             'ad_group_ad.ad.responsive_search_ad.descriptions, '
             'metrics.impressions, '
             'metrics.clicks, '
             'metrics.cost_micros, '
             'metrics.ctr '
             'FROM ad_group_ad WHERE campaign.advertising_channel_type = \'SEARCH\' '
             'ORDER BY metrics.impressions DESC '
             'LIMIT 50')

    # Issues a search request using streaming, passing in the query we just built.
    response = ga_service.search_stream(customer_id, query)
    try:
        for batch in response:
            for row in batch.results:
                # Simply prints out the values returned to the console. ToDo: These need to go into a DB or CSV file
                # and a clause for detecting RSA arrays and fill them separately. Right now, they're just dumped
                # to the console as whatever representation they're returned as.
                print(
                    f'Account:                 {row.customer.id.value}',
                    f'Campaign:                {row.campaign.name.value}',
                    f'Headline 1:              {row.ad_group_ad.ad.expanded_text_ad.headline_part1.value}',
                    f'Headline 2:              {row.ad_group_ad.ad.expanded_text_ad.headline_part2.value}',
                    f'Headline 3:              {row.ad_group_ad.ad.expanded_text_ad.headline_part3.value}',
                    f'Ad Description text 1:   {row.ad_group_ad.ad.expanded_text_ad.description.value}',
                    f'Ad Description text 2:   {row.ad_group_ad.ad.expanded_text_ad.description2.value}',
                    f'DSA Description text 1:  {row.ad_group_ad.ad.expanded_dynamic_search_ad.description.value}',
                    f'DSA Description text 2:  {row.ad_group_ad.ad.expanded_dynamic_search_ad.description2.value}',
                    f'RSA Headlines:           {row.ad_group_ad.ad.responsive_search_ad.headlines}',
                    f'RSA Descriptions:        {row.ad_group_ad.ad.responsive_search_ad.descriptions}',
                    f'Cost:                    {row.metrics.cost_micros.value}',
                    f'Impressions:             {row.metrics.impressions.value}',
                    f'Clicks:                  {row.metrics.clicks.value}',
                    f'CTR                      {row.metrics.ctr.value}',
                    # New fStrings need a separator parameter as \n can't be added to the strong without joins.
                    sep='\n')
    except GoogleAdsException as ex:
        print(f'Request with the ID "{ex.request_id}" failed with the status '
              f'"{ex.error.code().name}" and includes the below errors:')
        for error in ex.failure.errors:
            print(f'\tError with the message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn the field: {field_path_element.field_name}')
        sys.exit(1)


# Main. Set up the client and call the get_ad_report method.
google_ads_client = GoogleAdsClient.load_from_storage('config/google-ads.yaml')
with open('config/google-ads.yaml', 'r') as f:
    yaml_file = yaml.load(f, Loader=yaml.SafeLoader)

get_ad_report(google_ads_client, str(yaml_file['login_customer_id']))


