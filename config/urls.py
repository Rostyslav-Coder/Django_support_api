"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import json
from dataclasses import asdict, dataclass

import requests
from django.conf import settings  # pylint: disable=E0401
from django.contrib import admin  # pylint: disable=E0401
from django.http import HttpResponse, HttpResponseNotFound  # pylint: disable=E0401
from django.urls import path  # pylint: disable=E0401


def filter_by_keys(sourse: dict, keys: list[str]) -> dict:
    filtered_data = {}

    for key, value in sourse.items():
        if key in keys:
            filtered_data[key] = value

    return filtered_data


@dataclass
class Pokemon:
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
    """Take pokemon from the cache or
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
    elif request.method == "DELETE":
        pokemon: Pokemon = _del_pokemon(name)

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(asdict(pokemon)),
    )


def get_pokemon_for_mobile(request, name: str):
    if request.method == "GET":
        pokemon: Pokemon = _get_pokemon(name)
    elif request.method == "DELETE":
        pokemon: Pokemon = _del_pokemon(name)

    result = filter_by_keys(
        asdict(pokemon),
        ["id", "name", "base_experience"],
    )

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(result),
    )


def get_all_pokemons(request) -> dict[str, dict]:
    if request.method == "GET":
        all_pokemons = {}

        for key, value in POKEMONS.items():
            all_pokemons[key] = asdict(value)

        return HttpResponse(
            content_type="application/json", content=json.dumps(all_pokemons)
        )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/pokemons/<str:name>/", get_pokemon),
    path("api/pokemons/mobile/<str:name>/", get_pokemon_for_mobile),
    path("api/pokemons/", get_all_pokemons),
]
