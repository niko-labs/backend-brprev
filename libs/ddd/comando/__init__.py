import abc

from pydantic import BaseModel


class Comando(abc.ABC, BaseModel):
    ...
