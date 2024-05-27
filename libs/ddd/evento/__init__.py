import abc

from pydantic import BaseModel


class Evento(abc.ABC, BaseModel):
    ...
