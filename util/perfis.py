"""
Enum centralizado para perfis de usuario.

Este modulo define o Enum Perfil que e a FONTE UNICA DA VERDADE
para perfis de usuario no sistema.
"""

from util.enum_base import EnumEntidade


class Perfil(EnumEntidade):
    """
    Enum centralizado para perfis de usuario do AgendaFit.

    Este e a FONTE UNICA DA VERDADE para perfis no sistema.
    SEMPRE use este Enum ao referenciar perfis, NUNCA strings literais.

    Herda de EnumEntidade que fornece metodos uteis:
        - valores(): Lista todos os valores
        - existe(valor): Verifica se valor existe
        - from_valor(valor): Converte string para enum
        - validar(valor): Valida e retorna ou levanta ValueError

    Exemplos:
        - Correto: perfil = Perfil.ADMIN.value
        - Correto: perfil = Perfil.ALUNO.value
        - Correto: perfil = Perfil.PROFESSOR.value
        - ERRADO: perfil = "admin"
        - ERRADO: perfil = "aluno"
    """

    # PERFIS DO AGENDAFIT #####################################
    ADMIN = "Administrador"
    ALUNO = "Aluno"
    PROFESSOR = "Professor"
    # FIM DOS PERFIS ##########################################
