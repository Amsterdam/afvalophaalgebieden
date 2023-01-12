.PHONY: install
install:
	pip install wheel
	pip install -r requirements.txt

.PHONY: sync
sync:
	pip-sync requirements.txt

.PHONY: requirements
requirements: requirements.in
	pip-compile -v --generate-hashes --output-file requirements.txt requirements.in

.PHONY: upgrade
upgrade:
	pur -r requirements.in
	pip-compile -v --upgrade --output-file requirements.txt requirements.in

.PHONY: test
test:
	 python afvalophaalgebieden/tests.py
