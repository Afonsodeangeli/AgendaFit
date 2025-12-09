from dataclasses import dataclass


@dataclass
class Categoria:
    """
    Model de categoria de atividade do AgendaFit.

    Attributes:
        id_categoria: Identificador único da categoria
        nome: Nome da categoria
        descricao: Descrição detalhada da categoria
    """
    id_categoria: int
    nome: str
    descricao: str
