import discord
import matplotlib.pyplot as plt
import pandas as pd
from discord.ext import commands
from prettytable import PrettyTable
import os

from utils.get_secret import get_secret
from utils.is_valid_user import is_valid_user
from utils.run_query import run_query


class FeliPoints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._secret_name = 'simp/rds'

    @commands.command()
    async def felipoint(self, ctx, amount, recipient, type):
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

        secret = get_secret(self._secret_name)

        query = """insert into feli_point_transactions (discord_user_id, type, amount, given_by)
                   select discord_user_id, '{}', '{}', '{}'
                   from users
                   where custom_nickname = '{}'""".format(type, amount, ctx.message.author, recipient)
        run_query(secret['host'], secret['username'], secret['password'], secret['dbInstanceIdentifier'], query,
                  auto_commit=True)

        await ctx.send('Transaction completed :eggplant:')

        return None

    @commands.command()
    async def pointbalance(self, ctx):
        """Returns balance and transaction history of feli points."""

        secret = get_secret(self._secret_name)
        query = """select * from feli_point_balance"""
        results = run_query(secret['host'], secret['username'], secret['password'], secret['dbInstanceIdentifier'],
                            query, returns_results=True, return_column_names=True)

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
        output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'balance.png')
        plt.savefig(output_file)

        await ctx.send('```{}```'.format(table), file=discord.File(output_file))
