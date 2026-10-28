"""Lädt ein Rezept aus einer JSON-Datei als eigenes Rezept in Cookidoo hoch.

Aufruf: python upload_recipe.py rezepte/omas-vanillekipferl.json
Zugangsdaten kommen aus COOKIDOO_EMAIL und COOKIDOO_PASSWORD.
"""

import asyncio
import json
import os
import sys

from aiohttp import ClientSession, CookieJar
from cookidoo_api import Cookidoo, CookidooConfig
from cookidoo_api.helpers import get_localization_options
from cookidoo_api.types import CookidooCreateCustomRecipe


async def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    email = os.environ.get("COOKIDOO_EMAIL")
    password = os.environ.get("COOKIDOO_PASSWORD")
    if not email or not password:
        sys.exit("COOKIDOO_EMAIL und COOKIDOO_PASSWORD sind nicht gesetzt.")

    localization = (await get_localization_options(country="de", language="de-DE"))[0]
    cfg = CookidooConfig(localization=localization, email=email, password=password)

    async with ClientSession(cookie_jar=CookieJar(unsafe=True), trust_env=True) as session:
        cookidoo = Cookidoo(session, cfg)
        await cookidoo.login()
        recipe = await cookidoo.create_custom_recipe(
            CookidooCreateCustomRecipe(
                name=data["name"],
                ingredients=data["ingredients"],
                instructions=data["instructions"],
                serving_size=data["serving_size"],
                active_time=data["active_time"],
                total_time=data["total_time"],
                unit_text=data.get("unit_text", "portion"),
                hints=data.get("hints", []),
            )
        )
        print(f"Hochgeladen: {recipe.name} (ID {recipe.id})")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
