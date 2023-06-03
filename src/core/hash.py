from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def password_verify(password: str, hash_password: str) -> bool:
    """
    Função para verificar se a senha está correta, comparando
    a senha em texto puro, informada pelo usuário, e o hash da
    senha que estará salvo no banco de dados durante a criação
    da conta.
    """
    return CRIPTO.verify(password, hash_password)


def hash_password(password: str) -> str:
    """
    Função que gera e retorna o hash da senha
    """
    return CRIPTO.hash(password)
