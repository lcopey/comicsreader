#!/usr/bin/env python

"""Tests for `metaprocessor` submodule."""

import unittest
import json
from comicsreader.metaprocessor import TitleProcessor, MetaProcessor


class TestTitleProcessor(unittest.TestCase):
    """Tests for `TitleProcessor` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        with open('./Processor_tests.json', mode='r') as f:
            self.data = json.load(f)

    def test_processor(self):
        """Test something."""
        for row in self.data.values():
            processor = TitleProcessor()
            extension, date, volumes, chapters, title, tokenized_file = processor(row['file'])
            processed = (extension, date, volumes, chapters, title, tokenized_file)
            true_value = row['extension'], row['date'], row['volumes'], row['chapters'], row['title'], row[
                'tokenized_file']
            self.assertTupleEqual(processed, true_value)


class TestMetaProcessor(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures, if any."""
        with open('./Processor_tests.json', mode='r') as f:
            self.data = json.load(f)

    def test_meta_processor(self):
        for row in self.data.values():
            processed = MetaProcessor.from_file(row['file']).as_dict()
            self.assertDictEqual(processed, row)
