"""Test templated yaml rep"""

import unittest

from clustack.template import load_templated_yaml_rep

class TestYaml(unittest.TestCase):

    def test_templated_yaml_rep(self):
        yaml_rep = load_templated_yaml_rep('samtools')

        self.assertEqual(yaml_rep['version'], 1.1)
        build_string = yaml_rep['build'][0]
        string_end = build_string[-6:]
        self.assertEqual('source', string_end)



if __name__ == '__main__':
    unittest.main()
    

