# Imports
import discord, os, traceback, logging
from discord.ext import commands
from src.helper.config import Config
from src.database.loader import DatabaseLoader
from src.manager.file_manager import FileManager

# Set logging system
logging.basicConfig(handlers=[logging.FileHandler('ssh_bot.log', 'w+', 'utf-8'), logging.StreamHandler()], level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the bot & load the commands, events and loops
class Bot(commands.Bot):
    def __init__(self) -> None:
        self.file_manager = FileManager()
        super().__init__(command_prefix=Config().bot_prefix, help_command=None, intents=discord.Intents.all())

    # Function to load the extensions
    async def setup_hook(self) -> None:
        try:
            logger.info(f"Starting bot...")

            # Check for file inputs
            logger.info("Checking for file inputs...")
            self.file_manager.check_input()

            # Load the cogs
            logger.info("Loading cogs...")
            for filename in os.listdir("./src/cogs/commands"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.commands.{filename[:-3]}")

            # Load the events
            logger.info("Loading events...")
            for filename in os.listdir("./src/cogs/events"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.events.{filename[:-3]}")

            # Load the loops
            logger.info("Loading loops...")
            for filename in os.listdir("./src/cogs/loops"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.loops.{filename[:-3]}")

            # Set-up the database
            logger.info("Setting up databases...")
            await DatabaseLoader().setup()

            # Done!
            logger.info(f"Setup completed!")
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
        logger.error(f"Error running bot: {e}")
        traceback.print_exc()
        exit()