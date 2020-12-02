install:
	pip-compile requirements/prod.in
	pip-compile requirements/dev.in
	cp requirements/prod.txt requirements.txt
	pip install -r requirements/dev.txt
	pip install -r requirements/prod.txt

