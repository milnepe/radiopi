#!/usr/bin/env python3

"""A rotary-encoder controlled internet radio player.

Station information is loaded from a configuration file.

Starts by playing the last station selected. Then presents
a scrollable list of countries, each time the encoder is rotated.

Pressing the encoder button selects a country which then presents a
scrollable list of cities for that country.

Pressing the encoder button selects a city which then presents a
scrollable list of stations for that city.

Pressing the encoder button again, plays the current station and returns
to the list of locations. So everything starts over again.
"""

import json
from pathlib import Path
import evdev
import select
from streaming import Streamer
import argparse
from countries import get_countries


def get_encoder_value(value: int, alist: list) -> int:
    """Return a value in range of the list. Allows value to wrap round"""
    if value in range(len(alist)):  # increasing values
        value = value
    elif value < 0:  # decreasing values
        value = len(alist) + value
    else:  # wrap
        value = 0
    return value


def save_station(station: dict, last_station_file: str):
    """Saves last station played dict to file"""
    with Path(last_station_file).open(mode='w', encoding='utf-8') as f:
        json.dump(station, f)


def get_last_station(last_station_file: str) -> dict:
    """Returns dict containing last station played from file"""
    with Path(last_station_file).open(mode='r', encoding='utf-8') as f:
        return json.load(f)


def parse_command_line_args():
    parser = argparse.ArgumentParser(description=('Raspberry Pi Radio player'))
    parser.add_argument('--audio', default='alsa',
                        help=('Audio output, "alsa" or "pulse"'))
    parser.add_argument('--stations', default='stations.json',
                        help=('Path to Stations file'))
    parser.add_argument('--last_station', default='station.json',
                        help=('Path to Last Station file'))
    return parser.parse_args()


args = parse_command_line_args()

with Path(args.stations).open(mode='r', encoding='utf-8') as f:
    stations_dict = json.load(f)

countries_dict = get_countries(sorted(stations_dict))
countries_list = sorted(countries_dict)

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
devices = {dev.fd: dev for dev in devices}

# play last station
try:
    audio = args.stations
    station = get_last_station(args.last_station)
    name = station['name']
    print(f'Last Station: {name}')
    streamer = Streamer(audio, station['url'])
    streamer.play()
except:
    pass

# initialise stations
state = 'countries'
value = 0
old_country = 0
old_location = 0
country = countries_list[0]
location = 0
print(f'Country: {country}')

while True:
    r, w, x = select.select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            event = evdev.util.categorize(event)
            if isinstance(event, evdev.events.RelEvent):
                value = value + event.event.value
                if state == 'countries':  # scroll through countries
                    value = get_encoder_value(value, countries_list)
                    country = countries_list[value]
                    print(f'Country: {country}')
                if state == 'locations':  # scroll through locations
                    value = get_encoder_value(value, locations)
                    location = locations[value]
                    print(f'Location: {location}')
                if state == 'stations':  # scroll through stations
                    value = get_encoder_value(value, stations_list)
                    station = stations_list[value]
                    name = station.get('name')
                    print(f'Station: {name}')
            elif isinstance(event, evdev.events.KeyEvent):
                if event.keycode == "KEY_ENTER" and event.keystate == event.key_up:
                    if state == 'countries':
                        state = 'locations'
                        old_country = value
                        value = 0
                        # grab list of locations
                        locations = sorted(countries_dict[country])
                        location = locations[value]
                        print(f'Location: {location}')
                    elif state == 'locations':
                        state = 'stations'
                        value = 0
                        # grab list of stations
                        stations_list = stations_dict[location]['urls']
                        print(stations_list)
                        station = stations_list[value]
                        name = station.get('name')
                        print(f'Station: {name}')
                    elif state == 'stations':
                        state = 'countries'
                        # play the station
                        save_station(station, args.last_station)
                        url = station.get('url')
                        print(f'URL: {url}')
                        try:
                            streamer.stop()
                        except:
                            pass
                        streamer = Streamer(audio, url)
                        streamer.play()
                        value = old_country
                        print(f'Country: {country}')
