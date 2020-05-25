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
        # Get Item Info Data
        api = self.WowAPI(ctx)
        itemsInfo = api.get_item_data('us', namespace='static-us', id=UitemID, locale='en_US')
        return itemsInfo

    def WowImageAPI(self, ctx, UitemID):
        # Get Item Image Data
        api = self.WowAPI(ctx)
        itemMedia = api.get_item_media('us', namespace='static-us', id=UitemID, locale='en_US')
        imagelink = ''
        for data2 in itemMedia.get('assets'):
            imagelink = data2.get('value')
        return imagelink

    def WowGetInfo(self, ctx, itemsInfo):
        # Get Item Image Data
        itemname = itemsInfo.get('name')
        quality = itemsInfo.get('quality').get('name')
        level = itemsInfo.get('level')
        required_level = itemsInfo.get('required_level')
        description = itemsInfo.get('description')
        item_class = itemsInfo.get('item_class').get('name')
        item_subclass = itemsInfo.get('item_subclass').get('name')
        inventory_type = itemsInfo.get('inventory_type').get('name')
        max_count = itemsInfo.get('max_count')
        purchase_price = itemsInfo.get('purchase_price')
        sell_price = itemsInfo.get('sell_price')

        level_display_string = None
        spells_id = None
        spells_description = None
        display_string = None
        reputationname = None
        reputation_display_string = None
        min_reputation_level = None

        preview_item = itemsInfo.get('preview_item')
        if preview_item is not None:
            level2 = preview_item.get('level')
            spells = preview_item.get('spells')
            requirements = preview_item.get('requirements')
            if level2 is not None:
                level_display_string = level2.get('display_string')
            if spells is not None:
                for SD in spells:
                    spells_id = SD.get('spell').get('id')
                    spells_description = SD.get('description')
            if requirements is not None:
                ability = requirements.get('ability')
                reputation = requirements.get('reputation')
                if ability is not None:
                    display_string = ability.get('display_string')
                if reputation is not None:
                    reputationname = reputation.get('faction').get('name')
                    reputation_display_string = reputation.get('faction').get('display_string')
                    min_reputation_level = reputation.get('faction').get('min_reputation_level')

        return itemname, quality, level, required_level, description, item_class, item_subclass, inventory_type, \
               reputationname, level_display_string, display_string, max_count, spells_id, spells_description, \
               reputation_display_string, min_reputation_level, purchase_price, sell_price

    @commands.command(name='iteminfo')
    async def get_Items(self, ctx, *UitemID):
        """List Item Info."""
        if ctx.channel.name == self.bot.configs[str(ctx.guild.id)]['botChannel'] or ctx.channel.id == int(self.bot.configs[str(ctx.guild.id)]['botChannel']):
            try:
                # Namer Or ID Check
                UitemID = (' '.join(UitemID))
                if not UitemID.isdigit():
                    UitemID = self.bot.jsonData['itemsdb'][UitemID]
                if UitemID.isdigit():
                    UitemID = UitemID

                # Request Python Wow API
                self.PrintData('Requesting WoW API.')
                await ctx.send('Searching Items....')

                 # Get Item Infos
                itemsInfo = self.WowItemAPI(ctx, UitemID)
                itemsImage = self.WowImageAPI(ctx, UitemID)

                # Debug pprint JSON Data
                self.bot.get_cog("ConfigsCog").UsePPrint(ctx, itemsInfo)

                # Get Item Infos
                itemname, quality, level, required_level, description, item_class, item_subclass, inventory_type, \
                reputationname, level_display_string, display_string, max_count, spells_id, spells_description, \
                reputation_display_string, min_reputation_level, purchase_price, sell_price = self.WowGetInfo(ctx, itemsInfo)
                itemURL = 'https://www.wowhead.com/item=' + str(UitemID)
                output = 'Item ID: ['+str(UitemID)+']\n' + \
				         'Spell ID: ['+str(spells_id)+']\n' + \
                         'Quality: ['+str(quality)+']\n' + \
                         'Level: ['+str(level)+']\n' + \
                         'Required Level: ['+str(required_level)+']\n' + \
                         'Item Class: ['+str(item_class)+']\n' + \
                         'Item Sub Class: ['+str(item_subclass)+']\n' + \
                         'Inventory Type: ['+str(inventory_type)+']\n' + \
                         'Details?: ['+str(display_string)+']\n' + \
                         'Level Details?: ['+str(level_display_string)+']\n' + \
                         'Max Count: ['+str(max_count)+']\n' + \
                         '**Description Info:**\n' + \
                         'Description: ['+str(description)+']\n' + \
                         'Spells Description: ['+str(spells_description)+']\n' + \
                         '**Reputation Info:**\n' + \
                         'Rep Faction Name: ['+str(reputationname)+']\n' + \
                         'Rep Details?: ['+str(reputation_display_string)+']\n' + \
                         'Rep Min Level: ['+str(min_reputation_level)+']\n' + \
                         '**Price Info:**\n' + \
                         'Purchase Price: ['+self.bot.get_cog("ConfigsCog").WowGold(ctx, purchase_price)+']\n' + \
                         'Sell Price: ['+self.bot.get_cog("ConfigsCog").WowGold(ctx, sell_price)+']\n'

                # Output To Discord
                embed = discord.Embed(description=output, colour=0x98FB98)
                embed.set_author(name=str(itemname) + ' - ['+UitemID+']', url=itemURL, icon_url=itemsImage)
                await ctx.send(embed=embed)

            # Error Handleing
            except WowApiException as werror:
                self.PrintData('WowAPI Error: ' + str(werror))
                embed = discord.Embed(description=str(werror), colour=0xFF0000)
                embed.set_author(name='WowAPI Error')
                await ctx.send(embed=embed)
            except KeyError as kerror:
                self.PrintData('Key Error: ' + str(kerror))
                embed = discord.Embed(description=str(kerror), colour=0xFF0000)
                embed.set_author(name='Key Error')
                await ctx.send(embed=embed)
            except (RuntimeError, AttributeError, SyntaxError, ImportError, ReferenceError, NameError, Warning) as error:
                self.PrintData(error)
                embed = discord.Embed(description=str(error), colour=0xFF0000)
                embed.set_author(name='Wowbot Encountered An Error')
                await ctx.send(embed=embed)

    def PrintData(self, value):
        print(value)

def setup(bot):
    bot.add_cog(ItemsCog(bot))
