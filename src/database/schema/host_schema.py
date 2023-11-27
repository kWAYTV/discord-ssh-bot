class HostSchema:
    def __init__(self, database_id: int, owner: int, ip: str, port: str, username: str, password: str, key: str, discord_channel_id: int = None, last_used: str = None) -> None:
        self.id = database_id if database_id else None
        self.owner = int(owner)
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.key = key
        self.discord_channel_id = int(discord_channel_id) if discord_channel_id else None
        self.last_used = last_used if last_used else None

    def __repr__(self) -> str:
        return f"HostSchema({self.owner}, {self.ip}, {self.port}, {self.username}, {self.password}, {self.key}, {self.discord_channel_id}, {self.last_used})"
    
    def is_owner(self, user_id: int) -> bool:
        return int(self.owner) == int(user_id)

    def get_schema(self):
        return {
            'id': self.id,
            'owner': self.owner,
            'ip': self.ip,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'key': self.key,
            'discord_channel_id': self.discord_channel_id,
            'last_used': self.last_used
        }