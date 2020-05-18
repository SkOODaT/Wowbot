import discord
from discord.ext import commands
from asyncio import TimeoutError
import json

class ConfigsCog(commands.Cog):
    """ConfigsCog"""

    def __init__(self, bot):
        self.bot = bot
        print('Configs Cog Loaded.')

    def loadConfigs(self):
        with open('configs.json', 'r') as f:
            self.bot.configs = json.load(f)
        print("Configuration Loaded")

    def saveConfigs(self):
        with open('configs.json', 'w') as outfile:
            json.dump(self.bot.configs, outfile, indent=4)
        print("Configuration Saved")

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
                                                     "copperEmoji - Set Copper Emoji```")
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

def setup(bot):
    bot.add_cog(ConfigsCog(bot))
