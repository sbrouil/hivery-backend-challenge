VENV = hiveryenv
VENV_BIN = ./$(VENV)/bin
APP_NAME=backend

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

load:
	FLASK_APP=$(APP_NAME) $(VENV_BIN)/python -m flask load_data

install: initenv installdeps load

test:
	$(VENV_BIN)/python -m unittest discover -s $(APP_NAME) -p *_test.py

run:
	FLASK_APP=$(APP_NAME) $(VENV_BIN)/python -m flask run