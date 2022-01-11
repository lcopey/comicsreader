import unittest
import os
from comicsbrowser.converter import cbr2cbz, pdf2cbz


class ConvertTestCase(unittest.TestCase):
    def test_convert_cbr(self):
        cbr2cbz('01 Wasteland.cbr')
        self.assertTrue(os.path.exists('01 Wasteland.cbz'))

    def test_convert_pdf(self):
        pdf2cbz('./Invisible Republic - T01.pdf')
        self.assertTrue(os.path.exists('Invisible Republic - T01.cbz'))


if __name__ == '__main__':
    unittest.main()
