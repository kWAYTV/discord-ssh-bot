import discord
from loguru import logger
from src.helper.config import Config
from src.database.schema.host_schema import HostSchema
from src.controller.ssh_controller import SSHController
from src.views.host_client.host_chat import HostChatView
from src.views.host_manager.edit_host import EditHostModal
from src.views.host_manager.remove_host import RemoveHostModal
from src.database.controllers.sessions_controller import SessionsController

class HostPanelView(discord.ui.View):
    def __init__(self, host: HostSchema):
        super().__init__(timeout=None)
        self.host = host
        self.config = Config()
        self.sessions_controller = SessionsController()

    @discord.ui.button(label='🔗 Connect', style=discord.ButtonStyle.green, custom_id='ssh_menu:connect')
    async def connect_host(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild, user, channel_name = interaction.guild, interaction.user, f"host-{self.host.owner}-{self.host.ip}"

        # Check if the user already has a session for this host, if it does, it returns the host object
        session_exists = await self.sessions_controller.session_exists(self.host.owner, self.host.ip, self.host.port)
        if session_exists:
            return await interaction.response.send_message(f"You already have a session open for this host or use the /kill command to kill all your current sessions! <#{session_exists.discord_channel_id}>", ephemeral=True)
        
        # Create a new text channel for the host
        category = guild.get_channel(self.config.chat_category)
        channel = await category.create_text_channel(channel_name)

        # Set the permissions for the host channel
        await channel.set_permissions(guild.default_role, read_messages=False, send_messages=False)
        await channel.set_permissions(user, read_messages=True, send_messages=True)

        # Create a new session for the host
        session_id = await self.sessions_controller.add_session(self.host, channel.id)

        # Connect to the ssh host
        controller = SSHController(session_id, self.host.owner, self.host.ip, self.host.port, self.host.username, self.host.password, self.host.key, channel.id)
        try:
            await controller.connect()
        except Exception as e:
            await channel.delete()
            await self.sessions_controller.remove_session(session_id)
            logger.critical(f"Error connecting to host: {e}")
            return await interaction.response.send_message(f"Error connecting to host: {e}", ephemeral=True)

        # Switch to the new channel
        await interaction.response.send_message(f"Switching to: {channel.mention}", ephemeral=True)
        await channel.send(f"Welcome to your host channel! {user.mention}", view=HostChatView(controller))
        return

    @discord.ui.button(label='🗑️ Remove Host', style=discord.ButtonStyle.red, custom_id='ssh_menu:remove')
    async def remove_host(self, interaction: discord.Interaction, button: discord.ui.Button):
        return await interaction.response.send_modal(RemoveHostModal())

    @discord.ui.button(label='✍️ Edit Host', style=discord.ButtonStyle.blurple, custom_id='ssh_menu:edit')
    async def edit_host(self, interaction: discord.Interaction, button: discord.ui.Button):
        return await interaction.response.send_modal(EditHostModal(self.host))