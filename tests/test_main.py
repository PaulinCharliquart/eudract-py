from eudract import Eudract
import tempfile
import sqlite3


def test_search():
    eu = Eudract()
    assert eu.search("EFC14280", "summary", False) == [
        "\r\n\r\nEudraCT Number:          2015-001314-10\r\nSponsor Protocol Number: EFC14280\r\nSponsor Name:            SANOFI-AVENTIS RECHERCHE ET DEVELOPPEMENT\r\nFull Title:              A Randomized, Double-blind, 52-week, Placebo Controlled Efficacy and Safety Study of Dupilumab, in Patients with Bilateral Nasal Polyposis on a Background Therapy with Intranasal Corticosteroids\r\nStart Date:              2016-11-29\r\nMedical condition:       Bilateral nasal polyposis\r\nDisease:                 Version: 19.0, SOC Term: 10038738 - Respiratory, thoracic and mediastinal disorders, Classification Code: 10028756, Term: Nasal polyps, Level: PT\r\nPopulation Age:          Adults, Elderly\r\nGender:                  Male, Female\r\nTrial protocol:          SE(Completed) PT(Completed) ES(Completed) BE(Completed) \r\nLink:                    https://www.clinicaltrialsregister.eu/ctr-search/search?query=eudract_number:2015-001314-10"
    ]
    assert eu.search("EFC14280", "summary", True) == [
        {
            "EudraCT Number": "2015-001314-10",
            "Sponsor Protocol Number": "EFC14280",
            "Sponsor Name": "SANOFI-AVENTIS RECHERCHE ET DEVELOPPEMENT",
            "Full Title": "A Randomized, Double-blind, 52-week, Placebo Controlled Efficacy and Safety Study of Dupilumab, in Patients with Bilateral Nasal Polyposis on a Background Therapy with Intranasal Corticosteroids",
            "Start Date": "2016-11-29",
            "Medical condition": "Bilateral nasal polyposis",
            "Disease": "Version: 19.0, SOC Term: 10038738 - Respiratory, thoracic and mediastinal disorders, Classification Code: 10028756, Term: Nasal polyps, Level: PT",
            "Population Age": "Adults, Elderly",
            "Gender": "Male, Female",
            "Trial protocol": "SE(Completed) PT(Completed) ES(Completed) BE(Completed)",
            "Link": "https://www.clinicaltrialsregister.eu/ctr-search/search?query=eudract_number:2015-001314-10",
        }
    ]
    assert eu.search("gutihkkùml") == []
    x = eu.search("covid", size=10, to_dict=True)
    assert len(x) == 10
    assert len(set([i["EudraCT Number"] for i in x])) == 10


def test_info():
    eu = Eudract()
    assert eu.info("jffs") == ""
    assert (
        eu.info("2015-001314-10", "summary", False)
        == "\r\n\r\nEudraCT Number:          2015-001314-10\r\nSponsor Protocol Number: EFC14280\r\nSponsor Name:            SANOFI-AVENTIS RECHERCHE ET DEVELOPPEMENT\r\nFull Title:              A Randomized, Double-blind, 52-week, Placebo Controlled Efficacy and Safety Study of Dupilumab, in Patients with Bilateral Nasal Polyposis on a Background Therapy with Intranasal Corticosteroids\r\nStart Date:              2016-11-29\r\nMedical condition:       Bilateral nasal polyposis\r\nDisease:                 Version: 19.0, SOC Term: 10038738 - Respiratory, thoracic and mediastinal disorders, Classification Code: 10028756, Term: Nasal polyps, Level: PT\r\nPopulation Age:          Adults, Elderly\r\nGender:                  Male, Female\r\nTrial protocol:          SE(Completed) PT(Completed) ES(Completed) BE(Completed) \r\nLink:                    https://www.clinicaltrialsregister.eu/ctr-search/search?query=eudract_number:2015-001314-10"
    )
    assert eu.info("2015-001314-10", "summary", True) == {
        "EudraCT Number": "2015-001314-10",
        "Sponsor Protocol Number": "EFC14280",
        "Sponsor Name": "SANOFI-AVENTIS RECHERCHE ET DEVELOPPEMENT",
        "Full Title": "A Randomized, Double-blind, 52-week, Placebo Controlled Efficacy and Safety Study of Dupilumab, in Patients with Bilateral Nasal Polyposis on a Background Therapy with Intranasal Corticosteroids",
        "Start Date": "2016-11-29",
        "Medical condition": "Bilateral nasal polyposis",
        "Disease": "Version: 19.0, SOC Term: 10038738 - Respiratory, thoracic and mediastinal disorders, Classification Code: 10028756, Term: Nasal polyps, Level: PT",
        "Population Age": "Adults, Elderly",
        "Gender": "Male, Female",
        "Trial protocol": "SE(Completed) PT(Completed) ES(Completed) BE(Completed)",
        "Link": "https://www.clinicaltrialsregister.eu/ctr-search/search?query=eudract_number:2015-001314-10",
    }


def test_search_cache():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db_file = tmp.name
    eu = Eudract()
    x = eu.search("covid", size=10, to_dict=True, cache_file=db_file)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(
        """ SELECT COUNT(*) from results """,
    )
    rows = cur.fetchone()[0]
    assert rows == 10
    x = eu.search("covid", size=10, to_dict=False, cache_file=db_file)
    cur.execute(
        """ SELECT COUNT(*) from results """,
    )
    rows = cur.fetchone()[0]
    assert rows == 20


def test_info_cache():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db_file = tmp.name
    eu = Eudract()
    x = eu.search("EFC14280", "summary", to_dict=True, cache_file=db_file)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(
        """ SELECT COUNT(*) from results """,
    )
    rows = cur.fetchone()[0]
    assert rows == 1
    x = eu.search("EFC14280", "summary", to_dict=False, cache_file=db_file)
    cur.execute(
        """ SELECT COUNT(*) from results """,
    )
    rows = cur.fetchone()[0]
    assert rows == 2
