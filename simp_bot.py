import datetime

import discord
from discord.ext import commands

from commands.feli_points.feli_points import FeliPoints
from commands.generic.taylor import Taylor
from utils.get_secret import get_secret

secret_name = 'simp/rds'
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

bot.add_cog(FeliPoints(bot))
bot.add_cog(Taylor(bot))


@bot.command()
async def culo(ctx):
    """Returns time in which rick hasn't licked Ximena's ass."""

    today = datetime.datetime.now()
    start_date = datetime.datetime(2020, 10, 10)
    diff = today - start_date
    days, seconds = diff.days, diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    await ctx.send(
        'Rick no le ha chupado el culo a Ximena  en {} dias, {} horas, {} minutos y {} segundos'.format(days, hours,
                                                                                                        minutes,
                                                                                                        seconds))


bot.run(get_secret('simp/bot-token')['token'])
