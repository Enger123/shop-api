from dataclasses import dataclass

@dataclass
class Settings:
    DATABASE_URL: str

def get_settings():
    return Settings(
        DATABASE_URL="postgresql+psycopg://postgres:Enger123@localhost:5432/shop_api"
    )