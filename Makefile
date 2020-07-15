pip-tools:
	pip install -q pip-tools

deps: pip-tools
	pip-compile -q requirements.in
	pip-sync requirements.txt

devdeps: pip-tools
	pip-compile -q requirements.in
	pip-compile -q dev-requirements.in
	pip-sync requirements.txt dev-requirements.txt

lint:
	flake8 databases

