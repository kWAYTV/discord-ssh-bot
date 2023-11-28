import discord, traceback
from loguru import logger
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from src.helper.config import Config
from src.views.interaction_panel.interaction_panel_view import InteractionPanelButtonsView

class Panel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()

    @app_commands.command(name="panel", description="Send the bot interaction panel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def panel_command(self, interaction: discord.Interaction, hidden: bool = False):
        try:
            await interaction.response.defer()

            embed = discord.Embed(title="Bot Panel", description="Use the menu below to interact with the bot.")
            embed.set_author(name=self.config.app_name, icon_url=self.config.app_logo, url=self.config.app_url)
            embed.set_footer(text=f"Holding {len(self.bot.guilds)} guilds & {sum(guild.member_count for guild in self.bot.guilds)} users.", icon_url=self.config.app_logo)
            embed.set_thumbnail(url=self.config.app_logo)
            embed.set_image(url=self.config.rainbow_line_gif)
            embed.timestamp = datetime.utcnow()

            await interaction.followup.send(embed=embed, view=InteractionPanelButtonsView(), ephemeral=hidden)

        except Exception as e:
            await interaction.followup.send(f"An error occurred with panel command: {e}", ephemeral=True)
            logger.error(f"An error occurred with panel command: {e}")
            traceback.print_exc()

    @panel_command.error
    async def panel_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{self.config.red_cross_emoji_id} You don't have the necessary permissions to use this command.",ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Panel(bot))
    logger.info("Panel command loaded!")