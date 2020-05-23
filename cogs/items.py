import discord
from discord.ext import commands
from wowapi import WowApi
from wowapi import WowApiException

class ItemsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Items Cog Loaded.')

    def WowAPI(self, ctx):
        # Connect To Wow API
        api = WowApi(self.bot.configs[str(ctx.guild.id)]['clientID'], self.bot.configs[str(ctx.guild.id)]['clientSecret'])
        return api

    def WowItemAPI(self, ctx, UitemID):
        # Get Item Name And Image Data
        api = self.WowAPI(ctx)
        itemsInfo = api.get_item_data('us', namespace='static-us', id=UitemID, locale='en_US')

        itemname = itemsInfo.get('name')
        quality = itemsInfo.get('quality').get('name')
        level = itemsInfo.get('level')
        required_level = itemsInfo.get('required_level')
        item_class = itemsInfo.get('item_class').get('name')
        item_subclass = itemsInfo.get('item_subclass').get('name')
        inventory_type = itemsInfo.get('inventory_type').get('name')
        level_display_string = itemsInfo.get('preview_item').get('level').get('display_string')
		
        # Rep Stuff
        reputation = itemsInfo.get('preview_item').get('requirements').get('reputation').get('faction').get('name')
        reputation_display_string = itemsInfo.get('preview_item').get('requirements').get('reputation').get('display_string')
        min_reputation_level = itemsInfo.get('preview_item').get('requirements').get('reputation').get('min_reputation_level')

        #self.Debug(itemname)

        itemMedia = api.get_item_media('us', namespace='static-us', id=UitemID, locale='en_US')
        imagelink = ''
        for data2 in itemMedia.get('assets'):
            imagelink = data2.get('value')
        #self.Debug(itemsInfo.get('name'))
        #self.Debug(imagelink)
        return itemname, quality, level, required_level, item_class, item_subclass, \
            inventory_type, level_display_string, reputation, reputation_display_string, \
            min_reputation_level, imagelink

    def WowGold(self, ctx, value):
        if value is not None:
            gold = value / 10000
            value = value % 10000
            silver = value / 100
            copper = value % 100
            return '{:.0f}'.format(gold)+""+self.bot.configs[str(ctx.guild.id)]['goldEmoji']+" "+ \
                   '{:.0f}'.format(silver)+""+self.bot.configs[str(ctx.guild.id)]['silverEmoji']+" "+ \
                   '{:.0f}'.format(copper)+""+self.bot.configs[str(ctx.guild.id)]['copperEmoji']

    @commands.command(name='iteminfo')
    async def get_Auctions(self, ctx, *UitemID):
        """List ItemID By Item Name."""
        if ctx.channel.name == self.bot.configs[str(ctx.guild.id)]['botChannel'] or ctx.channel.id == int(self.bot.configs[str(ctx.guild.id)]['botChannel']):
            try:
                # Namer Or ID Check
                UitemID = (' '.join(UitemID))
                if not UitemID.isdigit():
                    UitemID = self.bot.jsonData['itemsdb'][UitemID]
                self.Debug(UitemID)
                if UitemID.isdigit():
                    UitemID = UitemID

                # Request Python Wow API
                self.Debug('Requesting WoW API.')
                await ctx.send('Searching Items....')
                 # Get Item Name And Image
                itemname, quality, level, required_level, item_class, item_subclass, \
                    inventory_type, level_display_string, reputation, reputation_display_string, \
                    min_reputation_level, imagelink = self.WowItemAPI(ctx, UitemID)
                itemURL = 'https://www.wowhead.com/item=' + str(UitemID)
                output = '['+str(UitemID)+']\n'+'['+quality+']\n'+'['+str(level)+']\n'+'['+str(required_level)+']\n'+'['+item_class+']\n'+'['+item_subclass+']\n'+'['+inventory_type+']\n'+'['+level_display_string+']\n' + \
				         '['+reputation+']\n'+'['+reputation_display_string+']\n'+'['+str(min_reputation_level)+']\n'
                embed = discord.Embed(description=output, colour=0x98FB98)
                embed.set_author(name=str(itemname) + ' - ['+UitemID+']', url=itemURL, icon_url=imagelink)
                await ctx.send(embed=embed)

            # Error Handleing
            except WowApiException as werror:
                self.Debug('WowAPI Error: ' + str(werror))
                embed = discord.Embed(description=str(werror), colour=0xFF0000)
                embed.set_author(name='WowAPI Error')
                await ctx.send(embed=embed)
            except KeyError as kerror:
                self.Debug('Key Error: ' + str(kerror))
                embed = discord.Embed(description=str(kerror), colour=0xFF0000)
                embed.set_author(name='Key Error')
                await ctx.send(embed=embed)
            except (RuntimeError, AttributeError, SyntaxError, ImportError, ReferenceError, NameError, Warning) as error:
                self.Debug(error)
                embed = discord.Embed(description=str(error), colour=0xFF0000)
                embed.set_author(name='Wowbot Encountered An Error')
                await ctx.send(embed=embed)

    def Debug(self, value):
        print(value)

def setup(bot):
    bot.add_cog(ItemsCog(bot))
