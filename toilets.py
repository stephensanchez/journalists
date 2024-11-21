from dataclasses import dataclass
import csv

@dataclass
class Toilet:
  facility_id: str
  url: str
  name: str
  facility_type: str
  address: str
  town: str
  state: str

def load_toilets():
  with open("toilets.csv") as toilets:
    toilet_data = csv.reader(toilets, delimiter=",")
    return [Toilet(toilet[0], toilet[1], toilet[2], toilet[3], toilet[4], toilet[5], toilet[6]) for toilet in toilet_data]