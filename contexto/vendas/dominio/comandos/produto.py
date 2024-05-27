from datetime import datetime

from libs.ddd.comando import Comando


class CriarProduto(Comando):
    nome: str
    susep: str
    expiracao_da_venda: datetime

    valor_minimo_aporte_inicial: float
    valor_minimo_aporte_extra: float

    idade_de_entrada: int
    idade_de_saida: int

    carencia_inicial_de_resgate: int
    carencia_entre_resgates: int
