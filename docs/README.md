# iRobot F2F App
> Check Food2Fork for the most popular recipes using a list of ingredients

Prompt a user to enter a list of ingredients.  Using the ingredient list, query F2F's web API for the top recipe found and list any missing ingredients.

## Installation

OS X & Linux:
* Change directory to irobotf2f directory
```
cd /path/to/irobotf2f
```
* Create Virtual Environment using Python 2.7.x
```
python -m virtualenv env
```
* Activate Virtual Environment
```
source env/bin/activate
```
* Run setup
```
python setup.py install
```

Windows:
* Change directory to irobotf2f directory
```
cd C:\path\to\irobotf2f
```
* Create Virtual Environment using Python 2.7.x
```
py -m virtualenv env
```
* Activate Virtual Environment
```
.\env\Scripts\activate
```
* Run setup
```
python setup.py install
```

## Usage example
Basic Usage:
```
cd irobotf2f
python __init__.py
```

## Release History
* 0.0.12
    * Unit tests passing

* 0.0.1
    * Work in progress

## Meta

Distributed under MIT Public license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/eric02138/irobotf2f/fork>)
2. Create your feature branch (`git checkout -b feature/someaddition`)
3. Commit your changes (`git commit -am 'Add someaddtion'`)
4. Push to the branch (`git push origin feature/someaddition`)
5. Create a new Pull Request
