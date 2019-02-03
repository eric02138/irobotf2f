# -*- coding: utf-8 -*-
"""
iRobot Food2Fork Application Main Executable

"python main.py" runs the interactive version
TODO: cli version
"""
import os
import sys
import urllib
import requests


class AppMgr:
    """
    Class to manage overall application setup.
    """
    def __init__(self):
        self.f2f_api_key = None
        self._continue = True      #Maybe the user wants to search again?
        self.get_f2f_api_key()

    def get_f2f_api_key(self):
        """
        Sets the app's api_key variable from ../apikey.conf
        :return:
        """
        f2f_api_key_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        f2f_api_key_path = os.path.join(f2f_api_key_dir, 'apikey.conf')
        try:
            with open(f2f_api_key_path, "r") as f:
                self.f2f_api_key = f.read()
        except Exception:
            print "Could not read api key at {0}".format(f2f_api_key_path)
            raise

    def prompt_user_to_search_again(self):
        print "Would you like to search again? (y/n)"
        user_response = raw_input()
        while user_response.lower()[0:1] != "y" and user_response.lower()[0:1] != "n":
            user_response = raw_input("Sorry, but I don't understand. "
                                      "Please try again. (y/n): ")
        if user_response.lower()[0:1] == "n":
            print "Bye!"
            self._continue = False

class IngredientMgr:
    """
    Class to prompt the user for the list of ingredients
    """
    def __init__(self):
        """
        initializes ingredients
        """
        self.user_input = True
        self.ingredient_list = []

    def get_ingredient_from_user(self):
        """
        prompts a user for an ingredient
        :return: string user_input
        """
        print "Please add an ingredient."
        print "If your list is complete, simply press return."
        user_input = raw_input()
        return user_input.strip()

    def prompt_user_for_ingredients(self):
        """
        Keep prompting user for ingredients if they haven't entered an empty string
        :return:
        """
        while self.user_input:
            self.user_input = self.get_ingredient_from_user()
            if self.user_input:
                self.ingredient_list.append(self.user_input)
        return self.ingredient_list

    def display_ingredient_list(self):
        """
        Format the display of the ingredients
        :return: None
        """
        print "Ingredient List:"
        print "****************************************"
        for i, ing in enumerate(self.ingredient_list, 1):
            print "  {i}) {ing}".format(i=i,
                                        ing=ing)
        print "****************************************"
        print

class RequestMgr:
    """
    Class for handling communication with F2F API
    """
    def __init__(self, f2f_api_key):
        """
        Copy the api key from the app level down to the ReqMgr level for easy-access
        This means a RequestManager must be initialized with an AppMgr
        :param f2f_api_key:
        """
        self.f2f_api_key = f2f_api_key
        self.f2f_search_url = "https://www.food2fork.com/api/search"
        self.f2f_detail_url = "https://www.food2fork.com/api/get"

    def search_by_ingredients(self, ingredient_list):
        ingredients_string = ",".join(ingredient_list)
        print ingredients_string
        payload = urllib.urlencode({'key': self.f2f_api_key,
                                    'q': ingredients_string})
        print self.f2f_search_url
        print payload
        response = requests.post(self.f2f_search_url, data=payload)
        print response.text
        print response.json

def main():
    app_mgr = AppMgr()
    req_mgr = RequestMgr(app_mgr.f2f_api_key)
    while app_mgr._continue:
        ing_mgr = IngredientMgr()
        ing_mgr.prompt_user_for_ingredients()
        ing_mgr.display_ingredient_list()
        req_mgr.search_by_ingredients(ing_mgr.ingredient_list)
        app_mgr.prompt_user_to_search_again()

if __name__ == "__main__":
    main()

__date__ = "2019-02-01"
__version__ = "0.0.1"
__author__ = "Eric Mattison"
__maintainer__ = "Eric Mattison"
__email__ = "emattison@gmail.com"
