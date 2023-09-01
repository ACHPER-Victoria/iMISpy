from .session import webinit
from .api import iMISAPI
from . import helpers
from .settings import init

def openAPI(dictobj):
    init(dictobj)
    return iMISAPI(webinit())
