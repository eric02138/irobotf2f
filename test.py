# -*- coding: utf-8 -*-
"""
Unit Tests
"""
import os
import unittest
import __builtin__
from contextlib import contextmanager
from irobotf2f.__main__ import AppMgr, IngredientMgr, RequestMgr, RecipeMgr

@contextmanager
def mockRawInput(mock):
    """
    Shamelessly stolen from StackOverflow
    https://stackoverflow.com/questions/21046717/python-mocking-raw-input-in-unittests
    :param mock:
    :return:
    """
    original_raw_input = __builtin__.raw_input
    __builtin__.raw_input = lambda _: mock
    yield
    __builtin__.raw_input = original_raw_input

class TestAppMgr(unittest.TestCase):
    def setUp(self):
        self.app_mgr = AppMgr()

    def test_init(self):
        """
        Test that the api key is set and that continue is True
        """
        print os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.assertEqual(len(self.app_mgr.f2f_api_key), 32)
        self.assertEqual(self.app_mgr._continue, True)

    def test_prompt_user_to_search_again_y(self):
        with mockRawInput('y'):
            self.app_mgr.prompt_user_to_search_again()
            self.assertEqual(self.app_mgr._continue, True)

    def test_prompt_user_to_search_again_n(self):
        with mockRawInput('n'):
            self.app_mgr.prompt_user_to_search_again()
            self.assertEqual(self.app_mgr._continue, False)

class TestIngredientMgr(unittest.TestCase):
    def setUp(self):
        self.ing_mgr = IngredientMgr()

    def test_init(self):
        """
        Test that the ingredient list is empty and that user input is True
        """
        self.assertEqual(self.ing_mgr.ingredient_list, [])
        self.assertEqual(self.ing_mgr.user_input, True)

    def test_get_ingredient_from_user(self):
        with mockRawInput(' banana '):
            self.assertEqual(self.ing_mgr.get_ingredient_from_user(), 'banana')

class TestRequestMgr(unittest.TestCase):
    def setUp(self):
        app_mgr = AppMgr()
        self.request_mgr = RequestMgr(app_mgr.f2f_api_key)

    def test_init(self):
        """
        Test that the urls are set
        """
        self.assertEqual(self.request_mgr.f2f_search_url,
                         "https://www.food2fork.com/api/search")
        self.assertEqual(self.request_mgr.f2f_detail_url,
                         "https://www.food2fork.com/api/get")

    def test_search_by_ingredients(self):
        """
        Test that search returns results
        """
        recipe_id = self.request_mgr.search_by_ingredients(['butter', 'sugar', 'eggs'])
        self.assertGreater(recipe_id, 0)

    def test_search_by_bad_ingredients(self):
        """
        Test that bad search returns no results
        """
        recipe_id = self.request_mgr.search_by_ingredients(['asdfadsfa'])
        self.assertEqual(recipe_id, None)

    def test_search_by_no_ingredients(self):
        """
        Test that bad search returns no results
        """
        recipe_id = self.request_mgr.search_by_ingredients([])
        self.assertEqual(recipe_id, None)

    def test_get_recipe_by_id(self):
        """
        make sure that a known id returns the correct recipe
        """
        recipe = self.request_mgr.get_recipe_by_id(35354)
        self.assertIn("Guinness", recipe.get('title'))

class TestRecipeMgr(unittest.TestCase):
    def setUp(self):
        app_mgr = AppMgr()
        request_mgr = RequestMgr(app_mgr.f2f_api_key)
        recipe = request_mgr.get_recipe_by_id(35354)
        self.recipe_mgr = RecipeMgr(recipe)

    def test_init(self):
        """
        Test that the urls are set
        """
        self.assertIn('3/4 cup Guinness\n', self.recipe_mgr.all_ingredients)
        self.assertIn('1 tablespoon sugar', self.recipe_mgr.all_ingredients)
        self.assertIn('3 (8 ounce) packages cream cheese', self.recipe_mgr.all_ingredients)

    def test_set_searched_for_ingredients(self):
        sfi = self.recipe_mgr.set_searched_for_ingredients(['butter', 'sugar', 'eggs'])
        self.assertIn('2 tablespoons butter, melted', sfi)
        self.assertIn('1 tablespoon sugar', sfi)
        self.assertIn('1 cup sugar', sfi)
        self.assertIn('3 eggs', sfi)

    def test_diff_ingredient_lists(self):
        self.recipe_mgr.set_searched_for_ingredients(['butter', 'sugar', 'eggs'])
        missing_ingredients = self.recipe_mgr.diff_ingredient_lists()
        self.assertIn('3/4 cup Guinness\n', missing_ingredients)
        self.assertIn('12 ounces dark chocolate, chopped', missing_ingredients)
        self.assertIn('1/2 cup sour cream', missing_ingredients)
        self.assertIn('2 tablespoons cocoa powder', missing_ingredients)

if __name__ == '__main__':
    unittest.main()

__date__ = "2019-02-03"
__version__ = "0.0.1"
__author__ = "Eric Mattison"
__maintainer__ = "Eric Mattison"
__email__ = "emattison@gmail.com"