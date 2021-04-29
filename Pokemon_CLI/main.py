
"""
Copyright © 2021  Bartłomiej Duda
License: GPL-3.0 License
"""

# Ver    Date        Author               Comment
# v0.1   27.04.2021  Bartlomiej Duda      -


import datetime
import argparse
import requests
import json
import logging


def logger(in_str):
    """
    Function for logging debug messages
    """
    now = datetime.datetime.now()
    print(now.strftime("%d-%m-%Y %H:%M:%S") + " " + in_str)


def get_poke_moves(pokemon_number):
    """
    Function for collecting pokemon moves from the PokeApi
    """
    print("Pokemon number: " + str(pokemon_number))

    logging.basicConfig(level=logging.WARNING)
    log = logging.getLogger('main_logger')

    try:
        response = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(pokemon_number))
    except requests.exceptions.Timeout:
        log.exception("Timeout has occured.")
        return 1
    except requests.exceptions.TooManyRedirects:
        log.exception("Bad URL. Please try a different one.")
        return 1
    except requests.exceptions.RequestException as e:
        log.exception("Request exception. Exiting...")
        raise SystemExit(e)

    if response.status_code != 200:
        log.exception("Status code " + str(response.status_code) + ". Exiting.")
        return 1

    response_formatted = json.dumps(response.json(), indent=4, sort_keys=True)
    response_parsed = json.loads(response_formatted)
    print("Pokemon name: " + response_parsed["name"])

    moves_json = response_parsed["moves"]

    moves_list = []
    for move in moves_json:
        move_formatted = json.dumps(move, indent=4, sort_keys=True)
        move_parsed = json.loads(move_formatted)
        move_name = move_parsed["move"]["name"]
        moves_list.append(move_name)

    moves_list.sort()

    print("\nMOVES LIST:")
    move_counter = 0
    for move_name in moves_list:
        move_counter += 1
        print(str(move_counter) + ") " + move_name)

    out_moves_json = json.dumps(moves_list)

    return out_moves_json


def main():
    """
    Main function of this program.
    """
    parser = argparse.ArgumentParser(description='Program to get Pokemon moves.')
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-n', '--number', type=int, metavar='', required='True', help='Number of the Pokemon')
    args = parser.parse_args()

    get_poke_moves(args.number)


if __name__ == '__main__':
    main()