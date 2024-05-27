from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self

from contexto.vendas.dominio.objeto_de_valor.produto import ProdutoID
from libs.ddd.entidade import Entidade


@dataclass
class Produto(Entidade):
    id: ProdutoID
    nome: str
    susep: str
    expiracao_da_venda: datetime
    valor_minimo_aporte_inicial: float
    valor_minimo_aporte_extra: float
    idade_de_entrada: int
    idade_de_saida: int
    carencia_inicial_de_resgate: int
    carencia_entre_resgates: int

    @classmethod
    def criar(
        cls,
        nome: str,
        susep: str,
        expiracao_da_venda: str,
        valor_minimo_aporte_inicial: float,
        valor_minimo_aporte_extra: float,
        idade_de_entrada: int,
        idade_de_saida: int,
        carencia_inicial_de_resgate: int,
        carencia_entre_resgates: int,
    ) -> Self:
        return cls(
            id=ProdutoID(),
            nome=nome,
            susep=susep,
            expiracao_da_venda=expiracao_da_venda,
            valor_minimo_aporte_inicial=valor_minimo_aporte_inicial,
            valor_minimo_aporte_extra=valor_minimo_aporte_extra,
            idade_de_entrada=idade_de_entrada,
            idade_de_saida=idade_de_saida,
            carencia_inicial_de_resgate=carencia_inicial_de_resgate,
            carencia_entre_resgates=carencia_entre_resgates,
        )

    def produto_esta_expirado(self, data: Optional[datetime] = None) -> bool:
        if data is None:
            data = datetime.now()
        return data.date() > self.expiracao_da_venda

    def pode_realizar_aporte(self, valor: float) -> bool:
        return valor >= self.valor_minimo_aporte_inicial

    def pode_realizar_aporte_extra(self, valor: float) -> bool:
        return valor >= self.valor_minimo_aporte_extra

    def idade_do_cliente_de_entrada_eh_valida(self, idade: int) -> bool:
        return self.idade_de_entrada <= idade

    def idade_do_cliente_de_saida_eh_valida(self, idade: int) -> bool:
        return idade <= self.idade_de_saida
