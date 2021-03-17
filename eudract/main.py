import requests
import re
from urllib.parse import urljoin
from eudract.utils import json_handler


class Eudract:

    def __init__(self):
        self._BASE_URL = "https://www.clinicaltrialsregister.eu/"
        self._SEARCH = urljoin(self._BASE_URL, "/ctr-search/search")
        self._DOWNLOAD = urljoin(self._BASE_URL, "/ctr-search/rest/download/")
        self._SCHEMA = {
            "summary":
                {
                    "EudraCT Number": "",
                    "Sponsor Protocol Number": "",
                    "Sponsor Name": "",
                    "Full Title": "",
                    "Start Date": "",
                    "Medical condition": "",
                    "Disease": "",
                    "Population Age": "",
                    "Gender": "",
                    "Trial protocol": "",
                    "Link": ""
                },
            "full":
                {
                    "A. PROTOCOL INFORMATION": "",
                    "B. SPONSOR INFORMATION": "",
                    "C. APPLICANT IDENTIFICATION": "",
                    "D. IMP IDENTIFICATION": "",
                    "E. GENERAL INFORMATION ON THE TRIAL": "",
                    "F. POPULATION OF TRIAL SUBJECTS": "",
                    "G. INVESTIGATOR NETWORKS TO BE INVOLVED IN THE TRIAL": "",
                    "N. REVIEW BY THE COMPETENT AUTHORITY OR ETHICS COMMITTEE IN THE COUNTRY CONCERNED": "",
                    "P. END OF TRIAL": ""
                }
        }

    def search(self, query, level="summary", to_dict=False):
        next_page = ["&page=1"]
        ids = []
        while next_page:
            page_id = re.findall(r"\d+", next_page[0])
            r = requests.get(self._SEARCH, params={'query': query, 'page': page_id[0]}, verify=False)
            next_page = re.findall(r"(?<=href=\").*?(?=\"\saccesskey=\"n\">\s*Next)", r.text)
            ids += list(set(re.findall(r"20\d{2}-\d{6}-\d{2}", r.text)))
        data = [{el: self.info(el, level, to_dict)} for el in ids]
        return data

    def info(self, eudract, level="summary", to_dict=False):
        if level == "summary":
            r = requests.get(urljoin(self._DOWNLOAD, level), params={'mode': 'selected', 'eudracts': eudract},
                             verify=False)
            if to_dict:
                data = json_handler(r.text, level, self._SCHEMA[level])
            else:
                data = r.text

        if level == "full":
            if to_dict:
                r = requests.get(self._SEARCH, params={'query': eudract}, verify=False)
                full_url = re.findall(r"ctr-search/trial/{}/[A-Z][A-Z]".format(eudract), r.text)
                r_full = requests.get(urljoin(self._BASE_URL, full_url[0]), verify=False)
                data = json_handler(r_full.text, level, self._SCHEMA[level])
            else:
                r = requests.get(urljoin(self._DOWNLOAD, level), params={'mode': 'selected', 'eudracts': eudract},
                                 verify=False)
                data = r.text

        return data
