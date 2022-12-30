from .session import web
from .api import iMISAPI
from . import helpers
from .settings import init
api = None

def setup(dictobj):
    init(dictobj)
    api = iMISAPI(web)
