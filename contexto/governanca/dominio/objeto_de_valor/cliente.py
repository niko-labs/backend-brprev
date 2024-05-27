import enum

from libs.pydantic.uuid import BaseUUID


class ClienteID(BaseUUID):
    ...


class Genero(enum.Enum):
    MASCULINO = "Masculino"
    FEMININO = "Feminino"
    OUTRO = "Outro"
