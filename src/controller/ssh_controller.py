import paramiko
from loguru import logger

class SSHController:
    def __init__(self, database_id: int, owner: int, host: str, port: int, username: str, password: str, key: str, discord_channel_id: int, last_used: str = None):
        self.id = database_id
        self.owner = owner
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key = key
        self.discord_channel_id = discord_channel_id
        self.last_used = last_used
        self.client = None

    async def connect(self) -> bool:
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.key: self.client.connect(self.host, port=self.port, username=self.username, pkey=self.key)
            else: self.client.connect(self.host, port=self.port, username=self.username, password=self.password)
            
            return True
        except Exception as e:
            logger.critical(f"Error connecting to host: {e}")
            return False
    
    async def execute(self, command: str) -> str or None:
        if self.client is None:
            return "Not connected to SSH server."
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode('utf-8') + stderr.read().decode('utf-8')
        except Exception as e:
            logger.critical(f"Error executing command: {e}")
            return None
    
    async def close(self) -> bool:
        if self.client:
            self.client.close()
            self.client = None
            return True
        return False