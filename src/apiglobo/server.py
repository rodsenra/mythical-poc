#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response
import sys
# DISCLAIMER: Hack Maligno in POC: xGH - viabilizar override da config em diferentes ambientes
from apiglobo import middleware, settings


if len(sys.argv) > 1:
    override_settings = __import__(sys.argv[1])
    settings.__dict__.update(override_settings.__dict__)


from apiglobo import data


app = Flask(__name__)
app.wsgi_app = middleware.LogMiddleware(app)
app.config.from_pyfile("settings.py")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/healthcheck")
def healthcheck():
    return "ok"

app.register_blueprint(data.data_blueprint)
app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
