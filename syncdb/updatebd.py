import itertools
import requests
from connect_database import ConnectDatabase


def get_orgaos(input):
    result = {}
    for i in input:
        servico_id = i['id'].split('/')[6]
        servico_nome = i['nome']
        orgao_id = i['orgao']['id'].split('/')[5]
        orgao_nome = i['orgao']['nomeOrgao']
        if orgao_id in result:
            result[orgao_id].append({'servico_id': servico_id, 'servico_nome': '{0}'.format(servico_nome), 'orgao_nome': '{0}'.format(orgao_nome,),
                                     'orgao_id': orgao_id.zfill(8)})
        else:
            result[orgao_id] = [{'servico_id': servico_id, 'servico_nome': '{0}'.format(servico_nome), 'orgao_nome': '{0}'.format(orgao_nome),
                                 'orgao_id': orgao_id.zfill(8)}]
    return result

def get_dataset(orgaos):
    orgaos_output = {}
    servicos_output = {}

    for o in orgaos:
        orgaos_output.update({
            '{0}'.format(orgaos[o][0]['orgao_id']):'{0}'.format(orgaos[o][0]['orgao_nome'].replace('&lt;', '<').replace('&gt;', '>')),
        })

        for s in orgaos[o]:
            servicos_output.update({
                '{0}{1}'.format(s['servico_id']):'{0}'.format(s['servico_nome'].replace('&lt;', '<').replace('&gt;', '>')),
            })

    return orgaos_output, servicos_output

if __name__ == '__main__':

        # Url for the serv.
        url = 'https://www.servicos.gov.br/api/v1/servicos/'

        # Variables used to insert into db
        qid_orgao = qid1  # replace with the question id
        qid_servico = qid2 # replace with the question id
        table = table # replace with the table
        column_table = column_table # replace with the column of the table

        response = requests.get(url)

        # Use API and get the serv. and org. and return dict
        orgaos_set = get_orgaos(response.json()['resposta'])
        orgaos_set, servicos_set = get_dataset(orgaos_set)

        # Connect to db and get tuples with current answer 
        orgaos_db_tp = ConnectDatabase.queryAnswer(qid_orgao)
        servicos_db_tp = ConnectDatabase.queryAnswer(qid_servico)

        # Convert tuples to dict
        orgaos_db = dict((y, x) for x, y in orgaos_db_tp)
        servicos_db = dict((y, x) for x, y in servicos_db_tp)
        table, old, new, column_table, column_value
        for code in orgaos_db: 
            ConnectDatabase.updateAnswer(table, qid_orgao, code, orgaos_set[code])
            print(code)

        for code in servicos_db:
            ConnectDatabase.updateAnswer(table, qid_servico, code, servicos_set[code])
            print(code)
