VENV = hiveryenv
VENV_BIN = ./$(VENV)/bin

initenv:
	@if [ -d ./$(VENV) ];	\
	then \
        echo "$(VENV) virtual env already exists"; \
	else \
		echo "Creating $(VENV) virtual env"; \
		pip install virtualenv; \
		virtualenv $(VENV); \
		$(VENV_BIN)/pip install -r requirements.txt; \
    fi

installdeps:
	$(VENV_BIN)/pip install -r requirements.txt

init: initenv installdeps

load:
	$(VENV_BIN)/python backend/load_data.py

test:
	$(VENV_BIN)/python -m unittest discover -s backend -p *_test.py

run:
	FLASK_APP=backend $(VENV_BIN)/python -m flask run