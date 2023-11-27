import logging
from discord.ext import commands
from src.helper.config import Config
from src.views.interaction_panel.interaction_panel_view import InteractionPanelButtonsView

logger = logging.getLogger(__name__)

class OnReady(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_ready(self):

        # Load persistent views
        logger.info(f"Loading persistent views...")
        self.bot.add_view(InteractionPanelButtonsView())

        logger.info(f"Logged in as {self.bot.user.name}#{self.bot.user.discriminator}.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnReady(bot))
    return logger.info("On ready event registered!")