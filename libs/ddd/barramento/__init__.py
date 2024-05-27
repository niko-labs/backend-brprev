from typing import Any

from libs.ddd.comando import Comando
from libs.ddd.evento import Evento
from libs.ddd.uow import UoW


class Barramento:
    _instances = {}

    comandos: set[Comando, callable] = {}
    eventos: set[Evento, list[callable]] = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwds)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def registrar_comando(self, comando: Comando, callback: callable) -> None:
        if not issubclass(comando, Comando):
            raise Exception("O comando deve ser uma instância de Comando")

        if tem_comando := self.comandos.get(comando):
            raise Exception(
                f"O Comando Já Registrado: '{comando} -> {tem_comando.__name__}'"
            )

        self.comandos.update({comando: callback})

    def registrar_evento(self, evento: Evento, callback: callable) -> None:
        if not issubclass(evento, Evento):
            raise Exception("O evento deve ser uma instância de Evento")

        if tem_evento := self.eventos.get(evento):
            self.eventos[evento].append(callback)
        else:
            self.eventos[evento] = [callback]

    def enviar_comando(self, comando: Comando, uow: UoW):
        return self.comandos[comando.__class__](comando, uow)

    def enviar_evento(self, evento: Evento, uow: UoW):
        for callback in self.eventos[evento.__class__]:
            callback(evento, uow)
