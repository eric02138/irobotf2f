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
        :return api key string:
        """
        f2f_api_key_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        f2f_api_key_path = os.path.join(f2f_api_key_dir, 'apikey.conf')
        try:
            with open(f2f_api_key_path, "r") as f:
                self.f2f_api_key = f.read()
        except Exception:
            print "Could not read api key at {0}".format(f2f_api_key_path)
            raise
        return self.f2f_api_key

    def prompt_user_to_search_again(self):
        """
        Prompts user to continue
        :return continue flag boolean:
        """
        print "Would you like to search again? (y/n)"
        user_response = raw_input("")
        while user_response.lower()[0:1] != "y" and user_response.lower()[0:1] != "n":
            user_response = raw_input("Sorry, but I don't understand. "
                                      "Please try again. (y/n): ")
        if user_response.lower()[0:1] == "n":
            print "Bye!"
            self._continue = False
        return self._continue

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
        :return user_input: string
        """
        print "Please add an ingredient."
        print "If your list is complete, simply press return."
        user_input = raw_input("")
        return user_input.strip()

    def prompt_user_for_ingredients(self):
        """
        Keep prompting user for ingredients if they haven't entered an empty string
        :return ingredient list list:
        """
        while self.user_input:
            self.user_input = self.get_ingredient_from_user()
            if self.user_input:
                self.ingredient_list.append(self.user_input)
        return self.ingredient_list

    def check_ingredient_list(self):
        """
        Make sure the user has entered at least one ingredient
        :return ingredient list list:
        """
        while not self.ingredient_list:
            print "Ha ha, wiseguy.  Now enter an ingredient."
            self.user_input = True
            self.prompt_user_for_ingredients()
        return "Wiseguy."

    def display_ingredient_list(self):
        """
        Format the display of the ingredients
        :return None:
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

    def display_http_errors(self, response):
        """
        A thin wrapper around the HTTP Response to display
        more meaningful error messages to the user.
        :param response: http response
        :return error object:
        """
        if response.status_code == 403:
            error_message = "Access to Food2Fork has been denied.  " \
                  "This may be due to an incorrect API key," \
                  "a lapsed account, etc." \
                  "Error code from F2F server: {0}".format(response.reason)
            print error_message
            return {'status_code': response.status_code,
                    'reason': response.reason,
                    'error_message': error_message}
        if response.status_code == 404:
            error_message = "The resource on Food2Fork is missing.  " \
                            "Maybe the url to F2F got changed?" \
                            "The current stored url is {1}" \
                            "Error code from F2F server: {0}".format(response.reason,
                                                                     self.f2f_search_url)
            print error_message
            return {'status_code': response.status_code,
                    'reason': response.reason,
                    'error_message': error_message}
        if response.status_code == 500:
            error_message = "Server Error." \
                  "It looks like something went wrong on the F2F server." \
                  "Error code from F2F server: {0}".format(response.reason)
            print error_message
            return {'status_code': response.status_code,
                    'reason': response.reason,
                    'error_message': error_message}
        if response.status_code == 504:
            error_message = "Server Error." \
                            "It looks like something went wrong on the F2F server." \
                            "Error code from F2F server: {0}".format(response.reason)
            print error_message
            return {'status_code': response.status_code,
                    'reason': response.reason,
                    'error_message': error_message}
        return {'status_code': response.status_code,
                'reason': response.reason,
                'error_message': response.reason}

    def search_by_ingredients(self, ingredient_list):
        """
        Query F2F's Search API using an HTTP request.
        Annoyingly, F2F only accepts a list of ingredients as an url-encoded string.
        Returns the first recipe, as we're sorting on rating
        :param ingredient_list:
        :return id of first recipe found or None:
        """
        if not ingredient_list:
            return None
        ingredients_string = ",".join(ingredient_list)
        print "Searching recipes with these ingredients on F2F..."
        payload = urllib.urlencode({'key': self.f2f_api_key,
                                    'q': ingredients_string,
                                    'sort': 'r'})
        response = requests.post(self.f2f_search_url, data=payload)
        if response.status_code != 200:
            self.display_http_errors(response)
            print "Quitting."
            sys.exit(1)
        if response.json().get('error') == 'limit':
            print "You have reached the maximum API limit for the day. \n" \
                  "Go ahead and create a new F2F account using a Mailinator email - \n" \
                  "F2F doesn't even blacklist @mailinator.com addresses.  Heck, \n" \
                  "you don't even have to get a validation code - F2F just logs you in. \n" \
                  "Then paste your new, shiny API Key into apikey.conf.  I'm actually \n" \
                  "kinda tempted to automate this process and simply scrape \n" \
                  "the API Key off their site.  $0 Enterprise Plan anyone?  \n" \
                  "I mean, you could pay actual dollars, \n" \
                  "but for this API?  They're just scraping other peoples' sites. \n\n" \
                  "And poorly, at that.  Try doing a search for 'Coca-Cola'. Go ahead. I'll wait."
            sys.exit(1)
        recipe_id = None
        if len(response.json().get('recipes')):
            recipe_id = response.json().get('recipes')[0].get('recipe_id')
        else:
            print "Could not find any recipes with all of these ingredients. " \
                  "Try removing a couple of ingredients to see if there are other, " \
                  "simpler recipes."
        return recipe_id

    def get_recipe_by_id(self, recipe_id):
        """
        Query F2F's Recipe Details API using an HTTP request.
        Returns Detail view of the recipe as JSON
        :param recipe_id:
        :return recipe json:
        """
        print "Retrieving recipe from F2F..."
        payload = urllib.urlencode({'key': self.f2f_api_key,
                                    'rId': recipe_id})
        response = requests.post(self.f2f_detail_url, data=payload)
        if response.status_code != 200:
            self.display_http_errors(response)
            print "Quitting."
            sys.exit(1)
        recipe = None
        if response.json().get('recipe'):
            recipe = response.json().get('recipe')
        else:
            print "Could not find a recipe with this id. "
        print "  ...Done."
        return recipe


class RecipeMgr:
    """
    Class with methods for dealing with recipes
    Expects a recipe for initialization
    """
    def __init__(self, recipe):
        self.recipe = recipe
        self.all_ingredients = self.recipe.get('ingredients')
        self.searched_for_ingredients = []
        self.missing_ingredients_list = []

    def set_searched_for_ingredients(self, ingredient_list):
        """
        Finds the searched-for ingredient among the recipe's ingredient list
        and returns a list with the full name of the ingredient
        There's a lot of looping here.  Might try using Pandas Series findall function
        if it takes too long.  On the other hand, we shouldn't be dealing with
        hundreds of ingredients, so this might be good enough.
        :param ingredient_list:
        :return searched for ingredient:
        """
        for search_ingredient in ingredient_list:
            for ingredient in self.all_ingredients:
                if search_ingredient in ingredient:
                    self.searched_for_ingredients.append(ingredient)
        return self.searched_for_ingredients

    def diff_ingredient_lists(self):
        """
        Turn both the recipe's ingredient list and the searched-for-list into sets
        Then get the difference of the two - these are the missing ingredients.
        Pretty clever, eh?  Eh??? Well, I thought so, anyway.
        :return missing ingredient list:
        """
        missing_ingredients_set = set(self.all_ingredients).\
            difference(self.searched_for_ingredients)
        self.missing_ingredients_list = list(missing_ingredients_set)
        return self.missing_ingredients_list

    def display_missing_ingredients(self):
        """
        Format the missing ingredients nicely
        :return:
        """
        print 'Missing Ingredients for "{0}":'.format(self.recipe.get('title'))
        print "****************************************"
        for i, missing_ingredient in enumerate(self.missing_ingredients_list, 1):
            print "  {i}) {missing_ingredient}"\
                .format(i=i, missing_ingredient=missing_ingredient)
        print "****************************************"
        print

def main():
    app_mgr = AppMgr()
    req_mgr = RequestMgr(app_mgr.f2f_api_key)
    while app_mgr._continue:
        ing_mgr = IngredientMgr()
        ing_mgr.prompt_user_for_ingredients()
        ing_mgr.check_ingredient_list()
        ing_mgr.display_ingredient_list()
        recipe_id = req_mgr.search_by_ingredients(ing_mgr.ingredient_list)
        if recipe_id:
            recipe = req_mgr.get_recipe_by_id(recipe_id)
            recipe_mgr = RecipeMgr(recipe)
            recipe_mgr.set_searched_for_ingredients(ing_mgr.ingredient_list)
            recipe_mgr.diff_ingredient_lists()
            recipe_mgr.display_missing_ingredients()
        app_mgr.prompt_user_to_search_again()

if __name__ == "__main__":
    main()

__date__ = "2019-02-01"
__version__ = "0.0.1"
__author__ = "Eric Mattison"
__maintainer__ = "Eric Mattison"
__email__ = "emattison@gmail.com"
