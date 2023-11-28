import traceback
from loguru import logger
from src.database.controllers.hosts_controller import HostsController
from src.database.controllers.sessions_controller import SessionsController

class DatabaseLoader:
    def __init__(self) -> None:
        self.hosts_controller = HostsController()
        self.sessions_controller = SessionsController()

    async def setup(self) -> None:
        try:
            await self.hosts_controller.create_table()
            await self.sessions_controller.create_table()
        except Exception as e:
            logger.critical(f"Error setting up database: {e}")
            traceback.print_exc()