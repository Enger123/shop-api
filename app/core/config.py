from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CACHE_TTL_SECONDS: int
    REDIS_HOST: str
    REDIS_PORT: int
    ORDER_EXCHANGE: str = "order"
    ORDER_ROUTING_KEY: str = "order.created"
    NOTIFICATIONS_QUEUE: str = "notifications.order_created"
    RABBIT_HOST: str
    EMAIL: str
    PASSWORD: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    @property
    def RABBITMQ_URL(self):
        return f"amqp://guest:guest@{self.RABBIT_HOST}:5672/"

    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()