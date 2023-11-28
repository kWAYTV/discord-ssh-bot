import discord, yaml
from yaml import SafeLoader

class Config():
    def __init__(self):

        with open("config.yaml", "r") as file:
            self.config = yaml.load(file, Loader=SafeLoader)

        # Rainbow line gif
        self.rainbow_line_gif = "https://i.imgur.com/mnydyND.gif"

        # App info
        self.app_logo = self.config["app_logo"]
        self.app_url = self.config["app_url"]
        self.app_name = self.config["app_name"]
        self.app_name_branded = f"{self.app_name} • {self.app_url}"
        self.app_version = self.config["app_version"]

        # Discord bot
        self.bot_prefix = self.config["bot_prefix"]
        self.bot_token = self.config["bot_token"]
        self.logs_channel = int(self.config["logs_channel"])
        self.chat_category = int(self.config["chat_category"])
        self.dev_guild_id = discord.Object(int(self.config["dev_guild_id"]))

        # Logs
        self.log_file = self.config["log_file"]