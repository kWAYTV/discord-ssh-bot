import aiosqlite, logging
from src.database.schema.host_schema import HostSchema

logger = logging.getLogger(__name__)

class SessionsController:
    def __init__(self):
        self.db_path = 'src/database/storage/sessions.sqlite'

    async def create_table(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS ssh_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner TEXT NOT NULL,
                    ip TEXT NOT NULL,
                    port TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT,
                    key TEXT,
                    discord_channel_id TEXT NOT NULL,
                    last_used TEXT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            await db.commit()

    async def add_session(self, host_schema: HostSchema, discord_channel_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT INTO ssh_sessions (owner, ip, port, username, password, key, discord_channel_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (host_schema.owner, host_schema.ip, host_schema.port, host_schema.username, host_schema.password, host_schema.key, discord_channel_id))
                await db.commit()
                # return the id of the session
                return await self.get_session_id(host_schema.owner, host_schema.ip, host_schema.port)
            except aiosqlite.Error as e:
                logger.error(f"Error adding session: {e}")
                return False

    async def remove_session(self, id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("DELETE FROM ssh_sessions WHERE id = ?", (id,))
                await db.commit()
                return True
            except aiosqlite.Error as e:
                logger.error(f"Error removing session: {e}")
                return False

    async def update_session_last_used(self, id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("UPDATE ssh_sessions SET last_used = CURRENT_TIMESTAMP WHERE id = ?", (id,))
                await db.commit()
                return True
            except aiosqlite.Error as e:
                logger.error(f"Error updating session last used: {e}")
                return False

    async def clear_unused_sessions(self):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("DELETE FROM ssh_sessions WHERE last_used < datetime('now', '-1 hour')")
                await db.commit()
                return True
            except aiosqlite.Error as e:
                logger.error(f"Error clearing unused sessions: {e}")
                return False

    async def get_session(self, id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                async with db.execute("SELECT * FROM ssh_sessions WHERE id = ?", (id,)) as cursor:
                    row = await cursor.fetchone()
                    if row is None:
                        return None
                    return HostSchema(row[1], row[2], row[3], row[4], row[5], row[6])
            except aiosqlite.Error as e:
                logger.error(f"Error getting session: {e}")
                return None

    async def get_sessions(self, discord_channel_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                async with db.execute("SELECT * FROM ssh_sessions WHERE discord_channel_id = ?", (discord_channel_id,)) as cursor:
                    rows = await cursor.fetchall()
                    if rows is None:
                        return None
                    return [HostSchema(row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]
            except aiosqlite.Error as e:
                logger.error(f"Error getting sessions: {e}")
                return None

    async def session_exists(self, owner_id: int, ip: str, port: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute("SELECT * FROM ssh_sessions WHERE owner = ? AND ip = ? AND port = ?", (owner_id, ip, port))
                session = await cursor.fetchone()
                if session is None:
                    return False
                return HostSchema(*session)
            except aiosqlite.Error as e:
                logger.error(f"Error checking if session exists: {e}")
                return False

    async def is_owner_of_session(self, owner_id: int, id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute("SELECT * FROM ssh_sessions WHERE owner = ? AND id = ?", (owner_id, id))
                session = await cursor.fetchone()
                return session is not None
            except aiosqlite.Error as e:
                logger.error(f"Error checking if session exists: {e}")
                return False

    async def get_owner_of_session(self, id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute("SELECT * FROM ssh_sessions WHERE id = ?", (id,))
                session = await cursor.fetchone()
                return session[1]
            except aiosqlite.Error as e:
                logger.error(f"Error checking if session exists: {e}")
                return None

    async def get_channel_of_session(self, id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute("SELECT * FROM ssh_sessions WHERE id = ?", (id,))
                session = await cursor.fetchone()
                return session[7]
            except aiosqlite.Error as e:
                logger.error(f"Error checking if session exists: {e}")
                return None

    async def get_session_id(self, owner_id: int, ip: str, port: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute("SELECT * FROM ssh_sessions WHERE owner = ? AND ip = ? AND port = ?", (owner_id, ip, port))
                session = await cursor.fetchone()
                return session[0]
            except aiosqlite.Error as e:
                logger.error(f"Error checking if session exists: {e}")
                return None

    async def get_session_by_channel(self, discord_channel_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute("SELECT * FROM ssh_sessions WHERE discord_channel_id = ?", (discord_channel_id,))
                session = await cursor.fetchone()
                return HostSchema(*session) if session else None
            except aiosqlite.Error as e:
                logger.error(f"Error getting session: {e}")
                return None