import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.photo:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.photo.url,
                'title_ru': pokemon.title
            })
        else:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title
            })

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemons_entity = PokemonEntity.objects.all()
        for pokemon_entity in pokemons_entity:
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                pokemon_entity.pokemon.title,
                request.build_absolute_uri(pokemon_entity.pokemon.photo.url))

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon = Pokemon.objects.get(id=pokemon_id)
    pokemon_info = {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.photo.url,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description
    }

    if pokemon.previous_evolution:
        pokemon_info.update({
            'previous_evolution': {
                'pokemon_id': pokemon.previous_evolution.id,
                'img_url': pokemon.previous_evolution.photo.url,
                'title_ru': pokemon.previous_evolution.title
            }}
        )

    next_evolutions = pokemon.next_evolutions.all().first()
    if next_evolutions:
        pokemon_info.update({
            'next_evolution': {
                'pokemon_id': next_evolutions.id,
                'title_ru': next_evolutions.title,
                'img_url': next_evolutions.photo.url
            }
        })

    pokemons_entity = PokemonEntity.objects.filter(pokemon=pokemon)
    for pokemon_entity in pokemons_entity:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url))
    return render(request, "pokemon.html", context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_info
    })
