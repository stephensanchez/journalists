from toilets import Toilet
from toilets import load_toilets

def greeting(person):
    return "Hello " + person

def print_toilets(search_text):
    toilets = load_toilets()
    for toilet in toilets:
        if search_text in toilet.name:
            print(toilet.name)

if __name__ == "__main__":
    print_toilets(search_text="Reserve")