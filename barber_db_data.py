from datetime import date
from gsheets_db import Gsheets_db, SPREADSHEET_ID


CABECALHO_BARBEARIAS_RANGE = 'barbearias!A:H'
CABECALHO_BARBEIROS_RANGE = 'barbeiros!A:F'
CABECALHO_PROPRIETARIOS_RANGE = 'proprietarios!A:H'

planilha = Gsheets_db()


def raw_to_dict(raw_data) -> dict:
    dict_data = {}
    for x in range(len(raw_data)):
        if x == 0:
            continue
        dict_data[raw_data[x][0]] = {}
        for item in range(raw_data[x].__len__()):
            if item == 0:
                continue
            dict_data[raw_data[x][0]][raw_data[0][item]] = raw_data[x][item]
    # print(dict_data)
    return dict_data

def getIdRow(aba: str, id: str | None = None):
    list_id = list(planilha.getValues(range=f'{aba}!A:A'))
    if id:
        return f'{aba}!A{list_id.index([id])+1}'
    return list_id
    

def getData(aba: str, id: str | None = None):
    raw_data = []
    if aba == 'barbearias': raw_data = planilha.getValues(range=CABECALHO_BARBEARIAS_RANGE)
    elif aba == 'barbeiros': raw_data = planilha.getValues(range=CABECALHO_BARBEIROS_RANGE)
    elif aba == 'proprietarios': raw_data = planilha.getValues(range=CABECALHO_PROPRIETARIOS_RANGE)
    dict_data = raw_to_dict(raw_data)
    if id is not None:
        try:
            return dict_data[id]
        except:
            return None
    return dict_data

def createData(aba: str, nome: str, apelido: str | None = None, local_trabalho: str | None = None, ativo: str = '1', dono_de: str | None = None, telefone: str | None = None, email: str | None = None, responsavel: str | None = None, cep: str | None = None):
    if (aba == 'barbeiros'):
        dados = [[
            getIdRow(aba=aba).__len__(),
            nome,
            apelido,
            f'{date.today().day}/{date.today().month}/{date.today().year}',
            local_trabalho,
            ativo
        ]]
    elif (aba == 'barbearias'):
        dados = [[
            getIdRow(aba=aba).__len__(),
            nome,
            f'{date.today().day}/{date.today().month}/{date.today().year}',
            responsavel,
            email,
            telefone,
            cep,
            ativo
        ]]
    elif (aba == 'proprietarios'):
        dados = [[
            getIdRow(aba=aba).__len__(),
            nome,
            f'{date.today().day}/{date.today().month}/{date.today().year}',
            dono_de,
            telefone,
            email,
            ativo
        ]]
    else:
        return 'Aba não econtrada...'
    result = planilha.insertValues(
        range=f'{aba}!A1', new_values=dados)
    return result['updates']['updatedRange']

def updateData(aba:str, id: str, data_cadastro: str, nome: str | None = None, apelido: str | None = None, local_trabalho: str | None = None, ativo: str | None = None, dono_de: str | None = None, telefone: str | None = None, email: str | None = None, responsavel: str | None = None, cep: str | None = None):
    item_row = getIdRow(aba=aba, id=id)
    if aba == 'barbearias': new_values = [[
        id,
        nome,
        data_cadastro,
        responsavel,
        email,
        telefone,
        cep,
        ativo
    ]]
    elif aba == 'barbeiros': new_values = [[
        id,
        nome,
        apelido,
        data_cadastro,
        local_trabalho,
        ativo
    ]]
    elif aba == 'proprietarios': new_values = [[
        id,
        nome,
        data_cadastro,
        dono_de,
        telefone,
        email,
        ativo
    ]]

    resp = planilha.setValues(range=item_row, new_values=new_values)
    return resp['updatedRange']

if __name__ == '__main__':
    print(getData('barbeiros', '33'))
