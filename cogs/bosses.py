import discord
from discord.ext import commands
from wowapi import WowApi

class BossesCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Bosses Cog Loaded.')

    def WowAPI(self, ctx):
        api = WowApi(self.bot.configs[str(ctx.guild.id)]['clientID'], self.bot.configs[str(ctx.guild.id)]['clientSecret'])
        return api

    @commands.command(name='bossinfo')
    async def get_skoodat(self, ctx):
        """List Bosses Info."""
        if ctx.channel.name == self.bot.configs[str(ctx.guild.id)]['botChannel'] or ctx.channel.id == int(self.bot.configs[str(ctx.guild.id)]['botChannel']):
            try:
                api = self.WowAPI(ctx)
                bosses = api.get_bosses('us', namespace='static-us', locale='en_US')
                print(bosses)
                await ctx.send('Boss Data')
            except (RuntimeError, AttributeError):
                await ctx.send('Server is not currently available.')

def setup(bot):
    bot.add_cog(BossesCog(bot))
