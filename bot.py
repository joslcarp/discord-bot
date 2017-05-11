import discord
from discord.ext import commands
from urllib.parse import urlencode
import random
import aiohttp

import secrets

bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# Retrieve query results from Wolfram Short Answer API
@bot.command(aliases=['eval'])
async def wolfram(*query):
    url = ('https://api.wolframalpha.com/v1/result?{}%3f'
           '&appid={}'.format(urlencode({'i': ' '.join(query)}), secrets.wolfram_id))
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        content = await response.read()
    await bot.say(content)

# Search Python3 Docs
@bot.command(aliases=['pyh'])
async def py_help(*query):
    url = ('https://docs.python.org/3/search.html?{}'
           '&check_keywords=yes&area=default'.format(urlencode({'q': ' '.join(query)})))
    await bot.say(url)

# Roll dice in NdN format
@bot.command()
async def roll(dice : str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

# Pick random choice from 2
@bot.command(description='Heads or tails')
async def choose(*choices : str):
    await bot.say(random.choice(choices))

# Repeat a message N times
@bot.command()
async def repeat(times : int, content='repeating...'):
    for i in range(times):
        await bot.say(content)

# Lookup user join timestamp on server
@bot.command()
async def joined(member : discord.Member):
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

# Run the bot
bot.run(secrets.discord_token)
