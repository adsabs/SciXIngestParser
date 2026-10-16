import json
import os
import unittest

from adsingestschema import ads_schema_validator

from ingestparser.parsers import ieee


class TestIEEE(unittest.TestCase):
    def setUp(self):
        stubdata_dir = os.path.join(os.path.dirname(__file__), "stubdata/")
        self.inputdir = os.path.join(stubdata_dir, "input")
        self.outputdir = os.path.join(stubdata_dir, "output")

    def test_ieee(self):
        filenames = [
            "ieee_conf1",
            "ieee_conf2",
            "ieee_conf3",
            "ieee_conf4",
        ]
        for f in filenames:
            test_infile = os.path.join(self.inputdir, f + ".xml")
            test_outfile = os.path.join(self.outputdir, f + ".json")
            parser = ieee.IEEEParser()

            with open(test_infile, "rb") as fp:
                input_data = fp.read()

            parsed = parser.parse(input_data)

            with open(test_outfile, "rb") as fp:
                output_text = fp.read()
                output_data = json.loads(output_text)

            # make sure this is valid schema
            try:
                ads_schema_validator().validate(parsed)
            except Exception:
                self.fail("Schema validation failed")
                pass

            # this field won't match the test data, discard
            parsed["recordData"]["parsedTime"] = ""

            self.maxDiff = None
            self.assertEqual(parsed, output_data)
