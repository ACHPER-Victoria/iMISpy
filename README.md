# iMISpy
Crude Python module for iMIS API

# How to use?
## Locally
You should have a .json file in your filesystem that has something similar to the following:
```json
{
  "iMIS_User" : "username",
  "iMIS_Password" : "password",
  "API_URL" : "https://example.com/api"
}
```
You can then initialise the library with something like:
```python
import json
from os.path import expanduser, join
from iMISpy import openAPI
home = expanduser("~")
api = openAPI(json.load(open(join(home, ".iMIS.json"), "rb")))
```

## Remote (e.g. Azure Functions)
Probably the most secure way to do this is to store the account details in a Azure Key Vault, then create environment variables that use the account details, then pass the environ to the init method.
```python
from os import environ
api = openAPI(environ)
```
