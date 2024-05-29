import aiohttp
import asyncio
import random

pokemon_names = [
    "pikachu", "charmander", "bulbasaur", "squirtle",
    "jigglypuff", "meowth", "psyduck", "machop",
    "gastly", "ditto"
]


async def fetch_pokemon_data(session, name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    async with session.get(url) as response:
        return await response.json()


async def get_pokemon_data(pokemon_names):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon_data(session, name) for name in pokemon_names]
        return await asyncio.gather(*tasks)


def calculate_strength(pokemon):
    stats = pokemon['stats']
    attack = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'attack')
    defense = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'defense')
    speed = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'speed')
    return attack + defense + speed


def battle(pokemon1, pokemon2):
    strength1 = calculate_strength(pokemon1)
    strength2 = calculate_strength(pokemon2)

    if strength1 > strength2:
        winner = pokemon1['name']
    elif strength2 > strength1:
        winner = pokemon2['name']
    else:
        winner = "Draw!"

    return {
        "pokemon1": pokemon1['name'],
        "pokemon2": pokemon2['name'],
        "strength1": strength1,
        "strength2": strength2,
        "winner": winner
    }


async def main():
    pokemon_data = await get_pokemon_data(pokemon_names)

    # Randomly select two Pokémon for the battle
    pokemon1, pokemon2 = random.sample(pokemon_data, 2)

    # Simulate the battle
    result = battle(pokemon1, pokemon2)

    # Output the results
    print(f"Battle between {result['pokemon1']} and {result['pokemon2']}:")
    print(f"{result['pokemon1']} strength: {result['strength1']}")
    print(f"{result['pokemon2']} strength: {result['strength2']}")
    print(f"Winner: {result['winner']}")


# Run the script
if __name__ == "__main__":
    asyncio.run(main())
