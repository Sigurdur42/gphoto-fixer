from unittest import TestCase

from gphoto_fixer.main import get_patched_json


class TestPatchedNumbering(TestCase):
    def test_get_patched_json(self):
        data = {
            (
                'Screenshot_20210112-093232_eBay Kleinanzeigen.',
                'Screenshot_20210112-093232_eBay Kleinanzeigen.jpg'),
            ('20011231_230000-1.JPG(1)', '20011231_230000-1(1).JPG'),
            ('20011231_230000-1.JPG', '20011231_230000-1.JPG'),
            ('Screenshot_20231113_165226_Samsung Internet.jp', 'Screenshot_20231113_165226_Samsung Internet.jpg')

        }

        for _ in data:
            self.__run_and_verify(_[0], _[1])

    def __run_and_verify(self, file_name: str, expected: str):
        result = get_patched_json(file_name)
        self.assertEqual(expected, result)
