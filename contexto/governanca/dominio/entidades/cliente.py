from dataclasses import dataclass, field
from datetime import datetime

from contexto.governanca.dominio.objeto_de_valor.cliente import ClienteID, Genero
from contexto.vendas.dominio.entidades.plano import Plano
from libs.ddd.entidade import Entidade


@dataclass
class Cliente(Entidade):
    id: ClienteID

    cpf: str
    nome: str
    email: str
    genero: Genero
    renda_mensal: float
    data_de_nascimento: datetime

    # Campo Virtual ORM
    planos_contratados: list[Plano] = field(default_factory=list)

    @classmethod
    def criar(
        cls,
        cpf: str,
        nome: str,
        email: str,
        genero: Genero,
        renda_mensal: float,
        data_de_nascimento: datetime,
    ) -> "Cliente":
        return cls(
            id=ClienteID(),
            cpf=cpf,
            nome=nome,
            email=email,
            genero=genero,
            renda_mensal=renda_mensal,
            data_de_nascimento=data_de_nascimento,
        )

    @property
    def idade(self) -> int:
        return datetime.now().year - self.data_de_nascimento.year
