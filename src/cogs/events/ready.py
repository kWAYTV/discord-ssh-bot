from loguru import logger
from pyfiglet import Figlet
from discord.ext import commands
from src.helper.config import Config
from pystyle import Colors, Colorate, Center
from src.views.interaction_panel.interaction_panel_view import InteractionPanelButtonsView

class OnReady(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_ready(self):

        logo = Figlet(font="big").renderText(self.config.app_name)
        centered_logo = Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1))
        divider = Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "────────────────────────────────────────────\n\n", 1))

        print(centered_logo)
        print(divider)

        # Load persistent views
        logger.debug(f"Loading persistent views...")
        self.bot.add_view(InteractionPanelButtonsView())

        logger.info(f"Logged in as {self.bot.user.name}#{self.bot.user.discriminator}.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnReady(bot))
    return logger.info("On ready event registered!")