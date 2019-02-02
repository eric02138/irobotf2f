from setuptools import setup

setup(name='irobotf2f',
      version='0.0.1',
      description="""Prompt a user to enter a list of ingredients.  Using the ingredient list, 
      query F2F's web API for the top recipe found and list any missing ingredients.""",
      url='http://github.com/eric02138/irobotf2f',
      author='Eric Mattison',
      author_email='emattison@gmail.com',
      license='MIT',
      packages=['irobot'],
      zip_safe=False)