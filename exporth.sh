HOUTDIR=/home/leslie/Documents/
mongoexport --db=hedgehog --collection=activities --jsonArray --out=${HOUTDIR}activities.json
mongoexport --db=hedgehog --collection=courses --jsonArray --out=${HOUTDIR}courses.json
mongoexport --db=hedgehog --collection=people --jsonArray --out=${HOUTDIR}people.json
mongoexport --db=hedgehog --collection=person --jsonArray --out=${HOUTDIR}person.json
mongoexport --db=hedgehog --collection=projects --jsonArray --out=${HOUTDIR}projects.json
mongoexport --db=hedgehog --collection=theses --jsonArray --out=${HOUTDIR}theses.json

