import discord, asyncio
from src.helper.config import Config
from src.controller.ssh_controller import SSHController
from src.views.host_client.command_modal import HostCommandModal
from src.database.controllers.sessions_controller import SessionsController

class HostChatView(discord.ui.View):
    def __init__(self, controller: SSHController):
        super().__init__(timeout=None)
        self.config = Config()
        self.controller = controller
        self.sessions_controller = SessionsController()

    async def not_implemented(self, interaction: discord.Interaction):
        return await interaction.response.send_message("Sorry! This option is **not** yet implemented.", ephemeral=True)
    
    @discord.ui.button(label='🔗 Send Command', style=discord.ButtonStyle.green, custom_id='ssh_menu:send_command')
    async def send_command(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.sessions_controller.update_session_last_used(self.controller.id)
        await interaction.response.send_modal(HostCommandModal(self.controller))

    @discord.ui.button(label='🛑 Disconnect', style=discord.ButtonStyle.red, custom_id='ssh_menu:disconnect')
    async def disconnect_host(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.sessions_controller.remove_session(self.controller.id)
        await self.controller.close()
        await interaction.response.send_message("Disconnected from host, deleting channel in 3 seconds...", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.channel.delete()