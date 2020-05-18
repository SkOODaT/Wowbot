import discord
from discord.ext import commands
from wowapi import WowApi

class ServersCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Servers Cog Loaded.')

    def WowAPI(self, ctx):
        api = WowApi(self.bot.configs[str(ctx.guild.id)]['clientID'], self.bot.configs[str(ctx.guild.id)]['clientSecret'])
        return api

    @commands.command(name='serverstats')
    async def get_Auctions(self, ctx):
        """List Silvermoon And Mok'Nathal Status."""
        if ctx.channel.name == self.bot.configs[str(ctx.guild.id)]['botChannel'] or ctx.channel.id == int(self.bot.configs[str(ctx.guild.id)]['botChannel']):
            try:
                api = self.WowAPI(ctx)
                realms = api.get_connected_realm_index('us', namespace='dynamic-us', locale='en_US')
                realms2 = realms['connected_realms']
                #print(realms2)
                for data in realms2:
                    worlds = data['href']
                    strip1 = worlds.replace('https://us.api.blizzard.com/data/wow/connected-realm/', '')
                    strip2 = strip1.replace('?namespace=dynamic-us', '')
                    wdata = api.get_connected_realm('us', namespace='dynamic-us', id=strip2, locale='en_US')
                    status = wdata['status']['type']
                    #print(wdata['status']['type'])
                    #print(wdata['realms'])
                    for x in wdata['realms']:
                        #print(x['name'])
                        name = x['name']
                        if name == "Silvermoon" or name == "Mok'Nathal":
                            await ctx.send(name + ' ' + strip2 + ' is ' + status)
            except (RuntimeError, AttributeError):
                await ctx.send('Server is not currently available.')

def setup(bot):
    bot.add_cog(ServersCog(bot))
