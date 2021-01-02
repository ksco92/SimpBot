import glob
import random

from discord.ext import commands


class Taylor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def taylor(self, ctx):
        """Returns a random taylor song snippet."""

        files = glob.glob("taylor_lyrics/*.txt")
        chosen_file = random.choice(files)
        with open(chosen_file, 'r') as file:
            song = file.read().replace('\n', '')
            file.close()

        await ctx.send(song)
