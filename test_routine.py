import os
import unittest
import routine


class TestRouting(unittest.TestCase):
    def setUp(self) -> None:
        self.testFile = os.path.join("test_files", "test_en.txt")

    def test_read_extract_values(self):
        with open(self.testFile, 'r') as f:
            expected_results = [{
                'name': 'Pinco Pallo',
                'date': '05/30/2008',
                'group': 'No, I am not a member of any of these groups.',
                'learners': 'Graduate Level University.',
                'group_size': '10-19.',
                'primary_role': '.',
                'instructive_perc': '20%',
                'org_name': 'Mars University.',
                'employment_sector': '.',
                'prompt': '.',
                'location': '.',
                'country': 'Mars.',
                'province': 'Mars.',
                'city': 'Marsity.',
                'highest_qual': ', .',
                'years_teaching': '20-24.',
                'years_practicing': '25-29.',
                'gender': 'Male',
                'TR': '37',
                'TRb': '13',
                'TRi': '12',
                'TRa': '12',
                'AP': '35',
                'APb': '11',
                'APi': '13',
                'APa': '11',
                'DV': '33',
                'DVb': '9',
                'DVi': '13',
                'DVa': '11',
                'NU': '26',
                'NUb': '9',
                'NUi': '10',
                'NUa': '7',
                'SR': '29',
                'SRb': '10',
                'SRi': '9',
                'SRa': '10',
                'B': '52',
                'I': '57',
                'A': '51',
                'M': '32',
                'SD': '4',
                'HIT': '36',
                'LOT': '28',
                'T': '160'}]
            results = routine.get_results_from_lines(f.readlines())
            for k in expected_results[0].keys():
                self.assertEquals(results[0][0][k], expected_results[0][k])
