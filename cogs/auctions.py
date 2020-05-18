import discord
from discord.ext import commands
from wowapi import WowApi

AHtimes = {
    'SHORT' : 'Less than 30 minutes.',
    'MEDIUM' : 'Between 30 minutes and 2 hours.',
    'LONG' : 'Between 2 hours and 12 hours.',
    'VERY_LONG' : 'Between 12 hours and 48 hours.'
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

    @commands.command(name='ahitem')
    async def get_Auctions(self, ctx, UitemID = ""):
        """List Silvermoon Auctions, Use !item "IDNumber"."""
        if ctx.channel.name == self.bot.configs[str(ctx.guild.id)]['botChannel'] or ctx.channel.id == int(self.bot.configs[str(ctx.guild.id)]['botChannel']):
            try:
                api = self.WowAPI(ctx)
                auctions = api.get_auctions('us', namespace='dynamic-us', realm_id=self.bot.configs[str(ctx.guild.id)]['realmID'], locale='en_US')
                count = 0
                for data in auctions.get('auctions'):
                    auctionID = data.get('id')
                    itemID = data.get('item').get('id')
                    buyOut = data.get('buyout')
                    unitPrice = data.get('unit_price')
                    timeLeft = data.get('time_left')
                    quantity = data.get('quantity')
                    if int(itemID) == int(UitemID):
                        convertgold = self.WowGold(ctx, buyOut)
                        itemsInfo = api.get_item_data('us', namespace='static-us', id=itemID, locale='en_US')
                        itemName = itemsInfo.get('name')
                        #print(itemsInfo.get('name'))
                        itemMedia = api.get_item_media('us', namespace='static-us', id=itemID, locale='en_US')
                        for data2 in itemMedia.get('assets'):
                            imagelink = data2.get('value')
                            #print(imagelink)
                        count = count + 1
                        #print(count)
                        #print(data)
                        output = 'Auction ID: ' + str(auctionID) + '\nItem ID: ' + str(itemID) + '\nQuantity: ' + str(quantity) + '\nUnit Price: ' + \
                                  str(unitPrice) + '\nBuyout: ' + str(convertgold) + '\nTime Left: ' + AHtimes[timeLeft] + '\n'
                        embed = discord.Embed(description=output, colour=0x98FB98)
                        embed.set_thumbnail(url=imagelink)
                        embed.set_author(name=itemName, url=imagelink, icon_url=imagelink)
                        await ctx.send(embed=embed)
                        if count > 9:
                            await ctx.send('Too Many Results To List Everything.') 
                            break
            except (RuntimeError, AttributeError):
                await ctx.send('Server is not currently available.')

def setup(bot):
    bot.add_cog(AuctionsCog(bot))
