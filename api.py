from sys import stderr
from collections import OrderedDict
from .helpers import genericProp

class APIException(Exception):
    def __init__(self, req, *args, **kwargs):
        self.req = req
        super(APIException, self).__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.req.status_code} - {self.req.url} \n{self.req.text[:500]}"

class iMISAPI:
    def __init__(self, session):
        self.session = session

    def get(self, endpoint, id):
        r = self.session.get(f"{endpoint}/{id}")
        r.raise_for_status()
        return r.json()

    def put(self, endpoint, id, obj):
        r = self.session.put(f"{endpoint}/{id}", json=obj)
        r.raise_for_status()
        return r.json()

    def post(self, endpoint, obj, id=""):
        r = self.session.post(f"{endpoint}/{id}", json=obj)
        r.raise_for_status()
        return r.json()

    def delete(self, endpoint, id=""):
        print(f"DELETE {endpoint}/{id}")
        r = self.session.delete(f"{endpoint}/{id}")
        r.raise_for_status()
        return r

    def apiIterator(self, url, p):
        # BE CAREFUL WHEN ITERATING. Don't modify objects that could change the iteration results/ordering.
        print(repr(p))
        p = list(p)
        p.append(("limit","100"))
        r = self.session.get(f"{url}", params=p)
        if r.status_code != 200:
            raise APIException(r)
        json = r.json(object_pairs_hook=OrderedDict)
        while json["Count"] > 0:
            nextoffset = json["NextOffset"]
            for x in json["Items"]["$values"]:
                yield x
            if nextoffset == 0: return
            r = self.session.get(f"{url}", params=p+[('offset', nextoffset)])
            if r.status_code != 200:
                raise APIException(r)
            json = r.json(object_pairs_hook=OrderedDict)

    def IterateQuery(self, q, params=None):
        qparams = (("queryname", q),)
        if params: qparams = qparams + params
        for x in self.apiIterator("query", qparams):
            yield x

    def getContact(self, id):
        r = self.session.get(f"Party/{id}")
        r.raise_for_status()
        return r.json()

    def updateContact(self, obj, id=None):
        if id is None: id = obj["PartyId"]
        r = self.session.put(f"Party/{id}", json=obj)
        r.raise_for_status()
        return r.json()

    def allianceList(self, alliancename):
        return list(self.apiIterator("/api/ACH_MarketingGroups", (('GroupName', alliancename),) ))

    def removeFromAlliance(self, id, alliancename):
        for entry in self.apiIterator("/api/ACH_MarketingGroups", (('GroupName', alliancename),) ):
            if genericProp(entry, "GroupName") == alliancename:
                print(f"Removing {id} from {alliancename}")
                print(self.delete("/api/ACH_MarketingGroups", "~{0}".format("|".join(entry["Identity"]["IdentityElements"]["$values"]))))
                exit()
