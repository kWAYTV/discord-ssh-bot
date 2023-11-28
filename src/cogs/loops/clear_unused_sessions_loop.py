from loguru import logger
from discord.ext import commands, tasks
from src.database.controllers.sessions_controller import SessionsController

class SessionsLoop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.sessions_controller = SessionsController()
        self.clear_sessions.start()

    @tasks.loop(minutes=1)
    async def clear_sessions(self):
        await self.sessions_controller.clear_unused_sessions()

    @clear_sessions.before_loop
    async def before_clear_sessions(self) -> None:
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SessionsLoop(bot))
    return logger.info("Sessions loop loaded!")