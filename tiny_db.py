from pydantic import BaseModel
from tinydb import TinyDB


class Barbeiro(BaseModel):
    nome: str
    apelido: str
    data_de_cadastro: str
    local_trabalho: tuple
    ativo: bool


class Proprietario(BaseModel):
    nome: str
    data_de_cadastro: str
    dono_de: tuple
    telefone: str
    email: str
    ativo: bool


class Barbearia(BaseModel):
    nome: str
    data_de_cadastro: str
    responsavel: int
    telefone: str
    email: str
    cep: str
    ativo: bool


class Barber_DB:
    def __init__(self) -> None:
        self.__db_barbeiros = TinyDB('DB/barbeiros.json')
        self.__db_barbearias = TinyDB('DB/barbearias.json')
        self.__db_proprietarios = TinyDB('DB/proprietarios.json')

    def create_Barbeiro(self, novo_barbeiro:Barbeiro) -> int:
        '''Create a new barbeiro and return ID'''
        return self.__db_barbeiros.insert(novo_barbeiro)

    def get_Barbeiro(self, id: int | None = None) -> Barbeiro:
        if id:
            return self.__db_barbeiros.get(id)
        else:
            return self.__db_barbeiros.all()

    def set_Barbeiro(self, id: int, doc:Barbeiro):
        return self.__db_barbeiros.update(fields=doc, doc_ids=[id])

    def create_Barbearia(self, nova_barbearia:Barbearia) -> int:
        '''Create a new barbearia and return ID'''
        return self.__db_barbearias.insert(nova_barbearia)

    def get_Barbearia(self, id: int | None = None) -> Barbearia:
        if id:
            return self.__db_barbearias.get(id)
        else:
            return self.__db_barbearias.all()

    def set_Barbearia(self, id: int, doc:Barbearia):
        return self.__db_barbearias.update(fields=doc, doc_ids=[id])

    def create_Proprietario(self, novo_proprietario:Proprietario) -> int:
        '''Create a new proprietario and return ID'''
        return self.__db_proprietarios.insert(novo_proprietario)

    def get_Proprietario(self, id: int | None = None) -> Proprietario:
        if id:
            return self.__db_proprietarios.get(id)
        else:
            return self.__db_proprietarios.all()

    def set_Proprietario(self, id: int, doc:Proprietario):
        return self.__db_proprietarios.update(fields=doc, doc_ids=[id])


if __name__ == '__main__':
    db = Barber_DB()

    novo_barbeiro ={}
    # novo_barbeiro['nome'] = 'Marcelo Aguiar Souza'
    novo_barbeiro['apelido'] = 'Seu Souza'
    # novo_barbeiro['data_de_cadastro'] = '22/09/2023'
    novo_barbeiro['local_trabalho'] = '2;4'
    # novo_barbeiro['ativo'] = True
    # db.Novo_Barbeiro( novo_barbeiro )
    # print(db.get_Barbeiro(2))
    print (db.set_Barbeiro(2, novo_barbeiro))
