# Imports
import os, discord, traceback
from loguru import logger
from discord.ext import commands
from src.helper.config import Config
from src.database.loader import DatabaseLoader
from src.manager.file_manager import FileManager

# Set logging system handler
logger.add("ssh_bot.log", encoding="utf-8")

# Define the bot & load the commands, events and loops
class Bot(commands.Bot):
    def __init__(self) -> None:
        self.file_manager = FileManager()
        super().__init__(command_prefix=Config().bot_prefix, help_command=None, intents=discord.Intents.all())

    def clear_screen(self) -> None:
        os.system('cls||clear')

    # Function to load the extensions
    async def setup_hook(self) -> None:
        try:
            logger.info(f"Starting bot...")

            # Check for file inputs
            logger.debug("Checking for file inputs...")
            self.file_manager.check_input()
            self.clear_screen()

            # Load the cogs
            logger.debug("Loading cogs...")
            for filename in os.listdir("./src/cogs/commands"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.commands.{filename[:-3]}")
            self.clear_screen()

            # Load the events
            logger.debug("Loading events...")
            for filename in os.listdir("./src/cogs/events"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.events.{filename[:-3]}")
            self.clear_screen()

            # Load the loops
            logger.debug("Loading loops...")
            for filename in os.listdir("./src/cogs/loops"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.loops.{filename[:-3]}")
            self.clear_screen()

            # Set-up the database
            logger.debug("Setting up databases...")
            await DatabaseLoader().setup()
            self.clear_screen()

            # Done!
            logger.info(f"Setup completed!")
            self.clear_screen()
        except Exception as e:
            logger.error(f"Error setting up bot: {e}")
            traceback.print_exc()
            exit()

# Run the bot
if __name__ == "__main__":
    try:
        bot = Bot()
        bot.run(Config().bot_token)
    except KeyboardInterrupt:
        logger.info("Goodbye!")
        exit()
    except Exception as e:
        logger.critical(f"Error running bot: {e}")
        traceback.print_exc()
        exit()
