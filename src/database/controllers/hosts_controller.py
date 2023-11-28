import aiosqlite
from loguru import logger
from src.helper.config import Config
from src.database.schema.host_schema import HostSchema

class HostsController:
    def __init__(self):
        self.config = Config()
        self.db_path = 'src/database/storage/hosts.sqlite'

    async def create_table(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS hosts_db (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner TEXT NOT NULL,
                    ip TEXT NOT NULL,
                    port TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    key TEXT
                );
            ''')
            await db.commit()

    async def add_host(self, host_schema: HostSchema) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT INTO hosts_db (owner, ip, port, username, password, key)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (host_schema.owner, host_schema.ip, host_schema.port, host_schema.username, host_schema.password, host_schema.key))
                await db.commit()
                return True
            except aiosqlite.Error as e:
                logger.error(f"Error adding host: {e}")
                return False

    async def remove_host(self, ip: str, port: str) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("DELETE FROM hosts_db WHERE ip = ? AND port = ?", (ip, port))
                await db.commit()
                return True
            except aiosqlite.Error as e:
                logger.error(f"Error removing host: {e}")
                return False

    async def edit_host(self, old_schema: HostSchema, new_schema: HostSchema) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("UPDATE hosts_db SET ip = ?, port = ?, username = ?, password = ?, key = ? WHERE owner = ? AND ip = ? AND port = ?", (new_schema.ip, new_schema.port, new_schema.username, new_schema.password, new_schema.key, old_schema.owner, old_schema.ip, old_schema.port))
                await db.commit()
                return True
            except aiosqlite.Error as e:
                logger.error(f"Error editing host: {e}")
                return False

    async def host_exists(self, ip: str, port: str) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute("SELECT * FROM hosts_db WHERE ip = ? AND port = ?", (ip, port))
                host = await cursor.fetchone()
                return host is not None
            except aiosqlite.Error as e:
                logger.error(f"Error checking if host exists: {e}")
                return False

    async def is_owner_of_host(self, owner_id: int, ip: str, port: str) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute("SELECT * FROM hosts_db WHERE owner = ? AND ip = ? AND port = ?", (owner_id, ip, port))
                host = await cursor.fetchone()
                return host is not None
            except aiosqlite.Error as e:
                logger.error(f"Error checking if host exists: {e}")
                return False

    async def get_host(self, owner_id: int, ip: str, port: str) -> HostSchema or None:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute("SELECT * FROM hosts_db WHERE owner = ? AND ip = ? AND port = ?", (owner_id, ip, port))
                host = await cursor.fetchone()
                return HostSchema(*host) if host else None
            except aiosqlite.Error as e:
                logger.error(f"Error getting host: {e}")
                return None

    async def get_hosts_by_owner(self, owner_id: int) -> list[HostSchema] or list[None]:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute("SELECT * FROM hosts_db WHERE owner = ?", (owner_id,))
                hosts = await cursor.fetchall()
                return [HostSchema(*host) for host in hosts] if hosts else []
            except aiosqlite.Error as e:
                logger.error(f"Error getting hosts: {e}")
                return []
