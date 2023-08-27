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
import math
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from eudract.utils import (
    read_cache,
    write_cache,
    create_connection,
    create_table,
    validate_id,
)


class Eudract:
    """Main class"""

    def __init__(self):
        self.session = requests.Session()
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

    def json_handler(self, doc, level: str):
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

    def read_page(self, url, query=None, page=None):
        r = self.session.get(url, params={"query": query, "page": page}, verify=False)
        r.raise_for_status()
        ids = list(set(re.findall(r"20\d{2}-\d{6}-\d{2}", r.text)))
        next_page = re.findall(
            r"(?<=href=\").*?(?=\"\saccesskey=\"n\">\s*Next)", r.text
        )
        return ids, next_page, r.text

    def search(self, query: str, level="summary", size=None, cache_file=None):
        """
        Search studies in Eudract

        Args:
            query (str): text to search
            level (str): type of info to extract (either summary or full)
            size (int): Max size of results
            cache_file (str): Set cache filename to save results to sqlite db

        Returns:
            [list]: List of dictionary
        """
        next_page = ["&page=1"]
        ids = []
        while next_page:
            page_id = re.findall(r"\d+", next_page[0])
            new_id, next_page, _ = self.read_page(
                url=self._SEARCH, query=query, page=page_id
            )
            ids += new_id
            if size is not None and len(ids) >= size:
                ids = ids[:size]
                break
        data = [self.info(el, level, cache_file) for el in ids]
        return data

    def info(self, eudract: str, level="summary", cache_file=None):
        """
        Get info for a study

        Args:
            eudract (str): Eudract ID
            level (str): type of info to extract (either summary or full)
            cache_file (str): Set cache filename to save results to sqlite db

        Returns:
            [dict]: dictionary
        """
        if validate_id(eudract_id=eudract) is False:
            return None
        if cache_file:
            db = create_connection(cache_file)
            key_id = "_".join([eudract, level, str(True)]).lower()

            if create_table(db):
                content = read_cache(db, key_id)
                if content:
                    data = json.loads(content)
                    return data
        if level == "summary":
            r = self.session.get(
                urljoin(self._DOWNLOAD, level),
                params={"mode": "selected", "eudracts": eudract},
                verify=False,
            )
            if r.text == "":
                return None
            data = self.json_handler(r.text, level)
        if level == "full":
            _, _, text = self.read_page(url=self._SEARCH, query=eudract)
            full_url = re.findall(
                r"ctr-search/trial/{}/[A-Z][A-Z]".format(eudract), text
            )
            if len(full_url) == 0:
                return None
            _, _, r_full = self.read_page(urljoin(self._BASE_URL, full_url[0]))
            data = self.json_handler(r_full, level)

        if cache_file:
            content = json.dumps(data)
            write_cache(db, key_id, content)
        return data

    def dump(self, level="summary", cache_file=None, max_worker=5):
        """
        Dump eudract

        Args:
            level (str): type of info to extract (either summary or full)
            cache_file (str): Set cache filename to save results to sqlite db

        Returns:
            [dict]: dictionary
        """
        _, _, text = self.read_page(url=self._SEARCH)
        soup = BeautifulSoup(text, "html.parser")
        total_studies = int(soup.find("span", {"id": "total"}).text)
        page_size = 20
        total_pages = math.ceil(total_studies / page_size)
        with ThreadPoolExecutor(max_workers=max_worker) as pool:
            res = pool.map(
                self.read_page,
                repeat(self._SEARCH),
                repeat(None),
                [*range(1, total_pages + 1, 1)],
            )
        studies = []
        for x in res:
            studies.extend(x[0])
        with ThreadPoolExecutor(max_workers=max_worker) as pool:
            data = pool.map(self.info, studies)
        return data
