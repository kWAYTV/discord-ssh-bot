import discord
from src.views.host_manager.add_host import AddHostModal
from src.views.host_manager.list_hosts import ListHostsDropdownView

class InteractionPanelButtonsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def not_implemented(self, interaction: discord.Interaction):
        return await interaction.response.send_message("Sorry! This option is **not** yet implemented.", ephemeral=True)

    @discord.ui.button(label='➕ Add Host', style=discord.ButtonStyle.green, custom_id='ssh_menu:add')
    async def add_host(self, interaction: discord.Interaction, button: discord.ui.Button):
        return await interaction.response.send_modal(AddHostModal())

    @discord.ui.button(label='📃 List Hosts', style=discord.ButtonStyle.grey, custom_id='ssh_menu:list')
    async def list_hosts(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ListHostsDropdownView(interaction.user.id)
        await view.async_setup()
        await interaction.response.send_message("Select a host:", view=view, ephemeral=True)