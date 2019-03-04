import data
import json

print('Food vocabulary')
data.show_people_food_vocabulary()

print('Prepare people')
people = data.load_people()
companies_map = data.companies_map()
people_map = data.people_map()

for p in people:
    augmented = data.prepare_person_document(p, companies_map, people_map)
    print(json.dumps(augmented, indent=4))

