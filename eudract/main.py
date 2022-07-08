"""
main.py
====================================
The core module of eudract-py
"""

import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
from eudract.utils import read_cache, write_cache, create_connection, create_table


class Eudract:
    """Main class"""

    def __init__(self):
        self._BASE_URL = "https://www.clinicaltrialsregister.eu/"
        self._SEARCH = urljoin(self._BASE_URL, "/ctr-search/search")
        self._DOWNLOAD = urljoin(self._BASE_URL, "/ctr-search/rest/download/")
        self._SCHEMA = {
            "summary": [
                "EudraCT Number",
                "Sponsor Protocol Number",
                "Sponsor Name",
                "Full Title",
                "Start Date",
                "Medical condition",
                "Disease",
                "Population Age",
                "Gender",
                "Trial protocol",
                "Link",
            ],
            "full": [
                "A. PROTOCOL INFORMATION",
                "B. SPONSOR INFORMATION",
                "C. APPLICANT IDENTIFICATION",
                "D. IMP IDENTIFICATION",
                "E. GENERAL INFORMATION ON THE TRIAL",
                "F. POPULATION OF TRIAL SUBJECTS",
                "G. INVESTIGATOR NETWORKS TO BE INVOLVED IN THE TRIAL",
                "N. REVIEW BY THE COMPETENT AUTHORITY OR ETHICS COMMITTEE IN THE COUNTRY CONCERNED",
                "P. END OF TRIAL",
            ],
        }

    def json_handler(self, doc, level):
        data = dict.fromkeys(self._SCHEMA[level], "")
        if level == "summary":
            for k in data.keys():
                val = re.findall("(?<={}:)(.+)".format(k), doc)
                if val:
                    data[k] = val[0].strip()

        if level == "full":
            soup = BeautifulSoup(doc, "html.parser")
            field_id = [i.text.strip() for i in soup.find_all("td", class_="first")]
            field_name = [i.text.strip() for i in soup.find_all("td", class_="second")]
            field_value = [i.text.strip() for i in soup.find_all("td", class_="third")]
            res = {
                "{}:{}".format(i, j): k
                for i, j, k in zip(field_id, field_name, field_value)
            }
            for k in data.keys():
                data[k] = {
                    key: res[key]
                    for key in res.keys()
                    if bool(re.search("^{}[.]".format(k[0]), key))
                }

        return data

    def search(self, query, level="summary", to_dict=False, size=None, cache_file=None):
        """
        Search studies in Eudract

        Args:
            query (str): text to search
            level (str): type of info to extract (either summary or full)
            to_dict (Bool): Return the results as dict
            size (int): Max size of results
            cache_file (str): Set cache filename to save results to sqlite db

        Returns:
            [list]: List of dictionary
        """
        next_page = ["&page=1"]
        ids = []
        while next_page:
            page_id = re.findall(r"\d+", next_page[0])
            r = requests.get(
                self._SEARCH, params={"query": query, "page": page_id[0]}, verify=False
            )
            r.raise_for_status
            next_page = re.findall(
                r"(?<=href=\").*?(?=\"\saccesskey=\"n\">\s*Next)", r.text
            )
            ids += list(set(re.findall(r"20\d{2}-\d{6}-\d{2}", r.text)))
            if size is not None:
                if len(ids) >= size:
                    ids = ids[:size]
                    break
        data = [self.info(el, level, to_dict, cache_file) for el in ids]
        return data

    def info(self, eudract, level="summary", to_dict=False, cache_file=None):
        """
        Get info for a study

        Args:
            eudract (str): Eudract ID
            level (str): type of info to extract (either summary or full)
            to_dict (Bool): Return the results as dict
            cache_file (str): Set cache filename to save results to sqlite db

        Returns:
            [dict]: dictionary
        """
        if cache_file:
            db = create_connection(cache_file)
            key_id = "_".join([eudract, level, str(to_dict)]).lower()

            if create_table(db):
                content = read_cache(db, key_id)
                if content:
                    data = json.loads(content) if to_dict else content
                    return data
        if level == "summary":
            r = requests.get(
                urljoin(self._DOWNLOAD, level),
                params={"mode": "selected", "eudracts": eudract},
                verify=False,
            )
            if to_dict:
                data = self.json_handler(r.text, level)
            else:
                data = r.text

        if level == "full":
            if to_dict:
                r = requests.get(self._SEARCH, params={"query": eudract}, verify=False)
                full_url = re.findall(
                    r"ctr-search/trial/{}/[A-Z][A-Z]".format(eudract), r.text
                )
                r.raise_for_status
                r_full = requests.get(
                    urljoin(self._BASE_URL, full_url[0]), verify=False
                )
                r.raise_for_status
                data = self.json_handler(r_full.text, level)
            else:
                r = requests.get(
                    urljoin(self._DOWNLOAD, level),
                    params={"mode": "selected", "eudracts": eudract},
                    verify=False,
                )
                r.raise_for_status
                data = r.text

        if cache_file:
            content = json.dumps(data) if to_dict else data
            write_cache(db, key_id, content)
        return data

    def dump(self, level="summary", to_dict=False, cache_file=None):
        """
        Dump eudract

        Args:
            level (str): type of info to extract (either summary or full)
            to_dict (Bool): Return the results as dict
            cache_file (str): Set cache filename to save results to sqlite db

        Returns:
            [dict]: dictionary
        """
        return self.search(
            query="", level=level, to_dict=to_dict, cache_file=cache_file
        )
