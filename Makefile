NEW_PYTHONPATH="`pwd`/src:$(PYTHONPATH)"

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

clean:
	@find . -name "*.pyc" -delete


run:
	@echo "Running server in dev mode..."
	PYTHONPATH="$(NEW_PYTHONPATH)" python -m apiglobo.server

gunicorn:
	PYTHONPATH="$(NEW_PYTHONPATH)" gunicorn -b 0.0.0.0:5100 --log-level=DEBUG apiglobo.server:app -w 1

pep8: 
	@echo "Checking PEP8 compliance..."
	@-pep8 src/apiglobo --ignore=E501,E126,E127,E128
