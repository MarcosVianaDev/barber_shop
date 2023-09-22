from datetime import date
from gsheets_db import Gsheets_db, SPREADSHEET_ID


CABECALHO_BARBEARIAS_RANGE = 'barbearias!A:H'
CABECALHO_BARBEIROS_RANGE = 'barbeiros!A:F'
CABECALHO_PROPRIETARIOS_RANGE = 'proprietarios!A:H'

planilha = Gsheets_db()


def raw_to_dict(raw_data: list) -> dict:
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

def getIdRow(aba: str, id: str | None = None) -> str | None:
    list_id = list(planilha.getValues(range=f'{aba}!A:A'))
    if id:
        return f'{aba}!A{list_id.index([id])+1}'
    return list_id
    

def getData(aba: str, id: str | None = None):
    if aba == 'barbearias': raw_data = planilha.getValues(range=CABECALHO_BARBEARIAS_RANGE)
    elif aba == 'barbeiros': raw_data = planilha.getValues(range=CABECALHO_BARBEIROS_RANGE)
    elif aba == 'proprietarios': raw_data = planilha.getValues(range=CABECALHO_PROPRIETARIOS_RANGE)
    dict_data = raw_to_dict(raw_data)
    # print(dict_data)
    if id is not None:
        try:
            return dict_data[id]
        except:
            return None
    return dict_data

def createData(aba: str, nome: str, apelido: str, local_trabalho: int | str, ativo: int):
    dados = [[
        getIdRow(aba=aba).__len__(),
        nome,
        apelido,
        f'{date.today().day}/{date.today().month}/{date.today().year}',
        local_trabalho,
        ativo
    ]]
    result = planilha.insertValues(
        range=CABECALHO_BARBEIROS_RANGE, new_values=dados)
    return result['updates']['updatedRange']

def updateData(aba:str, id: int, nome: str | None = None, apelido: str | None = None, local_trabalho: int | str | None = None, ativo: int | None = None):
    old_values = getData(aba=aba, id=id)
    item_row = getIdRow(aba=aba, id=id)
    new_values = [[
        id,
        nome if nome else old_values['nome_completo'],
        apelido if apelido else old_values['apelido'],
        old_values['data_cadastro'],
        local_trabalho if local_trabalho else old_values['local_trabalho'],
        ativo if ativo is not None else old_values['ativo']
    ]]
    resp = planilha.setValues(range=item_row, new_values=new_values)
    return resp['updatedRange']

if __name__ == '__main__':
    print(getData('barbeiros', '33'))
