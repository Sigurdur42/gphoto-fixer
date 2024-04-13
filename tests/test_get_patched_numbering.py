from unittest import TestCase

from gphoto_fixer.main import get_patched_json


class TestPatchedNumbering(TestCase):
    def test_get_patched_json(self):
        data = {
            ('20011231_230000-1.JPG(1)', '20011231_230000-1(1).JPG'),
            ('20011231_230000-1.JPG', '20011231_230000-1.JPG')
        }

        for _ in data:
            self.__run_and_verify(_[0], _[1])

    def __run_and_verify(self, file_name: str, expected: str):
        result = get_patched_json(file_name)
        self.assertEqual(expected, result)