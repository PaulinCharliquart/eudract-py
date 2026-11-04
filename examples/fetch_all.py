import json

from eudract import Eudract

eu = Eudract()

data = eu.fetch_all()

with open("fetch_all.json", "w") as f:
    f.write(json.loads(data))
