# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
#
# app = FastAPI()

# @app.get('/')
# async def root():
#     return {'message': "Hello World"}
import os
from flask import Flask, render_template, abort, send_file
import logging

LOGGER = logging.getLogger()
console_handler = logging.StreamHandler()
console_Formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
console_handler.setFormatter(console_Formatter)
LOGGER.addHandler(console_handler)
LOGGER.setLevel(logging.DEBUG)

BASE_DIR = 'D:/Mes bds'

app = Flask(__name__)


@app.route('/', defaults={'subpath': ''})
@app.route('/<path:subpath>')
def root(subpath):
    # TODO Handle recursive browsing directory ?
    LOGGER.debug(f'Requested subpath : {subpath}')
    abs_path = os.path.join(BASE_DIR, subpath)

    # Return 404 if subpath doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if subpath is a file and serve
    elif os.path.isfile(abs_path):
        LOGGER.debug(f'{abs_path} requested')
        return send_file(abs_path)

    else:
        files = os.listdir(abs_path)
        return render_template('files.html', files=files)


if __name__ == '__main__':
    app.run()
