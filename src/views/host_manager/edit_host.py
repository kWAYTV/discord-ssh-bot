import discord, logging
from datetime import datetime
from src.helper.config import Config
from src.database.schema.host_schema import HostSchema
from src.database.controllers.hosts_controller import HostsController

logger = logging.getLogger(__name__)

class EditHostModal(discord.ui.Modal, title='Edit Host'):
    def __init__(self, host: HostSchema):
        super().__init__()
        self.host = host
        self.config = Config()
        self.hosts_controller = HostsController()

    host_ip = discord.ui.TextInput(label='IP', placeholder='Enter the new IP address of the host...')
    host_port = discord.ui.TextInput(label='Port', placeholder='Enter the new port of the host...', min_length=1, max_length=5)
    host_username = discord.ui.TextInput(label='Username', placeholder='Enter the new username of the host...', min_length=1, max_length=32)
    host_password = discord.ui.TextInput(label='Password', placeholder='Enter the new password of the host...', min_length=1, max_length=32)
    host_key = discord.ui.TextInput(label='Key (Optional)', style=discord.TextStyle.long, placeholder='Enter the new key of the host...', required=False)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        old_schema: HostSchema = await self.hosts_controller.get_host(interaction.user.id, self.host.ip, self.host.port)
        new_schema: HostSchema = HostSchema(interaction.user.id, self.host_ip.value, self.host_port.value, self.host_username.value, self.host_password.value, self.host_key.value)

        if not old_schema.is_owner(interaction.user.id):
            self.logger.warning(f"{interaction.user.mention} tried to edit a host they do not own. {old_schema.__repr__()} -> {new_schema.__repr__()}")
            await interaction.followup.send(f'You are not the owner of the host, {interaction.user.mention}!', ephemeral=True)
            return
        
        if not await self.hosts_controller.host_exists(old_schema.ip, old_schema.port):
            await interaction.followup.send(f'The host does not exist in the database, {interaction.user.mention}!', ephemeral=True)
            return

        embed = discord.Embed(title="Host Info", description="The host was successfully edited in the database. Changes:")

        # For each field in the modal, add it to the embed if it changed from the original value
        embed.add_field(name="Edited By", value=f"{interaction.user.mention} (`{interaction.user.id}`)", inline=False)
        if new_schema.ip != old_schema.ip:
            embed.add_field(name="IP", value=f"`{old_schema.ip}` -> `{new_schema.ip}`", inline=False)
        if new_schema.port != old_schema.port:
            embed.add_field(name="Port", value=f"`{old_schema.port}` -> `{new_schema.port}`", inline=False)
        if new_schema.username != old_schema.username:
            embed.add_field(name="Username", value=f"`{old_schema.username}` -> `{new_schema.username}`", inline=True)
        if new_schema.password != old_schema.password:
            embed.add_field(name="Password", value=f"`{old_schema.password}` -> `{new_schema.password}`", inline=True)
        if new_schema.key != old_schema.key:
            embed.add_field(name="Key", value=f"```{old_schema.key}``` -> ```{new_schema.key}```", inline=False)

        embed.set_author(name=self.config.app_name, icon_url=self.config.app_logo, url=self.config.app_url)
        embed.set_footer(text=self.config.app_name, icon_url=self.config.app_logo)
        embed.set_thumbnail(url=self.config.app_logo)
        embed.set_image(url=self.config.rainbow_line_gif)
        embed.timestamp = datetime.utcnow()

        if not await self.hosts_controller.edit_host(old_schema, new_schema):
            await interaction.followup.send(f'Oops! Something went wrong editing the host.', ephemeral=True)
            return

        logger.info(f"{interaction.user.mention} Edited a host in the database. {old_schema.__repr__()} -> {new_schema.__repr__()}")
        await interaction.followup.send(f'Edited the host in the database, {interaction.user.mention}!', embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong: {error}', ephemeral=True)
