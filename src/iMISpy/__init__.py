from .session import webinit
from .api import iMISAPI
from . import helpers
from .settings import init

def openAPI(dictobj, retryForceList=None):
    init(dictobj)
    return iMISAPI(webinit(retryForceList=retryForceList))
