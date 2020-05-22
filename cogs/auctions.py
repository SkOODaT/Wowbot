import discord
from discord.ext import commands
from wowapi import WowApi

AHtimes = {
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
        api = WowApi(self.bot.configs[str(ctx.guild.id)]['clientID'], self.bot.configs[str(ctx.guild.id)]['clientSecret'])
        return api

    def WowGold(self, ctx, value):
        if value is not None:
            gold = value / 10000
            value = value % 10000
            silver = value / 100
            copper = value % 100
            return '{:.0f}'.format(gold)+""+self.bot.configs[str(ctx.guild.id)]['goldEmoji']+" "+ \
                   '{:.0f}'.format(silver)+""+self.bot.configs[str(ctx.guild.id)]['silverEmoji']+" "+ \
                   '{:.0f}'.format(copper)+""+self.bot.configs[str(ctx.guild.id)]['copperEmoji']

    def get_elem(self, elem):
        if elem[3][1] is not None:
            elem = elem[3]
        else: 
            elem = elem[4]
        return elem

    @commands.command(name='item')
    async def get_Auctions(self, ctx, UitemID = ""):
        """List Silvermoon Auctions, Use !item "IDNumber"."""
        if ctx.channel.name == self.bot.configs[str(ctx.guild.id)]['botChannel'] or ctx.channel.id == int(self.bot.configs[str(ctx.guild.id)]['botChannel']):
            try:
                # Request Python Wow API
                self.Debug('Requesting WoW API....')
                await ctx.send('Searching Auction Items....')
                api = self.WowAPI(ctx)
                auctions = api.get_auctions('us', namespace='dynamic-us', realm_id=self.bot.configs[str(ctx.guild.id)]['realmID'], locale='en_US')

                # Rebuild The Dictation
                self.Debug('Building Dict....')
                counter = 0
                AHlist = []
                AllData = auctions.get('auctions')
                printed = False
                for AHData in AllData:
                    itemID = AHData.get('item').get('id')
                    if int(itemID) == int(UitemID):
                        counter = counter + 1
                        itemsInfo = api.get_item_data('us', namespace='static-us', id=itemID, locale='en_US')
                        #self.Debug(itemsInfo.get('name'))
                        itemMedia = api.get_item_media('us', namespace='static-us', id=itemID, locale='en_US')
                        for data2 in itemMedia.get('assets'):
                            imagelink = data2.get('value')
                        #self.Debug(imagelink)
                        print(AHData)
                        AHlist.append({
                            'auction_ID': AHData.get('id'),
                            'name': itemsInfo.get('name'),
                            'item_ID': AHData.get('item').get('id'),
                            'unit_price': AHData.get('unit_price'),
                            'buyout': AHData.get('buyout'),
                            'quantity': AHData.get('quantity'),
                            'pet_level': AHData.get('item').get('pet_level'),
                            'time_left': AHData.get('time_left'),
                            'image_link': imagelink,
                        })
                        if counter > 40 and not printed:
                            printed = True
                            await ctx.send('Please Wait, Alot Of Records....')
                        elif counter > 100:
                            break
                else:
                    self.Debug('No Dict Data.')
                    await ctx.send('No Auction Items Found.')
                    return

                # Convert The Dictation To A List
                self.Debug('Converting To List....')
                AHlist2 = []
                for AHData2 in AHlist:
                    #self.Debug(list(AHData2.items()))
                    AHlist2.append(list(AHData2.items()))
                #self.Debug(AHlist2)

                # Sort The List And Format For Discord
                self.Debug('Sorting List....')
                numResults = len(AHlist2)
                ctr = 0
                outputTitle = ''
                header = "\n"
                output = header
                for infos in sorted(AHlist2, key=self.get_elem):
                    ctr += 1
                    auction_ID = infos[0][1]
                    name = infos[1][1]
                    item_ID = infos[2][1]
                    unit_price = infos[3][1]
                    buyout = infos[4][1]
                    quantity = infos[5][1]
                    pet_level = infos[6][1]
                    time_left = infos[7][1]
                    image_link = infos[8][1]
                    if unit_price is not None:
                        convertunitprice = self.WowGold(ctx, unit_price)
                    else:
                        convertunitprice = 'NoUP'
                    if buyout is not None:
                        convertbuyout = self.WowGold(ctx, buyout)
                    else:
                        convertbuyout = 'NoBO'
                    if pet_level is not None:
                        pet_level = '[PetLv.' + str(pet_level) + ']'
                    else:
                        pet_level = ''
                    #self.Debug(auction_ID, name, item_ID, unit_price ,quantity, time_left, image_link)
                    itemURL = 'https://www.wowhead.com/item=' + str(item_ID)
                    outputTitle = name + ' - [' + str(item_ID) + ']'
                    output += '[' + str(convertunitprice) + ']  [' + str(convertbuyout) + ']  [Qty.' + str(quantity) + '] ' + pet_level + ' [' + AHtimes[time_left] + ']  [' + str(auction_ID) + ']\n'
                    if len(output) > 1850 or ctr == numResults:
                        embed = discord.Embed(description=output, colour=0x98FB98)
                        embed.set_author(name=outputTitle, url=itemURL, icon_url=image_link)
                        await ctx.send(embed=embed)
                        if ctr != numResults:
                            output = header

            # Error Handleing
            except (RuntimeError, AttributeError, SyntaxError, ImportError, ReferenceError, Warning) as error:
                self.Debug(error)
                await ctx.send('Wowbot Encountered An Error.')

    def Debug(self, value):
        print(value)

def setup(bot):
    bot.add_cog(AuctionsCog(bot))
