# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
#
# app = FastAPI()

# @app.get('/')
# async def root():
#     return {'message': "Hello World"}
import os
import logging
from flask import Flask, render_template, abort, send_file

from typing import List, Dict

LOGGER = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_Formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
console_handler.setFormatter(console_Formatter)
LOGGER.addHandler(console_handler)
LOGGER.setLevel(logging.DEBUG)

BASE_DIR = 'E:/comics_database/'
STATIC_DIR = './static'
THUMBNAILS_DIR = './static/thumbnail'

app = Flask(__name__, static_folder=STATIC_DIR)


def retrieve_thumbnail_for_file(path, file):
    basename, _ = os.path.splitext(file)
    relpath = os.path.relpath(path, BASE_DIR)
    thumbnail_path = os.path.join(THUMBNAILS_DIR, relpath, basename + '.jpg')

    LOGGER.debug(f'Thumbnail requested path : {thumbnail_path}')
    if os.path.exists(thumbnail_path):
        return thumbnail_path
    else:
        return False


def browse_folder(path: str) -> List[Dict[str, str]]:
    """List path directory. This method is equivalent to listdir except that it returns a list of dictionary with keys
    file and thumbnail.

    Parameters
    ----------
    path: str
        path to browse, absolute

    Returns
    -------
    List[Dict[str, str]]
    List of dictionaries with keys file and thumbnail.

    """
    base_path, _ = os.path.split(path)
    base_path = os.path.relpath(base_path, BASE_DIR)

    items = [{'url': base_path, 'label': '..'}]
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        url = os.path.relpath(file_path, BASE_DIR)
        item = None

        if file.endswith('.cbz'):
            item = {'url': url, 'label': file}
            thumbnail_path = retrieve_thumbnail_for_file(path, file)
            LOGGER.debug(f'Thumbnail path : {thumbnail_path}')
            if thumbnail_path:
                item['thumbnail'] = thumbnail_path

        elif os.path.isdir(file_path):
            item = {'url': url, 'label': file}

        if item:
            items.append(item)

    LOGGER.debug(f'[Browse folder] {path} : {items.__str__()}')

    return items


@app.route('/', defaults={'subpath': ''})
@app.route('/<path:subpath>')
def root(subpath):
    LOGGER.debug(f'[ROUTE] Requested subpath : {subpath}')
    abs_path = os.path.join(BASE_DIR, subpath)

    # Return 404 if subpath doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if subpath is a file and serve
    elif os.path.isfile(abs_path):
        return send_file(abs_path)

    else:
        items = browse_folder(abs_path)
        return render_template('files_thumbnail.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
