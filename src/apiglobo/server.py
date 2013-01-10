#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import sys
# DISCLAIMER: Hack Maligno in POC: xGH - viabilizar override da config em diferentes ambientes
from apiglobo import settings
if len(sys.argv) > 1:
    override_settings = __import__(sys.argv[1])
    settings.__dict__.update(override_settings.__dict__)


from apiglobo import schemas, data


app = Flask(__name__)
app.config.from_pyfile("settings.py")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.register_blueprint(schemas.schema_blueprint)
app.register_blueprint(data.data_blueprint)
print(settings.ES_ENDPOINT)
app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
