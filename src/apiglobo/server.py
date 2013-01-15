#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response
import sys
# DISCLAIMER: Hack Maligno in POC: xGH - viabilizar override da config em diferentes ambientes
from apiglobo import data, middleware, settings


app = Flask(__name__)
# app.wsgi_app = middleware.LogMiddleware(app)
app.config.from_pyfile("settings.py")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/healthcheck")
def healthcheck():
    return "ok"

if __name__ == '__main__':
    # app.register_blueprint(data.data_blueprint)
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])

