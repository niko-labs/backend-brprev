from datetime import datetime
from decimal import Decimal
from typing import Optional

from contexto.governanca.dominio.objeto_de_valor.cliente import ClienteID
from contexto.vendas.dominio.objeto_de_valor.plano import PlanoID
from contexto.vendas.dominio.objeto_de_valor.produto import ProdutoID
from contexto.vendas.erros.plano import (
    ErroPlanoNaoPodeSerFinalizadoJaQueAindaPossuiAporte,
    ErroValorDoResgateMaiorQueAporte,
)
from libs.ddd.entidade import Entidade


class Plano(Entidade):
    id: PlanoID
    id_produto: ProdutoID
    id_cliente: ClienteID

    aporte: float
    plano_finalizado: bool
    data_da_contratacao: str
    idade_de_aposentadoria: int
    ultimo_resgate: Optional[datetime] = None

    @classmethod
    def criar(
        cls,
        id_produto: ProdutoID,
        id_cliente: ClienteID,
        aporte: float,
        data_da_contratacao: str,
        idade_de_aposentadoria: int,
        plano_finalizado: bool = False,
    ) -> "Plano":
        return cls(
            id=PlanoID(),
            id_produto=id_produto,
            id_cliente=id_cliente,
            aporte=aporte,
            data_da_contratacao=data_da_contratacao,
            idade_de_aposentadoria=idade_de_aposentadoria,
            plano_finalizado=plano_finalizado,
        )

    @property
    def dias_desde_contratacao(self) -> int:
        return (datetime.now().date() - self.data_da_contratacao).days

    @property
    def dias_desde_ultimo_resgate(self) -> Optional[int]:
        if self.ultimo_resgate:
            return (datetime.now().date() - self.ultimo_resgate).days
        return None

    def realizar_aporte_extra(self, valor: Decimal) -> None:
        self.aporte += Decimal(valor)

    def realizar_resgate(self, valor: Decimal) -> None:
        if not self.aporte >= Decimal(valor):
            raise ErroValorDoResgateMaiorQueAporte()

        self.ultimo_resgate = datetime.now()
        self.aporte -= Decimal(valor)

        if self.aporte == 0:
            self.finalizar_plano()

    def verifica_carencia_inicial(self, dias_de_carencia: int) -> bool:
        return self.dias_desde_contratacao >= dias_de_carencia

    def finalizar_plano(self) -> None:
        if self.aporte == 0:
            self.plano_finalizado = True
        else:
            raise ErroPlanoNaoPodeSerFinalizadoJaQueAindaPossuiAporte()
