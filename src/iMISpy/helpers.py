def genericProp(pitem, pname, pval=None, collection="Properties"):
    for prop in pitem[collection]["$values"]:
        if prop["Name"] == pname:
            if isinstance(prop["Value"], dict):
                if pval != None:
                    prop["Value"]["$value"] = pval
                return prop["Value"]["$value"]
            else:
                if pval != None:
                    prop["Value"] = pval
                return prop["Value"]

def deleteGenericProp(pitem, pname, collection="Properties"):
    newprops = [] # we do this because it's an array. Alternatively we could find the index then delete the index but I dunno about that...
    for prop in pitem[collection]["$values"]:
        if prop["Name"] != pname:
            newprops.append(prop)
    pitem[collection]["$values"] = newprops


ALLIANCE_BODY = {
    "$type": "Asi.Soa.Core.DataContracts.GenericEntityData, Asi.Contracts",
    "EntityTypeName": "ACH_MarketingGroups",
    "PrimaryParentEntityTypeName": "Party",
    "PrimaryParentIdentity": {
        "$type": "Asi.Soa.Core.DataContracts.IdentityData, Asi.Contracts",
        "EntityTypeName": "Party",
        "IdentityElements": {
            "$type": "System.Collections.ObjectModel.Collection`1[[System.String, mscorlib]], mscorlib",
            "$values": [""]
        }
    },
    "Properties": {
        "$type": "Asi.Soa.Core.DataContracts.GenericPropertyDataCollection, Asi.Contracts",
        "$values": [
            {
                "$type": "Asi.Soa.Core.DataContracts.GenericPropertyData, Asi.Contracts",
                "Name": "ID",
                "Value": ""
            },
            {
                "$type": "Asi.Soa.Core.DataContracts.GenericPropertyData, Asi.Contracts",
                "Name": "GroupName",
                "Value": ""
            }
        ]
    }
}
