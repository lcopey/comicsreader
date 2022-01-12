# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
#
# app = FastAPI()

# @app.get('/')
# async def root():
#     return {'message': "Hello World"}
import os
import logging
import base64
from flask import Flask, render_template, abort, send_file, url_for, redirect
from comic import Comic

from typing import List, Dict


def config_logger(app: Flask):
    app.logger.setLevel(logging.DEBUG)
    for h in app.logger.handlers:
        app.logger.removeHandler(h)

    console_handler = logging.StreamHandler()
    console_Formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    console_handler.setFormatter(console_Formatter)
    console_handler.setLevel(logging.DEBUG)

    app.logger.addHandler(console_handler)
    app.logger.debug(f'[config_logger] - logger handlers : {app.logger.handlers}')
    return app.logger


def get_path_relative_to_file(file: str, *args: str) -> str:
    """Return path relative to file provided

    Parameters
    ----------
    file : str
        path to current file
    args : str
        additional path to join on

    Returns
    -------
    str
        path relative to file
    """
    return os.path.join(os.path.dirname(file), *args)


BASE_DIR = 'E:/comics_database/'
STATIC_DIR = './static/'
THUMBNAILS_DIR = './static/thumbnail/'

app = Flask(__name__, static_folder=STATIC_DIR)
app.comics = {}
LOGGER = config_logger(app)


def retrieve_thumbnail_for_file(path, file):
    basename, _ = os.path.splitext(file)
    relpath = os.path.relpath(path, BASE_DIR)
    thumbnail_path = os.path.join(THUMBNAILS_DIR, relpath, basename + '.jpg')

    path_exists = os.path.exists(thumbnail_path)
    LOGGER.debug(f'Thumbnail requested path : {thumbnail_path}, {path_exists}')
    if path_exists:
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

    items = [{'url': base_path, 'label': '', 'thumbnail': './static/icons/back.png'}]
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        url = os.path.relpath(file_path, BASE_DIR)
        item = None

        if file.endswith('.cbz'):
            label, _ = os.path.splitext(file)
            item = {'url': url, 'label': label}

        elif os.path.isdir(file_path):
            item = {'url': url, 'label': file}

        thumbnail_path = retrieve_thumbnail_for_file(path, file)
        if thumbnail_path:
            item['thumbnail'] = thumbnail_path

        if item:
            items.append(item)

    LOGGER.debug(f'[Browse folder] {path} : {items.__str__()}')

    return items


def open(file, keystore):
    # comic = ZipFile(file)
    comic = Comic(file)

    # extract_path = os.path.join('./static/comic/', basename)
    # comic.extractall(extract_path)
    app.comics[keystore] = comic


@app.route('/open/<path:file>/<int:page>')
def comic_page(file, page):
    img_data = base64.b64encode(app.comics[file].page(page)).decode('utf-8')
    return render_template('reader.html', title=file, img_data=img_data)


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
        _, basename = os.path.split(abs_path)
        basename, _ = os.path.splitext(basename)
        open(abs_path, basename)

        return redirect(url_for('comic_page', file=basename, page=0))

    else:
        items = browse_folder(abs_path)
        return render_template('browser.html', items=items)


if __name__ == '__main__':
    app.config.update(TEMPLATES_AUTO_RELOAD=True)
    app.run(debug=True)
