import csv
import time
import requests
from requests.exceptions import RequestException


def get_county_and_code(county_and_code):
    # As a separate function, we can take each line of the list API response and parse it into a county and code.
    parts = county_and_code.split("-")
    return parts[0].strip(), parts[1].strip()

def check_county(county_and_code, writer):
    county, code = get_county_and_code(county_and_code)
    try:
        result = requests.get(f"https://illinoiscomptroller.gov/constituent-services/local-government/local-government-warehouse/landingpage?code={code}&searchtype=AuditSearch&originalSearchString={county}")
        if "has not supplied its required documentation for the last three fiscal years. No data is available." in result.text:
             writer.writerow([county, code, "false"])
    except RequestException as ex:
        print(f"Timeout on {county} - {code}: \n {ex.response}")
        writer.writerow([county, code, "true"]) # We write the errors too, so we know which counties we had trouble with.


def get_counties():
  result = requests.get("https://illinoiscomptroller.gov/ioc/remoteData?component=Queries%2FLocalGoveWarehouseSearchService&method=getSearchAllLocalUnitsOptionC&term=&_=1732041685267")
  return result.json()

def print_out_bad_counties(file_name):
    counties = get_counties()
    processed_counties = 0 # To keep track of script progress, we can count the number of counties we've processed.
    with open(file_name, "w") as report:
        writer = csv.writer(report, delimiter=',') # If we write to a file, we don't rely on the console to display the data.
        writer.writerow(["County", "Code", "Error"])
        time.sleep(2) # Sleep for 2 seconds to avoid rate limiting
        for county_and_code in counties:
            check_county(county_and_code, writer)
            processed_counties += 1 # Increment the processed counties.
            if processed_counties % 10 == 0:
                print(f"Processed {processed_counties} counties")

if __name__ == "__main__":
    print_out_bad_counties("counties.csv") # We pass in a name to of the file to write to.