import discord
from discord.ext import commands
from wowapi import WowApi
from wowapi import WowApiException

AHTimes = {
    'SHORT':      '30m',
    'MEDIUM':     '30m/2h',
    'LONG':       '2h/12h',
    'VERY_LONG':  '12h/48h'
}

class AuctionsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Auctions Cog Loaded.')

    def WowAPI(self, ctx):
        # Connect To Wow API
        api = WowApi(self.bot.configs[str(ctx.guild.id)]['clientID'], self.bot.configs[str(ctx.guild.id)]['clientSecret'])
        return api

    def WowAuctionAPI(self, ctx):
        # Get Auctions Data
        api = self.WowAPI(ctx)
        auctions = api.get_auctions('us', namespace='dynamic-us', realm_id=self.bot.configs[str(ctx.guild.id)]['realmID'], locale='en_US')
        return auctions

    def WowRebuildInfo(self, ctx, UitemID, auctions):
        counter = 0
        AHlist = []
        AllData = auctions.get('auctions')
        for AHData in AllData:
            itemID = AHData.get('item').get('id')
            if int(itemID) == int(UitemID):
                counter = counter + 1

                # Debug pprint JSON Data
                self.bot.get_cog("ConfigsCog").UsePPrint(ctx, AHData)

                AHlist.append({
                    'auction_ID': AHData.get('id'),
                    'item_ID': AHData.get('item').get('id'),
                    'unit_price': AHData.get('unit_price'),
                    'buyout': AHData.get('buyout'),
                    'quantity': AHData.get('quantity'),
                    'pet_level': AHData.get('item').get('pet_level'),
                    'time_left': AHData.get('time_left'),
                })
                # Break Loop For Excessive Results (What Is Discord Limit?)
                if counter > 100:
                    break
        return AHlist

    def WowImageAPI(self, ctx, UitemID):
        # Get Item Name And Image Data
        api = self.WowAPI(ctx)
        itemsInfo = api.get_item_data('us', namespace='static-us', id=UitemID, locale='en_US')
        itemname = itemsInfo.get('name')
        itemMedia = api.get_item_media('us', namespace='static-us', id=UitemID, locale='en_US')
        imagelink = ''
        for data2 in itemMedia.get('assets'):
            imagelink = data2.get('value')
        return itemname, imagelink

    def WowListConvert(self, AHlist):
        AHlist2 = []
        for AHData2 in AHlist:
            AHlist2.append(list(AHData2.items()))
        return AHlist2

    def WowGetElement(self, element):
        if element[2][1] is not None:
            element = element[2]
        else:
            element = element[3]
        return element

    @commands.command(name='itemah')
    async def get_Auctions(self, ctx, *UitemID):
        """List Silvermoon Auctions, Sorted By UnitPrice Then Buyout."""
        if ctx.channel.name == self.bot.configs[str(ctx.guild.id)]['botChannel'] or ctx.channel.id == int(self.bot.configs[str(ctx.guild.id)]['botChannel']):
            try:
                # Namer Or ID Check
                UitemID = (' '.join(UitemID))
                if not UitemID.isdigit():
                    UitemID = self.bot.jsonData['itemsdb'][UitemID]
                elif UitemID.isdigit():
                    UitemID = UitemID

                # Get Auction Data
                self.PrintData('Requesting WoW API.')
                await ctx.send('Searching Auction Items....')
                auctions = self.WowAuctionAPI(ctx)

                # Rebuild The Dictation
                self.PrintData('ReBuilding Dictation.')
                AHlist = self.WowRebuildInfo(ctx, UitemID, auctions)

                # Let User Know If No Data Found/Return
                if len(AHlist) == 0:
                    self.PrintData('No Auction Items Found.')
                    itemname, imagelink = self.WowImageAPI(ctx, UitemID)
                    itemURL = 'https://www.wowhead.com/item=' + str(UitemID)
                    embed = discord.Embed(description='No Auction Items Found For ['+UitemID+'].', colour=0xFF0000)
                    embed.set_author(name=str(itemname) + ' - ['+UitemID+']', url=itemURL, icon_url=imagelink)
                    await ctx.send(embed=embed)
                    return

                # Get Item Name And Image
                itemname, imagelink = self.WowImageAPI(ctx, UitemID)

                # Convert The Dictation To A List
                self.PrintData('Converting Dictation To List.')
                AHlist2 = self.WowListConvert(AHlist)

                # Sort The List And Format For Discord
                self.PrintData('Sorting Python List.')
                numResults = len(AHlist2)
                ctr = 0
                outputTitle = ''
                header = "\n"
                output = header
                for infos in sorted(AHlist2, key=self.WowGetElement):
                    ctr += 1
                    auction_ID = infos[0][1]
                    item_ID = infos[1][1]
                    unit_price = infos[2][1]
                    buyout = infos[3][1]
                    quantity = infos[4][1]
                    pet_level = infos[5][1]
                    time_left = infos[6][1]
                    if unit_price is not None:
                        convertunitprice = self.bot.get_cog("ConfigsCog").WowGold(ctx, unit_price)
                    else:
                        convertunitprice = 'NoUP'
                    if buyout is not None:
                        convertbuyout = self.bot.get_cog("ConfigsCog").WowGold(ctx, buyout)
                    else:
                        convertbuyout = 'NoBO'
                    if pet_level is not None:
                        pet_level = '[PetLv.' + str(pet_level) + ']'
                    else:
                        pet_level = ''
                    #self.PrintData(auction_ID, item_ID, unit_price ,quantity, time_left)
                    itemURL = 'https://www.wowhead.com/item=' + str(item_ID)
                    outputTitle = str(itemname) + ' - [' + str(item_ID) + ']'
                    output += '[' + str(convertunitprice) + '] ' + \
                              '[' + str(convertbuyout) + '] ' + \
                              '[Qty.' + str(quantity) + '] ' + \
                              '' + pet_level + '' + \
                              '[' + AHTimes[time_left] + '] ' + \
                              '[' + str(auction_ID) + ']\n'
                    if len(output) > 1850 or ctr == numResults:
                        embed = discord.Embed(description=output, colour=0x98FB98)
                        embed.set_author(name=outputTitle, url=itemURL, icon_url=imagelink)
                        await ctx.send(embed=embed)
                        if ctr != numResults:
                            output = header

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
    bot.add_cog(AuctionsCog(bot))
