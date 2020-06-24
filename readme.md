# Setup

1) Get the details required in the google-ads.yaml file. 
2) Download the OAuth json file from the Google console as secret.json.
3) Put them in the /config/ directory.
3) Run the following:

       $  python authenticate_in_standalone_application.py --client_secrets_path=secret.json

This will give the URL to authorize. Complete and get the access token and refresh tokens
and fill in the refresh token in the YAML file. 


# Building the client
When running examples, when building the client, just pass the file path as an 
argument to the load_from_storage() method like this: 

    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient.load_from_storage('/config/google-ads.yaml'))


# Beginner Insights
Things can be broken down into two main use cases. Reporting, and actually managing/editing accounts. 
So far, the code in this repo is only useful for reporting. Particularly for reporting that isn't 
available in the web UI (multi dimensional reports). 

So for every report, we need to query the ga_service.search or ga_service.search_stream methods, passing
it our client and a query. The query is the tricky part as the documentation is not beginner friendly. 
Particularly the view resource that needs to be queried. The FROM clause specifies the main resource that 
will be used to select fields. More details can be found here: https://developers.google.com/google-ads/api/docs/query/structure#from

# Time based reporting
In your GAQL queries, if you want to segment by date (for example, a daily report), you need to include the 
segment.date segment resource in your select statement, not just the where statement.

# Notes

The list_accessible_customers file will only get a list of MCCs you have access to as well as accounts
that you have been added to as an admin directly. Usually, this isn't what you want. I've built a crude 
get_account_hierarchy file that loops through the accounts in your MCC and gives you back the CIDs. This
is most likely what you want. 


# ToDo
Queries with string based where clauses like: 

      "SELECT CampaignName, Clicks, Cost " + //sample metrics
      "FROM CAMPAIGN_PERFORMANCE_REPORT " +
      "WHERE CampaignName CONTAINS '" + names[i] + "'" +
      "DURING THIS_MONTH " //sample date range


Turn this into a package that can be called with easier parameters. 

A predefined ENUM list of GAQL queries to get up and running faster in future


# Potential Use Cases
1) Apply recommendations
2) Check AccountBudgetProposal resource, and compare with ROAS to accept or decline. 
3) Reduce/Increase bids depending on ROAS



# Mappings and Views
A list of logical (Old AWQL) reports and their new mappings in the Google Ads API is here: 
https://developers.google.com/google-ads/api/docs/migration/reports