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
You can then initialise the library with:
```python
import json
from iMISpy import openAPI
home = expanduser("~")
api = openAPI(json.load(open(join(home, ".iMIS.json"), "rb")))
```
