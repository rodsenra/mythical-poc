NEW_PYTHONPATH="`pwd`/src:$(PYTHONPATH)"

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

clean:
	@find . -name "*.pyc" -delete


run:
	@echo "Running server in dev mode..."
	PYTHONPATH="$(NEW_PYTHONPATH)" python -m apiglobo.server

pep8: 
	@echo "Checking PEP8 compliance..."
	@-pep8 src/apiglobo --ignore=E501,E126,E127,E128
