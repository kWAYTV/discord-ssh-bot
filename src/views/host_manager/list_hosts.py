import discord, traceback
from src.views.host_client.host_panel import HostPanelView
from src.database.controllers.hosts_controller import HostsController

class ListHostsDropdown(discord.ui.Select):
    def __init__(self, hosts, options=[]):
        super().__init__(custom_id="ssh_bot:hostlistdrop", placeholder="Select an option", max_values=1, min_values=1, options=options)
        self.hosts = hosts  # Save a reference to the hosts

    async def callback(self, interaction: discord.Interaction):
        try:
            selected_value = self.values[0]

            selected_host = next((host for host in self.hosts if f"{host.ip}:{host.port}" == selected_value), None)
            if not selected_host:
                return await interaction.response.send_message("Host not found.", ephemeral=True)

            embed = discord.Embed(title="Host Panel", description= "Here are your host details:", color=discord.Color.green())
            embed.add_field(name="Host Owner", value=f"<@{selected_host.owner}> (||{selected_host.owner}||)", inline=True)
            embed.add_field(name="Host Address", value=f"||{selected_host.ip}||:||{selected_host.port}||", inline=False)
            embed.add_field(name="Host Username", value=f"||{selected_host.username}||", inline=True)
            embed.add_field(name="Host Password", value=f"||{selected_host.password}||", inline=True)
            embed.add_field(name="Host Key", value=f"||```{selected_host.key}```||", inline=False)
            
            return await interaction.response.send_message(f"Welcome to your host panel!", embed=embed, view=HostPanelView(selected_host), ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred listing hosts: {e}", ephemeral=True)
            traceback.print_exc()

class ListHostsDropdownView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.dropdown = None
        self.user_id = user_id
        self.hosts_controller = HostsController()

    async def async_setup(self):
        hosts = await self.hosts_controller.get_hosts_by_owner(self.user_id)

        if not hosts:
            # Create an dummy option to display
            self.dropdown = ListHostsDropdown(hosts, [discord.SelectOption(label="No hosts found.", description="Add hosts to use this feature!", emoji="❌", value="no_hosts")])
            self.add_item(self.dropdown)
            return

        options = [discord.SelectOption(label=f"{host.ip}:{host.port}", description="Click me to manage this host.", emoji="🔑", value=f"{host.ip}:{host.port}") for host in hosts]
        self.dropdown = ListHostsDropdown(hosts, options)

        self.add_item(self.dropdown)