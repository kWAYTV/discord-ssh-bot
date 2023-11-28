import discord
from loguru import logger
from datetime import datetime
from src.helper.config import Config
from src.database.schema.host_schema import HostSchema
from src.database.controllers.hosts_controller import HostsController

class AddHostModal(discord.ui.Modal, title='Add Host'):
    def __init__(self):
        self.config = Config()
        self.hosts_controller = HostsController()
        super().__init__()

    host_ip = discord.ui.TextInput(label='IP', placeholder='Enter the IP address of the host here...')
    host_port = discord.ui.TextInput(label='Port', placeholder='Enter the port of the host here...', min_length=1, max_length=5)
    host_username = discord.ui.TextInput(label='Username', placeholder='Enter the username of the host here...', min_length=1, max_length=32)
    host_password = discord.ui.TextInput(label='Password', placeholder='Enter the password of the host here...', min_length=1, max_length=32)
    host_key = discord.ui.TextInput(label='Key (Optional)', style=discord.TextStyle.long, placeholder='Enter the key of the host here...', required=False)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        embed = discord.Embed(title="Host Info", description="The host was successfully added to the database.")
        
        # For each field in the modal, add it to the embed
        embed.add_field(name="Owner", value=f"{interaction.user.mention} (`{interaction.user.id}`)", inline=False)
        embed.add_field(name="Address", value=f"`{self.host_ip.value}`:`{self.host_port.value}`", inline=False)
        embed.add_field(name="Username", value=f"`{self.host_username.value}`", inline=True)
        embed.add_field(name="Password", value=f"`{self.host_password.value}`", inline=True)
        if self.host_key.value is not None or self.host_key.value != "":
            embed.add_field(name="Key", value=f"```{self.host_key.value}```", inline=False)
        else: pass

        embed.set_author(name=self.config.app_name, icon_url=self.config.app_logo, url=self.config.app_url)
        embed.set_footer(text=self.config.app_name, icon_url=self.config.app_logo)
        embed.set_thumbnail(url=self.config.app_logo)
        embed.set_image(url=self.config.rainbow_line_gif)
        embed.timestamp = datetime.utcnow()

        host_schema = HostSchema(0, interaction.user.id, self.host_ip.value, self.host_port.value, self.host_username.value, self.host_password.value, self.host_key.value)
        if await self.hosts_controller.host_exists(self.host_ip.value, self.host_port.value):
            await interaction.followup.send(f'The host already exists in the database, {interaction.user.mention}!', ephemeral=True)
            return
        
        if not await self.hosts_controller.add_host(host_schema):
            await interaction.followup.send(f'Oops! Something went wrong adding the host.', ephemeral=True)
            return

        logger.info(f"{interaction.user.name} Added a host to the database. {host_schema.__repr__()}")
        await interaction.followup.send(f'Added the host to the database, {interaction.user.mention}!', embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong: {error}', ephemeral=True)