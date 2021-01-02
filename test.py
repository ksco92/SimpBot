import datetime
import glob
import random

import discord
import matplotlib.pyplot as plt
import pandas as pd
from discord.ext import commands
from prettytable import PrettyTable

from get_secret import get_secret
from run_query import run_query

secret_name = 'simp/rds'
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


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


@bot.command()
async def taylor(ctx):
    """Returns a random taylor song snippet."""

    files = glob.glob("taylor_lyrics/*.txt")
    chosen_file = random.choice(files)
    with open(chosen_file, 'r') as file:
        song = file.read().replace('\n', '')
        file.close()

    await ctx.send(song)


def is_valid_user(user_nickname):
    """Checks if the nickname of a user is valid."""

    secret = get_secret(secret_name)
    query = """select custom_nickname
               from users
               where custom_nickname = '{}'""".format(user_nickname)
    results = run_query(secret['host'], secret['username'], secret['password'], secret['dbInstanceIdentifier'], query,
                        returns_results=True)

    if len(results) == 1:
        return True
    else:
        return False


@bot.command()
async def felipoint(ctx, amount, recipient, type):
    """<amount> <recipient> <type>: Adds or removes a feli points to a user."""

    help_text = 'Usage is ```!felipoint <amount> <recipient> <type>```'

    if type not in ['add', 'remove']:
        await ctx.send('Invalid transaction type!')
        await ctx.send(help_text)
        return None

    if not is_valid_user(recipient):
        await ctx.send('Invalid point recipient!')
        await ctx.send(help_text)
        return None

    try:
        int(amount)
    except ValueError:
        await ctx.send('Amount must be an integer number!')
        await ctx.send(help_text)
        return None

    secret = get_secret(secret_name)

    query = """insert into feli_point_transactions (discord_user_id, type, amount, given_by)
               select discord_user_id, '{}', '{}', '{}'
               from users
               where custom_nickname = '{}'""".format(type, amount, ctx.message.author, recipient)
    run_query(secret['host'], secret['username'], secret['password'], secret['dbInstanceIdentifier'], query,
              auto_commit=True)

    await ctx.send('Transaction completed :eggplant:')

    return None


@bot.command()
async def pointbalance(ctx):
    """Returns balance and transaction history of feli points."""

    secret = get_secret(secret_name)
    query = """select * from feli_point_balance"""
    results = run_query(secret['host'], secret['username'], secret['password'], secret['dbInstanceIdentifier'], query,
                        returns_results=True, return_column_names=True)

    table = PrettyTable()

    table.field_names = results[0]

    for row in results[1:]:
        table.add_row(row)

    df = pd.DataFrame(results[1:], columns=results[0])
    df = df.set_index('custom_nickname')
    for i in range(len(df)):
        plt.plot([k for k in df.columns if k != 'total_balance'],
                 [int(df[y].iloc[i]) for y in df.columns if y != 'total_balance'])
    plt.legend(df.index, loc="upper left")
    plt.savefig('balance.png')

    await ctx.send('```{}```'.format(table), file=discord.File('balance.png'))


bot.run(get_secret('simp/bot-token')['token'])
