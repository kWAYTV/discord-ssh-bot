import discord, logging
from datetime import datetime
from discord.ext import commands
from src.helper.config import Config

logger = logging.getLogger(__name__)

class Logger:

    def __init__(self, bot: commands.Bot = None):
        self.bot = bot
        self.config = Config()

    async def discord_log(self, description: str):
        channel = self.bot.get_channel(self.config.logs_channel)
        if channel:
            embed = discord.Embed(title=self.config.app_name, description=f"```{description}```")
            embed.set_thumbnail(url=self.config.app_logo)
            embed.set_image(url=self.config.rainbow_line_gif)
            embed.set_footer(text=f"{self.config.app_name_branded}", icon_url=self.config.app_logo)
            embed.timestamp = datetime.utcnow()
            await channel.send(embed=embed)
        else:
            logger.error(f"Could not find the logs channel with id {self.config.logs_channel}")

    async def dm_user(self, userid: int, message: str):
        user = await self.bot.fetch_user(userid)
        if user:
            await user.send(message)
        else:
            logger.error(f"Could not find the user with id {userid}")