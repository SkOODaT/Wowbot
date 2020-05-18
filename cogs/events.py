import discord
from discord.ext import commands
import aiomysql

class EventsCog(commands.Cog):
    """EventsCog"""

    def __init__(self, bot):
        self.bot = bot
        self.bot.configs = {}
        print('Events Cog Loaded.')

    @commands.Cog.listener()
    async def on_ready(self):
        """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

        self.bot.get_cog("ConfigsCog").loadConfigs()

        print(f'Logged in as: {self.bot.user.name} - {self.bot.user.id}\nVersion: 1.0')
        # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
        await self.bot.change_presence(activity=discord.Game(name='World of Warcraft....', type=1))
        #print(f'Successfully logged in and booted...!')

        for guild in self.bot.guilds:
            if str(guild.id) not in self.bot.configs:
                self.bot.configs[str(guild.id)] = dict()
                self.bot.get_cog("ConfigsCog").saveConfigs()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if str(guild.id) not in self.bot.configs:
            self.bot.configs[str(guild.id)] = dict()
            self.bot.get_cog("ConfigsCog").saveConfigs()

def setup(bot):
    bot.add_cog(EventsCog(bot))
