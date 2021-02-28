import requests
import re
from urllib.parse import urljoin
from eudract.utils import json_handler


class Eudract:

    def __init__(self):
        self._BASE_URL = "https://www.clinicaltrialsregister.eu/"
        self._SEARCH = urljoin(self._BASE_URL, "/ctr-search/search")
        self._DOWNLOAD = urljoin(self._BASE_URL, "/ctr-search/rest/download/")
               
    def search(self, query, level="summary", to_dict=False):
        next_page = ["&page=1"]
        ids = []
        while next_page:
            pageid = re.findall(r"\d+", next_page[0])
            print("scraping page {}".format(pageid[0]))
            r = requests.get(self._SEARCH, params={'query': query, 'page': pageid[0]}, verify=False)
            next_page = re.findall(r"(?<=href=\").*?(?=\"\saccesskey=\"n\">\s*Next)", r.text)
            ids += list(set(re.findall(r"20\d{2}-\d{6}-\d{2}", r.text)))
        data = [{el: self.info(el, level, to_dict)} for el in ids]
        return data


    def info(self, eudract, level="summary", to_dict=False):
        r = requests.get(urljoin(self._DOWNLOAD, level), params={'mode':'selected', 'eudracts': eudract}, verify=False)
        if to_dict:
            return json_handler(r.text, level)
        return r.text
        



