from datetime import date, datetime


class CreateUserOutput:
    def __init__(
        self,
        id: str,
        nome_completo: str ,
        genero: str ,
        cpf: str ,
        email: str ,
        data_nascimento: date ,
        preferencia_comunicacao: str ,
        cep: str ,
        telefone: str ,
        endereco: str ,
        created_at: datetime,
        updated_at: datetime 
    ) -> None:
        self.id = id
        self.nome_completo = nome_completo
        self.genero = genero
        self.cpf = cpf
        self.email = email
        self.data_nascimento = data_nascimento
        self.preferencia_comunicacao = preferencia_comunicacao
        self.cep = cep
        self.telefone = telefone
        self.endereco = endereco
        self.created_at = created_at
        self.updated_at = updated_at