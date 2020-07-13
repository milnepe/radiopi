import json
from pathlib import Path


def get_countries(cities: list) -> dict:
    """Returns a dict of country: [list_of_cities] for all cities
    in a cities list. US uses COUNTRY-STATE format"""
    countries = dict()
    for c in cities:
        country = c.split(',')  # last part is country / country-state
        if country[1] not in countries:
            countries[country[1]] = [c]
        else:
            countries[country[1]].append(c)
    return countries


if __name__ == "__main__":
    data = Path(r'../etc/radiopi/stations.json')

    with data.open(mode='r', encoding='utf-8') as f:
        stations_dict = json.load(f)

    cities_list = sorted(stations_dict)
    print(cities_list)

    print("_____________________")

    countries_dict = get_countries(sorted(stations_dict))
    print(countries_dict)
    print("______________________")

    countries_list = sorted(countries_dict)
    print(countries_list)

    cities = countries_dict['AT']
    print(cities)
