import redis


class RedisCache:
    def __init__(self, host="localhost", port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db)

    def __del__(self):
        if self.client:
            self.client.close()

    def set(self, key, value):
        """Set a key-value pair in Redis."""

        self.client.set(key, value)

    def get(self, key):
        """Get the value of a key from Redis."""

        return self.client.get(key)
