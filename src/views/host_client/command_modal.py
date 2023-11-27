import discord
from datetime import datetime
from src.helper.config import Config
from src.controller.ssh_controller import SSHController

class HostCommandModal(discord.ui.Modal, title='Send command to host'):
    def __init__(self, controller: SSHController):
        super().__init__()
        self.config = Config()
        self.controller = controller

    host_command = discord.ui.TextInput(label='Command', style=discord.TextStyle.long, placeholder='Enter the command you want to execute')

    async def on_submit(self, interaction: discord.Interaction):
        result = await self.controller.execute(self.host_command.value)
        embed = discord.Embed(title='Hello there!', description=f"Result for `{self.host_command.value}`", color=discord.Color.green())

        embed.add_field(name="Result", value=f"```{result}```", inline=False)

        embed.set_author(name=self.config.app_name, icon_url=self.config.app_logo, url=self.config.app_url)
        embed.set_footer(text=self.config.app_name, icon_url=self.config.app_logo)
        embed.set_thumbnail(url=self.config.app_logo)
        embed.set_image(url=self.config.rainbow_line_gif)
        embed.timestamp = datetime.utcnow()

        await interaction.response.send_message(f'Executed the command successfully, {interaction.user.mention}!', embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong: {error}', ephemeral=True)