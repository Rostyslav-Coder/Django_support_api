"""This is my API to DET & DELETE Pokemons from Pokeapi."""


import json
from dataclasses import asdict, dataclass

import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import path


def filter_by_keys(sourse: dict, keys: list[str]) -> dict:
    filtered_data = {}

    for key, value in sourse.items():
        if key in keys:
            filtered_data[key] = value

    return filtered_data


@dataclass
class Pokemon:
    """Class to create Pokemons"""

    id: int
    name: str
    height: int
    weight: int
    base_experience: int

    @classmethod
    def from_raw_data(cls, raw_data: dict) -> "Pokemon":
        filtered_data = filter_by_keys(
            raw_data,
            cls.__dataclass_fields__.keys(),  # pylint: disable=E1101
        )

        return cls(**filtered_data)


# CACHE SIMULATOR
POKEMONS: dict[str, Pokemon] = {}


def get_pokemon_from_api(name: str) -> Pokemon:
    url = settings.POKEAPI_BASE_URL + f"/{name}"
    response = requests.get(url, timeout=5)
    raw_data = response.json()

    return Pokemon.from_raw_data(raw_data)


def _get_pokemon(name) -> Pokemon:
    """
    Take pokemon from the cache or
    get it from the API and then save it to thhe cache.
    """

    if name in POKEMONS:
        pokemon = POKEMONS[name]
    else:
        pokemon: Pokemon = get_pokemon_from_api(name)
        POKEMONS[name] = pokemon

    return pokemon


def _del_pokemon(name):
    """Delete pokemon from the cache"""

    return POKEMONS.pop(name)


def get_pokemon(request, name: str):
    if request.method == "GET":
        pokemon: Pokemon = _get_pokemon(name)

        return HttpResponse(
            content_type="application/json",
            content=json.dumps(asdict(pokemon)),
        )

    elif request.method == "DELETE":
        if name in POKEMONS:
            pokemon: Pokemon = _del_pokemon(name)
        else:
            return HttpResponseNotFound("Object not found")


def get_pokemon_for_mobile(request, name: str):
    if request.method == "GET":
        pokemon: Pokemon = _get_pokemon(name)

        result = filter_by_keys(
            asdict(pokemon),
            ["id", "name", "base_experience"],
        )

        return HttpResponse(
            content_type="application/json",
            content=json.dumps(result),
        )

    elif request.method == "DELETE":
        if name in POKEMONS:
            pokemon: Pokemon = _del_pokemon(name)
        else:
            return HttpResponseNotFound("Object not found")


def get_all_pokemons(request) -> dict[str, dict]:
    if request.method == "GET":
        all_pokemons = {}

        for key, value in POKEMONS.items():
            all_pokemons[key] = asdict(value)

        return HttpResponse(
            content_type="application/json",
            content=json.dumps(all_pokemons),
        )


urlpatterns = [
    path("api/pokemons/<str:name>/", get_pokemon),
    path("api/pokemons/mobile/<str:name>/", get_pokemon_for_mobile),
    path("api/pokemons/", get_all_pokemons),
]
