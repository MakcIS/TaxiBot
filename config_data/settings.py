from environs import Env
from dataclasses import dataclass

env = Env()
env.read_env()

@dataclass
class TgBot:
    token: str

@dataclass
class DataBaseConfig:
    database: str
    user: str
    password: str
    port: str | int
    db_url: str

@dataclass
class DaDataConfig:
    token: str

@dataclass
class Settings:
    tg_bot: TgBot
    db_config: DataBaseConfig
    dadata: DaDataConfig




def get_settings():

    return Settings(tg_bot=TgBot(env('BOT_TOKEN')),
                    db_config=DataBaseConfig(database=env('DB_NAME'),
                                             user=env('DB_USER'),
                                             password=env('DB_PASSWORD'),
                                             port=env('DB_PORT'),
                                             db_url = f'postgresql+asyncpg://{env('DB_USER')}:{env('DB_PASSWORD')}@db:{env('DB_PORT')}/{env('DB_NAME')}',
                                             ),
                    dadata=DaDataConfig(env('DADATA_TOKEN')))
