import unittest
import yaml
import routine
import ftfy


class TestRoutine(unittest.TestCase):
    def setUp(self) -> None:
        with open('templates/en.yaml', 'r') as f:
            self.enTemplate = yaml.safe_load(f)
        with open('templates/it.yaml', 'r') as f:
            self.itTemplate = yaml.safe_load(f)
        with open('test_files/test_en.txt', 'r') as f:
            self.enTestFile = f.readlines()
        with open('test_files/test_it.txt', 'r') as f:
            self.itTestFile = f.readlines()

    def test_read_extract_values_with_en_template(self):
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
        results = routine.get_results_from_lines(self.enTestFile, self.enTemplate)
        for k in expected_results[0].keys():
            self.assertEquals(results[0][0][k], expected_results[0][k])

    def test_read_extract_values_with_it_template(self):
        expected_results = [{
            'name': 'Pinco Pallo',
            'date': '10/10/2010',
            'group': 'No, non faccio parte di nessun gruppo.',
            'learners': 'Lauree Triennali',
            'group_size': '20-39.',
            'primary_role': 'Docente.',
            'instructive_perc': '40%',
            'org_name': 'Università di Giove.',
            'employment_sector': 'Istruzione.',
            'prompt': 'Richiesto dalla suprema corte di Giove.',
            'country': 'Giove.',
            'city': 'Giovina.',
            'highest_qual': 'Dottorato di ricerca (PhD).',
            'years_teaching': '5-9.',
            'years_practicing': '5-9.',
            'gender': 'Alieno',
            'TR': '36',
            'TRc': '12',
            'TRi': '11',
            'TRa': '13',
            'AP': '33',
            'APc': '12',
            'APi': '13',
            'APa': '8',
            'SV': '31',
            'SVc': '9',
            'SVi': '13',
            'SVa': '9',
            'CR': '22',
            'CRc': '10',
            'CRi': '8',
            'CRa': '4',
            'RS': '25',
            'RSc': '12',
            'RSi': '7',
            'RSa': '6',
            'C': '55',
            'I': '52',
            'A': '40',
            'M': '29.4',
            'DS': '5.16',
            'HIT': '34.56',
            'LOT': '24.24',
            'T': '147'}]
        results = routine.get_results_from_lines(self.itTestFile, self.itTemplate)
        for k in expected_results[0].keys():
            self.assertEquals(results[0][0][k], expected_results[0][k], "Checking field" + k)

    def test_read_extract_values_from_bad_encoding_it_file(self):
        with open("test_files/test_it_wrong_enc.txt", 'r') as f:
            expected_results = [{
                'name': 'La Pimpa',
                'instructive_perc': '50%',
                'org_name': 'Università di Venere.',
                'employment_sector': 'Istruzione Universitaria.',
                'prompt': 'Pre-requisiti.',
                'city': 'Venusia.',
                'highest_qual': 'Dottorato di ricerca (PhD).',
                'T': '185'}]
            results = routine.get_results_from_lines(f.readlines(), self.itTemplate)
            for k in expected_results[0].keys():
                self.assertEquals(results[0][0][k], expected_results[0][k])


