from chicago import Crime, School
from chicago import pull_schools, pull_crimes, degrees_within_miles

def crimes_near_schools():
    schools = pull_schools(1000, 0)
    crimes = pull_crimes(1000, 0)
    for school in schools:
        for crime in crimes:
            if degrees_within_miles(1.0, (school.latitude, school.longitude), (crime.latitude, crime.longitude)):
                print(f"Crime {crime.crime_id} is near school {school.long_name}. School address: {school.address} -- {school.latitude}, {school.longitude}. Crime location: {crime.latitude}, {crime.longitude}.")


# Crime 842 is near school CICS - Washington Park. School address: -87.622068, 41.783617. Crime location: -87.766625355, 41.893629328.