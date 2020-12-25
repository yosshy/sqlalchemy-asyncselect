init:
	pip install -r requirements.txt
	pip install -r test-requirements.txt

test:
	black sqlalchemy_asyncselect tests
	nosetests -vv
