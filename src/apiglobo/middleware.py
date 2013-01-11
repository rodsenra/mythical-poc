# coding: utf-8
import logging
import sys
import traceback
from logging.handlers import WatchedFileHandler
from simplejson import dumps

from apiglobo import settings


HEADER_JSON = {"content-type": "application/json"}


def create_logger(filename=settings.LOG_FILE, level=settings.LOG_LEVEL, name=settings.LOG_NAME):
    # WatchedFileHandler watches the file it is logging to.
    # If the file changes, it is closed and reopened using the file name.
    file_handler = WatchedFileHandler(filename)
    file_handler.setLevel(level)
    logger = logging.getLogger(name)
    logger.addHandler(file_handler)

    logger.setLevel(level)
    return logger


class LogMiddleware(object):
    """
    WSGI middleware for logging exceptions during requests.
    """

    def __init__(self, app):
        self.app = app
        self.logger = create_logger()  # get_logger()

    # Based on http://flask.pocoo.org/docs/reqcontext/
    def __call__(self, environ, start_response):
        with self.app.request_context(environ) as context:
            method = context.request.method
            url = context.request.url
            try:
                response = self.app.full_dispatch_request()
            except BaseException:
                error_msg = self._log_error(url, method)
                error_json = dumps({"error": error_msg})
                response = self.app.make_response((error_json, 500, HEADER_JSON))
            else:
                self.logger.info("Request '%s' [%s]" % (url, method))

            return response(environ, start_response)

    def _log_error(self, url, method):
        etype, value, tb = sys.exc_info()
        error_msg = ''.join(traceback.format_exception(etype, value, tb))
        self.logger.error("Request '%s' [%s]\n%s" % (url, method, error_msg))
        return error_msg
