Adreszoeker afval ophaaldagen
==============================

Adreszoeker afval ophaaldagen

# Requirements

* Docker-Compose (required)


# Developing
Use `docker-compose` to start a local database.

	(sudo) docker-compose start

or

	docker-compose up

The API should now be available on http://localhost:8000/

It accepts two GET parameters: x and y. When given, a search will be executed for these RD coordinates and all features
 that match those coordinates will be returned as GeoJSON.

## Run import
Run `python import.py` to recreate tables and import shape files.


## Testing
Run `bash test.sh` to run tests.
