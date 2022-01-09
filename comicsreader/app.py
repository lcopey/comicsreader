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

BASE_DIR = 'E:/comics_database/'

app = Flask(__name__)


def has_thumbnail(path) -> bool:
    return os.path.exists(os.path.join(path, '.thumbnail'))


def retrieve_thumbnail_for_file(path, file):
    basename, _ = os.path.splitext(file)
    thumbnail_path = os.path.join(path, '.thumbnail', basename + '.jpg')
    if os.path.exists(thumbnail_path):
        return thumbnail_path
    else:
        return False


def browse_folder(path: str):
    items = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        item = None

        if file.endswith('.cbz'):
            item = {'file': file}
            thumbnail_path = retrieve_thumbnail_for_file(path, file)
            if thumbnail_path:
                item['thumbnail'] = thumbnail_path

        elif os.path.isdir(file_path):
            item = {'file': file}

        if item:
            items.append(item)

    return items


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
        items = browse_folder(abs_path)
        return render_template('files_thumbnail.html', items=items)


if __name__ == '__main__':
    app.run()
