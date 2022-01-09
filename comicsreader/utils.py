import os
from typing import Iterable


def extensions_check(file_path: str, allowed_extensions: Iterable):
    """Check file extensions"""
    _, ext = os.path.splitext(file_path)
    assert ext in allowed_extensions, f'file_path should be one of {allowed_extensions}, got {ext}.'
    return True
