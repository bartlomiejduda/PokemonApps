
"""
Copyright © 2021  Bartłomiej Duda
License: GPL-3.0 License
"""

# Ver    Date        Author               Comment
# v0.1   28.04.2021  Bartlomiej Duda      -


import json
from nameko.web.handlers import http
import requests
import logging

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger('nameko_logger')


class PokemonService:
    name = "pokemon_service"

    @http('GET', '/get/<int:pokemon_number>')
    def get_method(self, request, pokemon_number):

        try:
            response = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(pokemon_number))
        except requests.exceptions.Timeout:
            log_msg = "Timeout has occured."
            log.exception(log_msg)
            return log_msg
        except requests.exceptions.TooManyRedirects:
            log_msg = "Bad URL. Please try a different one."
            log.exception(log_msg)
            return log_msg
        except requests.exceptions.RequestException as e:
            log_msg = "Request exception. Exiting..."
            log.exception(log_msg)
            raise SystemExit(e)

        if response.status_code != 200:
            log_msg = "Error has occured. Status code: " + str(response.status_code)
            log.exception(log_msg)
            return log_msg

        response_formatted = json.dumps(response.json(), indent=4, sort_keys=True)
        response_parsed = json.loads(response_formatted)

        moves_json = response_parsed["moves"]

        moves_list = []
        for move in moves_json:
            move_formatted = json.dumps(move, indent=4, sort_keys=True)
            move_parsed = json.loads(move_formatted)
            move_name = move_parsed["move"]["name"]
            moves_list.append(move_name)

        moves_list.sort()

        out_moves_json = json.dumps(moves_list)

        return out_moves_json

