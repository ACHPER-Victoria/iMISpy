import logging
import time
import requests
from .settings import SETTINGS

AUTH_HEADER = { 'content-type': "application/x-www-form-urlencoded", "X-AUTH-ATTEMPT" : "Y"}
AUTH_DATA = { "Username" : "", "Password": "", "Grant_type": "password" }

from requests.auth import AuthBase

class iMISAuth(AuthBase):
    expires = time.time()-100
    access_token = None
    session = None
    def __init__(self, session):
        AUTH_DATA["Username"] = SETTINGS["iMIS_User"]
        AUTH_DATA["Password"] = SETTINGS["iMIS_Password"]
        self.session = session

    def token(self, regen=False):
        #no token or expired/about to expire: reauth
        if regen or not self.access_token or time.time() >= self.expires:
            r = self.session.post("/token", headers=AUTH_HEADER, data=AUTH_DATA)
            r.raise_for_status()
            token_data =  r.json()
            self.access_token = token_data["access_token"]
            self.expires = time.time()+token_data["expires_in"]-10 # minute 10 seconds for margin...
        #return token string
        return "Bearer %s" % self.access_token

    def reauthhook(self, res, *args, **kwargs):
        if res.status_code == requests.codes.unauthorized:
            logging.warn('Token rejected, refreshing')
            req = res.request
            req.headers['Authorization'] = self.token(True)
            logging.debug(f'Resending request: {req.method} - {req.url}')
            return session.send(res.request)

    def __call__(self, r):
        # modify and return the request only if not auth attempt.
        if "X-AUTH-ATTEMPT" not in r.headers:
            r.headers['Authorization'] = self.token()
            # add hook for reauth if 401
            r.register_hook('response', self.reauthhook)
        else :
            del r.headers["X-AUTH-ATTEMPT"]
        return r
