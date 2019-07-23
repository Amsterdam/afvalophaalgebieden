Adreszoeker afval ophaaldagen
==============================

## Usage

Garbage collection days of the city of Amsterdam.
Best used together with our typeahead bag/brk api for addresses and postal code search:
- https://api.data.amsterdam.nl/atlas/typeahead/bag/?q=dam%201 or
- https://api.data.amsterdam.nl/atlas/typeahead/bag/?q=1012JS%201

Is important to complete the search api with a house number to get a "label":"Adres" result list to obtain a proper x,y coordinate.
Then you can get the coordinates from the chosen address URI:
- https://api.data.amsterdam.nl/atlas/typeahead/bag/bag/verblijfsobject/03630003761571/ 

You can use these coordinates in two GET parameters: x and y to get the garbage collection days:
https://api.datapunt.amsterdam.nl/afvalophaalgebieden/search/?x=121394.0&y=487383.0

# Requirements

* Docker-Compose (required)


# Developing
Use `docker-compose up -d database` to start a local postgres database on localhost:5405

Start the services using:

	docker-compose up afvalophaalgebieden

The API should now be available on http://localhost:8095/api/

It accepts two GET parameters: x and y or lat and lon. When given, a search will be executed for these RD  or WGS84 coordinates and all features
 that match those coordinates will be returned as GeoJSON.

## Run import

Run `sh docker-import-db.sh` to recreate tables and import shape files locally.
The used python scripts with necessary arguments can also be found in this file.

## Testing
Run `python tests.py` to run tests.
