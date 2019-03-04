init:
	pip install virtualenv
	virtualenv hiveryenv
	./hiveryenv/bin/pip install -r requirements.txt

load:
	./hiveryenv/bin/python backend/load_data.py

test:
	./hiveryenv/bin/python -m unittest discover -s backend -p *_test.py