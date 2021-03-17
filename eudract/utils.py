import re
from bs4 import BeautifulSoup


def json_handler(x, level, data):
    if level == "summary":
        for k in data.keys():
            val = re.findall("(?<={}:)(.+)".format(k), x)
            if val:
                data[k] = val[0].strip()

    if level == "full":
        soup = BeautifulSoup(x, "html.parser")
        field_id = [i.text.strip() for i in soup.find_all("td", class_="first")]
        field_name = [i.text.strip() for i in soup.find_all("td", class_="second")]
        field_value = [i.text.strip() for i in soup.find_all("td", class_="third")]
        res = {"{}:{}".format(i, j): k for i, j, k in zip(field_id, field_name, field_value)}
        for k in data.keys():
            data[k] = {key: res[key] for key in res.keys() if bool(re.search("^{}[.]".format(k[0]), key))}

    return data
