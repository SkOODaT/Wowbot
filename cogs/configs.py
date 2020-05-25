import discord
from discord.ext import commands
from asyncio import TimeoutError
import json
import pprint

class ConfigsCog(commands.Cog):
    """ConfigsCog"""

    def __init__(self, bot):
        self.bot = bot
        print('Configs Cog Loaded.')

    def loadConfigs(self):
        with open('configs.json', 'r') as f:
            self.bot.configs = json.load(f)
        print("Configuration Loaded")
		
        with open('itemdb.json', 'r') as f:
            self.bot.jsonData = json.load(f)
        print("Item Data Loaded")

    def saveConfigs(self):
        with open('configs.json', 'w') as outfile:
            json.dump(self.bot.configs, outfile, indent=4)
        print("Configuration Saved")

    def WowGold(self, ctx, value):
        if value is not None:
            gold = value / 10000
            value = value % 10000
            silver = value / 100
            copper = value % 100
            return '{:.0f}'.format(gold)+""+self.bot.configs[str(ctx.guild.id)]['goldEmoji']+" "+ \
                   '{:.0f}'.format(silver)+""+self.bot.configs[str(ctx.guild.id)]['silverEmoji']+" "+ \
                   '{:.0f}'.format(copper)+""+self.bot.configs[str(ctx.guild.id)]['copperEmoji']

    def UsePPrint(self, ctx, value):
        if self.bot.configs[str(ctx.guild.id)]['pprint'] == "True":
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(value)

    def UseDebug(self, ctx, value):
        if self.bot.configs[str(ctx.guild.id)]['debug'] == "True":
            print(value)

    @commands.command(name='wowbot')
    @commands.is_owner()
    async def run_config(self, ctx, *, config = ""):
        """Admin Command"""
        def check(msg):
            return msg.content != "cancel" and msg.author == ctx.author and msg.channel == ctx.channel

        if config == "":
            await ctx.send("Configuration options: ```clientID - Set Blizzard API ClientID\n" \
                                                     "clientSecret - Set Blizzard API ClientSecret\n" \
                                                     "realmID - Set realmID For Auctions and Misc\n" \
                                                     "botChannel - Set botChannel\n" \
                                                     "goldEmoji - Set Gold Emoji\n" \
                                                     "silverEmoji - Set Silver Emoji\n" \
                                                     "copperEmoji - Set Copper Emoji\n" \
                                                     "pprint - Toggle PPrint (True/False)\n" \
                                                     "debug - Toggle Debug (True/False)```")
        elif config == "clientID":
            try:
                await ctx.send("Please enter a response for the `clientID` command. Enter `cancel` to exit.")
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                if msg:
                    pass
                    self.bot.configs[str(ctx.guild.id)]['clientID'] = msg.content
                    self.saveConfigs()
            except TimeoutError:
                await ctx.send("Timeout. not updated")
        elif config == "clientSecret":
            try:
                await ctx.send("Please enter a response for the `clientSecret` command.  Enter `cancel` to exit.")
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                if msg:
                    pass
                    self.bot.configs[str(ctx.guild.id)]['clientSecret'] = msg.content
                    self.saveConfigs()
            except TimeoutError:
                await ctx.send("Timeout. not updated")
        elif config == "realmID":
            try:
                await ctx.send("Please enter a response for the `realmID` command. Enter `cancel` to exit.")
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                if msg:
                    pass
                    self.bot.configs[str(ctx.guild.id)]['realmID'] = msg.content
                    self.saveConfigs()
            except TimeoutError:
                await ctx.send("Timeout. not updated")
        elif config == "botChannel":
            try:
                await ctx.send("Please enter a response for the `botChannel` command. Enter `cancel` to exit.")
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                if msg:
                    pass
                    self.bot.configs[str(ctx.guild.id)]['botChannel'] = msg.content
                    self.saveConfigs()
            except TimeoutError:
                await ctx.send("Timeout. not updated")
        elif config == "goldEmoji":
            try:
                await ctx.send("Please enter a response for the `goldEmoji` command.  Enter `cancel` to exit.")
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                if msg:
                    print(msg)
                    pass
                    self.bot.configs[str(ctx.guild.id)]['goldEmoji'] = msg.content
                    self.saveConfigs()
            except TimeoutError:
                await ctx.send("Timeout. not updated")
        elif config == "silverEmoji":
            try:
                await ctx.send("Please enter a response for the `silverEmoji` command.  Enter `cancel` to exit.")
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                if msg:
                    pass
                    self.bot.configs[str(ctx.guild.id)]['silverEmoji'] = msg.content
                    self.saveConfigs()
            except TimeoutError:
                await ctx.send("Timeout. not updated")
        elif config == "copperEmoji":
            try:
                await ctx.send("Please enter a response for the `copperEmoji` command.  Enter `cancel` to exit.")
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                if msg:
                    pass
                    self.bot.configs[str(ctx.guild.id)]['copperEmoji'] = msg.content
                    self.saveConfigs()
            except TimeoutError:
                await ctx.send("Timeout. not updated")
        elif config == "pprint":
            try:
                await ctx.send("Please enter a response for the `pprint` command.  Enter `cancel` to exit.")
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                if msg:
                    pass
                    self.bot.configs[str(ctx.guild.id)]['pprint'] = msg.content
                    self.saveConfigs()
            except TimeoutError:
                await ctx.send("Timeout. not updated")
        elif config == "debug":
            try:
                await ctx.send("Please enter a response for the `debug` command.  Enter `cancel` to exit.")
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                if msg:
                    pass
                    self.bot.configs[str(ctx.guild.id)]['debug'] = msg.content
                    self.saveConfigs()
            except TimeoutError:
                await ctx.send("Timeout. not updated")

def setup(bot):
    bot.add_cog(ConfigsCog(bot))
