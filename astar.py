import json
from pprint import pprint

pastClass = None;
alreadyTaken = [];


### User input for past classes ###
while True:
    pastClass = input("Enter previously taken class, or 'NONE': ").upper()
    if pastClass == "NONE":
        break
    alreadyTaken.append(pastClass)


### Insert underscore if not in user-inputted string ###
for item in alreadyTaken:
    if '_' not in item:
        alreadyTaken.append(item[:4] + '_' + item[4:])
        alreadyTaken.remove(item)

print("\nClasses already taken:\n", alreadyTaken)

### Loading json ###
f = open('dataJson.json',)
catalog = json.load(f)
f.close()


### Deleting already taken classes from catalog ###
for key, value in catalog.items():
    for item in alreadyTaken:
        try:
            del catalog[key][item]
        except KeyError:
            pass

print("\nRemaining classes to be taken:")
pprint(catalog)
