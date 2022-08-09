# Baato Python Library
![Build](https://github.com/baato/python-client/actions/workflows/baato_test.yml/badge.svg) ![Supported](https://img.shields.io/badge/python-3.6%2C%203.7%2C%203.8%2C%203.9%2C%203.10-blue) ![License](https://img.shields.io/badge/License-MIT-green.svg)

The Python library makes it easy to consume the Baato API into existing python projects.

## Installation
Baato Python can be installed from PyPI with tools like ``pip``:

```bash
$ pip install baato
```

## Features

The Baato Python client library makes it easy to integrate the [Baato API](https://baato.io) into existing python projects. This package acts as a wrapper for the following Baato services:

- [Search API](https://docs.baato.io/#/v1/services/search)
- [Reverse Search API](https://docs.baato.io/#/v1/services/reverse)
- [Places API](https://docs.baato.io/#/v1/services/places)
- [Nearby Places API](https://docs.baato.io/#/v1/services/nearby_places)
- [Directions API](https://docs.baato.io/#/v1/services/directions)
- [Map Styles API](https://docs.baato.io/#/v1/services/styles)

## Usage
### Search API
After initializing Baato with your access token, the `search()` method can be used to make requests to the Search API.
```python
from baato import BaatoClient

client = BaatoClient(access_token="YOUR_ACCESS_KEY")

"""Optional Initilization Parameters

- endpoint="https://api.baato.io/api" # default
- version="v1" # default
"""

response = client.search(q="kathmandu")
print(response["data"])
print(response["status"])

"""Optional Search Parameters

- lat and lon =>(float) latitude and longitude coordinates. Useful in mobile applications for providing geographical context to the search. 
- type =>(str) The type or category of results that the request should return. For example: hospital, cafe etc.
- radius =>(int)  Radius, in kilometers from the specified lat/lon pair within which to look for results. Only integer values supported. By default the value is set to 10.
- limit =>(int) The number of results that the request should return. By default the value is set to 5.
"""
```

### Reverse Search API
After initializing Baato with your access token, the `reverse()` method can be used to make requests to the Reverse Search API.
```python
from baato import BaatoClient

client = BaatoClient(access_token="YOUR_ACCESS_KEY")

""" Optional Initilization Parameters

- endpoint="https://api.baato.io/api" # default
- version="v1" # default
"""

response = client.reverse(lat=27.70446921370009,lon=85.32051086425783)
print(response["data"])
print(response["status"])

"""Optional Reverse Parameters

- radius =>(int) A proxy variable for the inaccuracy, denoting how close around the coordinates should the algorithm look for potential address nodes.
- limit =>(int) The number of results to be returned; defaults to 1.
"""
```

### Places API
After initializing Baato with your access token, the `places()` method can be used to make requests to the Places API.
```python
from baato import BaatoClient

client = BaatoClient(access_token="YOUR_ACCESS_KEY")

""" Optional Initilization Parameters

- endpoint="https://api.baato.io/api" # default
- version="v1" # default
"""

response = client.places(place_id=100006)
print(response["data"])
print(response["status"])
```

### NearbyPlaces API
After initializing Baato with your access token, the `near_by()` method can be used to make requests to the NearbyPlaces API.
```python
from baato import BaatoClient

client = BaatoClient(access_token="YOUR_ACCESS_KEY")

""" Optional Initilization Parameters

- endpoint="https://api.baato.io/api" # default
- version="v1" # default
"""

response = client.near_by(lat=27.717245, lon=85.323959, type="school")
print(response["data"])
print(response["status"])

"""Here is the list for merged feature types:
- eat => Returns results for cafe, restaurant, bakery
- grocery => Returns results for department_store, supermarket
- tourism => Returns results for attraction, artwork, museum,park
- transport => Returns results for bus_stop, bus_station
- parking => Returns results for parking, bicycle_parking, underground,multi-storey, parking_space, car_parking
- shopping => Returns results for jewelry, sports, gift ,mall,department_store,hardware,kitchen, furniture
- children => Returns results for swimming_pool, playground, recreation_ground, park, water_park, disneyland
- night_life => Returns results for pub, bar, nightclub
- entertainment => Returns results for cinema, theatre, casino, nightclub
- clinic => Returns results for clinic, dentist, veterinary, herbalist, ayurvedic
- workshop => Returns results for metal, bicycle, aluminium, car_repair, tyres, car_parts
"""

"""Optional Near By Parameters

- radius =>(int) Radius, in kilometers from the specified lat/lon pair within which to look for results. Only integer values supported. By default the value is set to 10.
- limit =>(int) The number of results that the request should return. By default the value is set to 5.
"""
```
### Directions API
After initializing Baato with your access token, the `direction()` method can be used to make requests to the Directions API.
```python
from baato import BaatoClient

client = BaatoClient(access_token="YOUR_ACCESS_KEY")

""" Optional Initilization Parameters

- endpoint="https://api.baato.io/api" # default
- version="v1" # default
"""

response = client.direction(points=["27.71772,85.32784", "27.73449,85.33714"], mode="car")
print(response["data"])
print(response["status"])
"""Here is the availabe mode:
- car
- bike
- foot
"""

"""Optional Near By Parameters

- alternatives =>(boolen) enable alternatives by setting alternatives=true.
- instructions =>(boolen) enable instructions by setting instructions=true.

```

### Map Styles API
After initializing Baato with your access token, the `map_style()` method can be used to make requests to the Map Styles API.
```python
from baato import BaatoClient

client = BaatoClient(access_token="YOUR_ACCESS_KEY")

""" Optional Initilization Parameters

- endpoint="https://api.baato.io/api" # default
- version="v1" # default
"""

response = client.map_style(style_name="monochrome")
print(response["data"])
print(response["status"])

"""Here is the availabe style_name:
- monochrome
- breeze
- dark
- black_white
- roads
- retro
"""
```

## Contributing

[![Baato](https://user-images.githubusercontent.com/24504319/183284839-082b8253-2e75-4487-bcf5-8d1475f2e85f.png)](https://baato.io/)

### Development Environment
Fork the repository

Once you have forked this repository to your own GitHub account, install your
own fork in your development environment:

```bash
$ git clone git@github.com:<your_fork>/python-client.git
$ cd python-client
```
```bash
$ pip install -r requirements.txt
```
#### Running the tests

Test all supported versions
You can also use the excellent tox testing tool to run the tests against all supported versions of Python. Install tox, and then simply run:
```bash
$ pip install tox
```
In the tox.ini file update your `YOUR_BAATO_ACCESS_TOKEN` then.
```bash
$ tox

```
