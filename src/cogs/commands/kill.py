import discord
from loguru import logger
from discord.ext import commands
from discord import app_commands
from src.helper.config import Config
from src.database.controllers.sessions_controller import SessionsController

class Kill(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()
        self.sessions_controller = SessionsController()

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="kill", description="Kill all your current active sessions.")
    async def kill_command(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer(ephemeral=True)
        try:
            # if the user is not the same as the command issuer and the command issuer is not an admin, return
            if user is not None and interaction.user != user and not interaction.user.guild_permissions.administrator:
                logger.critical(f"User {interaction.user.name} ({interaction.user.id}) tried to kill another user's sessions without being an admin.")
                return await interaction.followup.send(f"You don't have the necessary permissions to use this command on that user.", ephemeral=True)

            try:
                channels_to_close = await self.sessions_controller.kill_sessions(interaction.user.id if user is None else user.id)
                if len(channels_to_close) > 0:
                    for channel_id in channels_to_close:
                        channel = self.bot.get_channel(int(channel_id))
                        await channel.delete()
            except Exception as e:
                logger.critical(f"Failed to delete the session channels for user {interaction.user.name} ({interaction.user.id}): {e}")

            logger.info(f"Successfully killed all sessions for user {interaction.user.name} ({interaction.user.id}).")
            return await interaction.followup.send(f"Successfully killed all sessions for user {interaction.user.mention} (`{interaction.user.id}`).", ephemeral=True)
        except Exception as e:
            logger.critical(f"Failed to respond to kill command: {e}")
            return await interaction.followup.send("There was an error trying to execute that command!", ephemeral=True)

    @kill_command.error
    async def kill_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            return await interaction.response.send_message(f"You don't have the necessary permissions to use this command.",ephemeral=True)
        else:
            return await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Kill(bot))
    logger.info("Kill command loaded!")