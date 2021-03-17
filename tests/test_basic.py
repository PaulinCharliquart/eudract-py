import unittest
from eudract import Eudract


class TestBasic(unittest.TestCase):
    """
    Test suite for eudract-py.
    """

    def test_search(self):
        eu = Eudract()
        self.assertEqual(eu.search("EFC14280", "summary", False), [{
                                                                       '2015-001314-10': '\r\n\r\nEudraCT Number:          2015-001314-10\r\nSponsor Protocol Number: EFC14280\r\nSponsor Name:            SANOFI-AVENTIS RECHERCHE ET DEVELOPPEMENT\r\nFull Title:              A Randomized, Double-blind, 52-week, Placebo Controlled Efficacy and Safety Study of Dupilumab, in Patients with Bilateral Nasal Polyposis on a Background Therapy with Intranasal Corticosteroids\r\nStart Date:              2016-11-29\r\nMedical condition:       Bilateral nasal polyposis\r\nDisease:                 Version: 19.0, SOC Term: 10038738 - Respiratory, thoracic and mediastinal disorders, Classification Code: 10028756, Term: Nasal polyps, Level: PT\r\nPopulation Age:          Adults, Elderly\r\nGender:                  Male, Female\r\nTrial protocol:          SE(Completed) PT(Completed) ES(Completed) BE(Completed) \r\nLink:                    https://www.clinicaltrialsregister.eu/ctr-search/search?query=eudract_number:2015-001314-10'}])
        self.assertEqual(eu.search("EFC14280", "summary", True), [{'2015-001314-10': {
            'EudraCT Number': '2015-001314-10', 'Sponsor Protocol Number': 'EFC14280',
            'Sponsor Name': 'SANOFI-AVENTIS RECHERCHE ET DEVELOPPEMENT',
            'Full Title': 'A Randomized, Double-blind, 52-week, Placebo Controlled Efficacy and Safety Study of Dupilumab, in Patients with Bilateral Nasal Polyposis on a Background Therapy with Intranasal Corticosteroids',
            'Start Date': '2016-11-29', 'Medical condition': 'Bilateral nasal polyposis',
            'Disease': 'Version: 19.0, SOC Term: 10038738 - Respiratory, thoracic and mediastinal disorders, Classification Code: 10028756, Term: Nasal polyps, Level: PT',
            'Population Age': 'Adults, Elderly', 'Gender': 'Male, Female',
            'Trial protocol': 'SE(Completed) PT(Completed) ES(Completed) BE(Completed)',
            'Link': 'https://www.clinicaltrialsregister.eu/ctr-search/search?query=eudract_number:2015-001314-10'}}])
        self.assertEqual(eu.search("gutihkkùml"), [])

    def test_info(self):
        eu = Eudract()
        self.assertEqual(eu.info("jffs"), '')
        self.assertEqual(eu.info("2015-001314-10", "summary", False),
                         '\r\n\r\nEudraCT Number:          2015-001314-10\r\nSponsor Protocol Number: EFC14280\r\nSponsor Name:            SANOFI-AVENTIS RECHERCHE ET DEVELOPPEMENT\r\nFull Title:              A Randomized, Double-blind, 52-week, Placebo Controlled Efficacy and Safety Study of Dupilumab, in Patients with Bilateral Nasal Polyposis on a Background Therapy with Intranasal Corticosteroids\r\nStart Date:              2016-11-29\r\nMedical condition:       Bilateral nasal polyposis\r\nDisease:                 Version: 19.0, SOC Term: 10038738 - Respiratory, thoracic and mediastinal disorders, Classification Code: 10028756, Term: Nasal polyps, Level: PT\r\nPopulation Age:          Adults, Elderly\r\nGender:                  Male, Female\r\nTrial protocol:          SE(Completed) PT(Completed) ES(Completed) BE(Completed) \r\nLink:                    https://www.clinicaltrialsregister.eu/ctr-search/search?query=eudract_number:2015-001314-10')
        self.assertEqual(eu.info("2015-001314-10", "summary", True),
                         {'EudraCT Number': '2015-001314-10', 'Sponsor Protocol Number': 'EFC14280',
                          'Sponsor Name': 'SANOFI-AVENTIS RECHERCHE ET DEVELOPPEMENT',
                          'Full Title': 'A Randomized, Double-blind, 52-week, Placebo Controlled Efficacy and Safety Study of Dupilumab, in Patients with Bilateral Nasal Polyposis on a Background Therapy with Intranasal Corticosteroids',
                          'Start Date': '2016-11-29', 'Medical condition': 'Bilateral nasal polyposis',
                          'Disease': 'Version: 19.0, SOC Term: 10038738 - Respiratory, thoracic and mediastinal disorders, Classification Code: 10028756, Term: Nasal polyps, Level: PT',
                          'Population Age': 'Adults, Elderly', 'Gender': 'Male, Female',
                          'Trial protocol': 'SE(Completed) PT(Completed) ES(Completed) BE(Completed)',
                          'Link': 'https://www.clinicaltrialsregister.eu/ctr-search/search?query=eudract_number:2015-001314-10'})


if __name__ == '__main__':
    unittest.main()
