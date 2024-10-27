import csv
from datetime import datetime

from chicago import Crime, School
from chicago import pull_schools, pull_crimes, degrees_within_miles

CRIME_LIMIT = 3000

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

def crimes_near_schools(file_name):
    print(f"Collecting crimes near schools and writing them to {file_name}")
    # There are only ~600 schools in Chicago, so we can pull them all at once.
    schools = pull_schools(1000, 0)
    crimes = collect_all_crimes()

    with open(file_name, "w") as report:
        writer = csv.writer(report, delimiter=',')
        writer.writerow(["School Name", "School Address", "Crime ID", "Crime Latitude", "Crime Longitude"])
        for school in schools:
            found_crimes = 0
            for crime in crimes:
                if degrees_within_miles(1.0, (school.latitude, school.longitude), (crime.latitude, crime.longitude)):
                    writer.writerow([school.long_name, school.address, crime.crime_id, crime.latitude, crime.longitude])
                    found_crimes += 1
            print(f"Found {found_crimes} crimes near {school.long_name}")


def collect_all_crimes():
    crimes = []
    # `while True` is an infinite loop, because "True" is always True. It is important that we `break` a few lines down on a specific condition.
    while True:
        new_crimes = pull_crimes(1000, len(crimes))
        if crimes and compare_string_dates(crimes[-1].date, new_crimes[0].date):
            # This API loops around to the first crimes after we've seen them all. Break when we see the same crimes again.
            break
        crimes.extend(new_crimes)
        print(f"Collected {len(crimes)} crimes")
        if len(crimes) >= CRIME_LIMIT:
            print("Collected enough crimes, raise CRIME_LIMIT if you want more.")
            break
    return crimes

def compare_string_dates(date_str1, date_str2, date_format=ISO_FORMAT):
    date1 = datetime.strptime(date_str1, date_format)
    date2 = datetime.strptime(date_str2, date_format)
    return date1 > date2
