from importlib import metadata as _metadata
import importlib
from os import getenv

__all__ = [
    'ProgressBar',
    '__version__']

def __getattr__(name):
    if name == 'ProgressBar':
        from .progressbar import ProgressBar
        return ProgressBar
    # If the requested attribute isn't one of the known top-level symbols,
    # try to lazily import a submodule (e.g. `threaded_order.scheduler`) so
    # attribute lookups such as those used by mocking/patching succeed.
    try:
        return importlib.import_module(f"{__name__}.{name}")
    except Exception:
        raise AttributeError(name)

try:
    __version__ = _metadata.version(__name__)
except _metadata.PackageNotFoundError:
    __version__ = '1.1.0'

if getenv('DEV'):
    __version__ = f'{__version__}+dev'
