import os
import io
import shutil
from zipfile import ZipFile
from PIL import Image


def extract_cbz_first_page(file_path: str):
    """Extract the first image from a cbz archive and returns PIL.Image

    Parameters
    ----------
    file_path: str
        file_path to .cbz file

    Returns
    -------
    Image

    """
    with ZipFile(file_path) as f:
        # Detect first image
        zipped_filename = None
        for zipinfo in f.filelist:
            if zipinfo.filename.endswith('.jpg'):
                zipped_filename = zipinfo.filename
                break

        # Generate thumbnail
        if zipped_filename:
            img_buffer = f.read(zipped_filename)
            img = Image.open(io.BytesIO(img_buffer))
            img.thumbnail((300, 300))

            return img


def erase_thumbnail(root_path):
    """Remove all .thumbnail folder within root_path

    Parameters
    ----------
    root_path: str
    """
    # for dirpath, dirnames, filenames in os.walk(root_path):
    #     _, current_dir = os.path.split(dirpath)
    #     if current_dir == '.thumbnail':
    #         shutil.rmtree(dirpath)
    shutil.rmtree('./comicsreader/static/thumbnail')


def build_thumbnail(root_path, output_path='./comicsreader/static/thumbnail'):
    """Build the .thumbnail folder for each subfolder containing .cbz files

    Parameters
    ----------
    root_path: str

    Returns
    -------

    """
    for dirpath, dirnames, filenames in os.walk(root_path):
        for file in filenames:
            if file.endswith('.cbz'):
                file_path = os.path.join(dirpath, file)
                img = extract_cbz_first_page(file_path)

                # Get filename
                if img:
                    basename, _ = os.path.splitext(file)
                    # _, ext = os.path.splitext(zipped_filename)
                    # miniature_path = os.path.join(dirpath, '.thumbnail')
                    miniature_path = os.path.relpath(dirpath, root_path)
                    miniature_path = os.path.join(output_path, miniature_path)

                    miniature_file_path = os.path.join(miniature_path, basename + '.jpg')

                    # Save
                    if not os.path.exists(miniature_path):
                        os.makedirs(miniature_path)
                    img.save(miniature_file_path)
