# These libraries are included in the Python Standard Library.
from dataclasses import dataclass

# External Libraries. `pip install -r requirements.txt` to install these.
from geopy.distance import geodesic
import requests

@dataclass
class Crime:
  crime_id: str
  case_number: str
  date: str
  block: str
  iucr: str
  primary_type: str
  description: str
  location_description: str
  arrest: bool
  domestic: bool
  beat: str
  longitude: float
  latitude: float

@dataclass
class School:
  school_id: str
  long_name: str
  address: str
  city: str
  state: str
  zip: str
  phone: str
  school_type: str
  latitude: float
  longitude: float  

def degrees_within_miles(miles, origin, destination):
  distance = geodesic(origin, destination).miles
  return distance <= miles

def pull_crimes(limit, offset):
  result = requests.get(f"https://data.cityofchicago.org/resource/crimes.json?$limit={limit}&$offset={offset}&$order=date")
  return [Crime(
      crime_id=crime["id"],
      case_number=crime["case_number"],
      date=crime["date"],
      block=crime["block"],
      iucr=crime["iucr"],
      primary_type=crime["primary_type"],
      description=crime["description"],
      location_description=crime.get("location_description"),
      arrest=crime["arrest"],
      domestic=crime["domestic"],
      beat=crime["beat"],
      longitude=crime.get("longitude"),
      latitude=crime.get("latitude"),
    ) for crime in result.json()]

def pull_schools(limit, offset): 
  result = requests.get(f"https://data.cityofchicago.org/resource/8i6r-et8s.json?$limit={limit}&$offset={offset}&$order=school_id")
  return [School(
    school_id=school["school_id"],
    long_name=school["long_name"],
    address=school["address"],
    city=school["city"],
    state=school["state"],
    zip=school["zip"],
    phone=school["phone"],
    school_type=school["school_type"],
    latitude=school["school_latitude"],
    longitude=school["school_longitude"],
  ) for school in result.json()]
