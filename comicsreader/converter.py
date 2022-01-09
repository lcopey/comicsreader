"""This module contains basically function to convert cbr and pdf to cbz format."""

import os
import shutil
import typing

from pyunpack import Archive
from PyPDF4 import PdfFileReader
from zipfile import ZipFile
from PIL import Image
import logging
from typing import Optional, List
from .utils import extensions_check

if typing.TYPE_CHECKING:
    from PyPDF4.pdf import PageObject

log = logging.getLogger(__name__)


def _get_filepath(basename: str, path: str, extension: Optional[str] = '', make_dir: bool = True):
    """Utility function

    Create out directory when make_dir is True and change the basename with the correct extension."""
    if make_dir and not os.path.exists(path):
        os.makedirs(path)
    filename = basename.strip('/').split('.')[0]  # in case of pdf file, name starts with '/'
    return os.path.join(path, filename + extension)


def _extract_image_from_pdf_page(page: 'PageObject', tmp_path: Optional[str] = './tmp/'):
    """Utility function

    Extract image from pdf file, containing 1 image per page (as in comics books). Extract the image without changing
    resolution.
    """
    objects_in_page = page['/Resources']['/XObject'].getObject()
    if len(objects_in_page) == 1:
        # 1 image by page
        for name in objects_in_page.keys():
            obj = objects_in_page[name]
            if obj['/Subtype'] == '/Image':
                # in case of image
                size = (obj['/Width'], obj['/Height'])
                data = obj.getData()
                if obj['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"

                if '/Filter' in obj:
                    if obj['/Filter'] == '/FlateDecode':
                        filepath = _get_filepath(name, tmp_path, extension='.png')
                        img = Image.frombytes(mode, size, data)
                        img.save(filepath)
                    elif obj['/Filter'] == '/DCTDecode':
                        filepath = _get_filepath(name, tmp_path, extension='.jpg')
                        img = open(filepath, "wb")
                        img.write(data)
                        img.close()
                    elif obj['/Filter'] == '/JPXDecode':
                        filepath = _get_filepath(name, tmp_path, extension='.jp2')
                        img = open(filepath, "wb")
                        img.write(data)
                        img.close()
                    elif obj['/Filter'] == '/CCITTFaxDecode':
                        filepath = _get_filepath(name, tmp_path, extension='.tiff')
                        img = open(filepath, "wb")
                        img.write(data)
                        img.close()
                else:
                    filepath = _get_filepath(name, tmp_path, extension='.png')
                    img = Image.frombytes(mode, size, data)
                    img.save(filepath)
            else:
                raise Exception


def _create_cbz_from_tmp_path(out_path, tmp_path):
    basename, _ = os.path.splitext(out_path)
    shutil.make_archive(base_name=basename, format='zip', root_dir=tmp_path)
    os.rename(basename + '.zip', out_path)

    shutil.rmtree(tmp_path)


def _setup_conversion(file: str, out_path: str, allowed_extensions: List[str],
                      tmp_path: Optional[str] = './tmp') -> str:
    extensions_check(file_path=file, allowed_extensions=allowed_extensions)

    in_filename = os.path.basename(file)
    in_dirname = os.path.dirname(file)
    if out_path is None:
        out_path = in_dirname

    out_filepath = _get_filepath(in_filename, path=out_path, extension='.cbz', make_dir=False)
    log.debug(f'Convert {file} to {out_filepath}')

    # Create temp subpath
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)
    os.makedirs(tmp_path)

    return out_filepath


def pdf2cbz(pdf_file: str, out_path: Optional[str] = None, tmp_path: Optional[str] = './tmp'):
    """Convert PDF file to CBZ file.

    It depends on `PyPDF4`_. It extract all images into `./tmp` and the rebuild a zip file based on its content.

    Parameters
    ----------
    pdf_file : str
        subpath of the file to convert. It must have .cbr or .rar extension.
    out_path : Optional[str]
        optionally specify the output subpath
    tmp_path: Optional[str]
        optionnally specify the temporary directory where to store images

    Returns
    -------

    """
    out_filepath = _setup_conversion(pdf_file, out_path=out_path, tmp_path=tmp_path, allowed_extensions=['pdf'])

    # Extract pdf file into temp folder
    log.debug(f'Extract {pdf_file} into {tmp_path}')
    with open(pdf_file, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()
        for n in range(number_of_pages):
            page = pdf.getPage(n)
            _extract_image_from_pdf_page(page, tmp_path=tmp_path)

    # Create cbz file
    log.debug(f'Start writing {out_filepath}')
    _create_cbz_from_tmp_path(out_filepath, tmp_path=tmp_path)
    log.debug(f'Finish writing')


def cbr2cbz(cbr_file: str, out_path: Optional[str] = None, tmp_path: Optional[str] = './tmp'):
    """Convert CBR file to CBZ file.

    It depends on `pyunpack`_. It unpacks the archive into `./tmp` and the rebuild a zip file based on its content.

    Parameters
    ----------
    cbr_file : str
        subpath of the file to convert. It must have .cbr or .rar extension.
    out_path : Optional[str]
        optionally specify the output subpath
    tmp_path: Optional[str]
        optionnally specify the temporary directory where to store images

    Returns
    -------

    """
    out_filepath = _setup_conversion(cbr_file, out_path=out_path, tmp_path=tmp_path,
                                     allowed_extensions=['.cbr', '.rar'])

    # Extract cbr/rar file into temp file
    log.debug(f'Extract {cbr_file} into {tmp_path}')
    Archive(cbr_file, backend='patool').extractall(tmp_path)

    # Create cbz file
    log.debug(f'Start writing {out_filepath}')
    _create_cbz_from_tmp_path(out_filepath, tmp_path=tmp_path)
    log.debug(f'Finish writing')
