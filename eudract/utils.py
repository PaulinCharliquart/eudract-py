import json
import re
import eudract.schema


def json_handler(x, level):
    data = getattr(eudract.schema, level)()
    
    for k in data.keys():
        val = re.findall("(?<={}:)(.+)".format(k), x)
        if val:
            data[k] = val[0].strip()
    
    return data


