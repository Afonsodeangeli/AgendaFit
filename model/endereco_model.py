from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.usuario_model import Usuario

@dataclass
class Endereco:
    id_endereco: int
    id_usuario: int
    titulo: str
    logradouro: str
    numero: int
    complemento: str
    bairro: str
    cidade: str
    uf: str
    cep: int

    usuario: Optional[Usuario]
    