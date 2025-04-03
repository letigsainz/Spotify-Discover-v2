import webbrowser
import requests
import json
import logging

logger = logging.getLogger(__name__)

# open app locally
def open_browser():
    try:
        url = 'http://127.0.0.1:5000/'
        webbrowser.open(url)
    except webbrowser.Error as e:
        logger.error(f'An error occurred: {e}')
        logger.info('Try to manually open your browser and navigate to: http://127.0.0.1:5000/')

# shut down the flask server. Note: deprecated in Werkzeug 2.1
def shutdown_server(environ):
    if 'werkzeug.server.shutdown' not in environ:
        raise RuntimeError('Not running the development server')
    environ['werkzeug.server.shutdown']()
    logger.info('Shutting down server...')
