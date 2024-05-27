import os
from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings


def buscar_arquivo_env():
    root = Path(__file__).parent.parent.parent

    root_path = os.getenv("ROOT_PATH")
    if root_path and root_path != "":
        root = Path(root_path)

    # verifica se o arquivo .env existe
    if (root / ".env").exists():
        print("Arquivo .env encontrado")
        return root / ".env"

    # verifica se o arquivo .env.example existe
    if (root / ".env.example").exists():
        print("Arquivo .env não encontrado, utilizando .env.example")
        return root / ".env.example"

    # se não encontrar nenhum, retorna None para utilizar as variáveis do sistema
    print("Arquivo .envs não encontrados, utilizando variáveis do sistema")
    return None


class GerenciadorDeENVs(BaseSettings):
    DEBUG: bool = False

    DB_USER: Final[str]
    DB_PASS: Final[str]
    DB_HOST: Final[str]
    DB_PORT: Final[int]
    DB_NAME: str

    SERVER_HOST: Final[str]
    SERVER_PORT: Final[int]
    SERVER_WORKERS: Final[int]

    @property
    def DB_URI(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = buscar_arquivo_env()


ENVS = GerenciadorDeENVs()
