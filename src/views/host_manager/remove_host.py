import discord
from loguru import logger
from datetime import datetime
from src.helper.config import Config
from src.database.controllers.hosts_controller import HostsController

class RemoveHostModal(discord.ui.Modal, title='Remove Host'):
    def __init__(self):
        self.config = Config()
        self.hosts_controller = HostsController()
        super().__init__()

    host_ip = discord.ui.TextInput(label='IP', placeholder='Enter the IP address of the host here...')
    host_port = discord.ui.TextInput(label='Port', placeholder='Enter the port of the host here...', min_length=1, max_length=5)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if not await self.hosts_controller.is_owner_of_host(interaction.user.id, self.host_ip.value, self.host_port.value):
            await interaction.followup.send(f'You are not the owner of the host, {interaction.user.mention}!', ephemeral=True)
            return

        embed = discord.Embed(title="Host Info", description="The host was successfully removed from the database.")
        
        # For each field in the modal, add it to the embed
        embed.add_field(name="Removed By", value=f"{interaction.user.mention} (`{interaction.user.id}`)", inline=False)
        embed.add_field(name="Address", value=f"`{self.host_ip.value}`:`{self.host_port.value}`", inline=False)

        embed.set_author(name=self.config.app_name, icon_url=self.config.app_logo, url=self.config.app_url)
        embed.set_footer(text=self.config.app_name, icon_url=self.config.app_logo)
        embed.set_thumbnail(url=self.config.app_logo)
        embed.set_image(url=self.config.rainbow_line_gif)
        embed.timestamp = datetime.utcnow()

        if not await self.hosts_controller.host_exists(self.host_ip.value, self.host_port.value):
            await interaction.followup.send(f'The host does not exist in the database, {interaction.user.mention}!', ephemeral=True)
            return

        if not await self.hosts_controller.remove_host(self.host_ip.value, self.host_port.value):
            await interaction.followup.send(f'Ooaps! Something went wrong removing the host.', ephemeral=True)
            return

        logger.info(f"{interaction.user.mention} Removed a host from the database.")
        await interaction.followup.send(f'Removed the host from the database, {interaction.user.mention}!', embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong: {error}', ephemeral=True)
