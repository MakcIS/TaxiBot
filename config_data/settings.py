from environs import Env
from dataclasses import dataclass

env = Env()
env.read_env()

@dataclass
class Settings:
    token: str


def get_settings():
    return Settings(env('BOT_TOKEN'))