import unittest
import coverage

from speac_tests.speac_chapter_7_tests.new_form_test import NewFormTest
from speac_tests.speac_chapter_7_tests.pattern_match_test import PatternMatchTest
from speac_tests.speac_chapter_7_tests.speac_analysis_test import SPEAC_analysis_test
from speac_tests.speac_chapter_7_tests.speac_test import TestSPEAC
from speac_tests.speac_chapter_7_tests.top_level_test import TopLevelTest


class CoverageTest(unittest.TestCase):

    def test_all(self):
        cov = coverage.Coverage()
        cov.start()

        print("Testing new_form")
        NewFormTest().test_all()

        print("Testing pattern_match")
        PatternMatchTest().test_all()

        print("Testing speac_library")
        SPEAC_analysis_test().test_all()

        print("Testing speac_test")
        TestSPEAC().test_all()

        print("Testing top_level")
        TopLevelTest().test_all()

        cov.stop()
        cov.save()
        cov.report(show_missing=True, include="*/speac/*")