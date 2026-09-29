import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        title = "# Hello"
        self.assertEqual(
            extract_title(title),
            "Hello"
        )