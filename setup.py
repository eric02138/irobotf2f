# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup

def create_api_key_file():
      """Uses user input to create an api key file in a pseudo-secure place.  This has
      been done to make the install easier/usability.
      In a real-world scenario, this would not be anywhere near secure enough.
      Previously, I have stored sensitive information using private-public encrypted files
      that were a) only accessible by the web server and sysadmins and b) in a
      secure section of the server (or, even better, stored on a dedicated secure key
      manager).
      Still, I didn't want to store sensitive information in the repo.  And since the API
      key should be different for each user, prompting the user for their key makes sense.
      """
      print
      print "This application requires an API key from food2fork (https://www.food2fork.com/)."
      has_api_key = raw_input("Do you have an API key? (y/n): ")
      while has_api_key.lower()[0:1] != "y" and has_api_key.lower()[0:1] != "n":
            has_api_key = raw_input("Sorry, but I don't understand. Please try again. (y/n): ")
      if has_api_key.lower()[0:1] == "n":
            print """To get an API Key, first go to https://www.food2fork.com/ and create 
      an account."""
            print """Once you have an account, log in and go to
      https://www.food2fork.com/about/api. Your API Key can be copied from the
      section marked 'Your API Details'. Then re-run this installer."""
            print "See you soon!"
            sys.exit()

      user_supplied_key = raw_input("Great! Please enter it now:").strip()
      while len(user_supplied_key) != 32 and user_supplied_key.lower()[0:4] != "quit":
            print "Hmm.  That doesn't look right.  Your key should be a 32-character string."
            user_supplied_key = raw_input("Why don't you try again? (Enter 'quit' to quit):") \
                  .strip()
      if "quit" in user_supplied_key.lower():
            print "See you soon!"
            sys.exit()

      print "You have entered '{0}'.".format(user_supplied_key)

      # f2f_api_key_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
      # print f2f_api_key_dir
      # f2f_api_key_dir = os.path.abspath(os.path.dirname(__file__))
      f2f_api_key_dir = os.path.dirname(os.path.realpath(__file__))
      f2f_api_key_path = os.path.join(f2f_api_key_dir, 'apikey.conf')

      print "This installer will attempt to create a key file here: {0}".format(f2f_api_key_path)
      try:
            with open(f2f_api_key_path, "w") as f:
                  f.write(user_supplied_key)
      except Exception:
            print "Could not write api key file at {0}".format(f2f_api_key_path)
            print "Quitting."
            raise
      print "Wrote key to {0} successfully.".format(f2f_api_key_path)
      return True

if __name__ == "__main__":
      create_api_key_file()
      setup(name='irobotf2f',
      version='0.0.1',
      description="""Prompt a user to enter a list of ingredients.  Using the ingredient list, 
      query F2F's web API for the top recipe found and list any missing ingredients.""",
      url='http://github.com/eric02138/irobotf2f',
      author='Eric Mattison',
      author_email='emattison@gmail.com',
      license='MIT',
      packages=['irobotf2f'],
      install_requires=[
            "requests"
      ],
      zip_safe=False)