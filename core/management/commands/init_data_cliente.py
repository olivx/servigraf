import pymysql
from django.core.management.base import BaseCommand

from core.models import Cliente


class Command(BaseCommand):



    def connect(self, query):
        """Conecta com banco de dados e devolve um cursor """
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='grafica')
        cursor = con.cursor()
        cursor.execute(query)

        return cursor

    def init_client(self):
        """Faz o cursor.fetchall e o insert parao banco que estamo testando"""
        print('Varrendo Clientes....')
        cursor = self.connect('select * from cliente')

        client_list = []
        for row in cursor.fetchall():
            mensalista = True
            documento = ''
            tipo = 0
            # verifica se é mensalista
            if row[17] == b'\x00':
                mensalista = False

            # verifica se o documento é cpf ou cnpj
            if row[3] == 'J':
                documento = row[4]
                tipo = 1
            else:
                documento = row[5]
                tipo = 2

            data = {
                'id': row[0],
                'razao_social': row[1],
                'nome_fantasia': row[2],
                'tipo': tipo,
                'documento': documento,
                'user_id': row[10],
                'status': row[11],
                'ramo': row[12],
                'ie': row[13],
                'mensalista': mensalista,
            }
            client_list.append(data)

        print('Inportando para banco de dados atual....')
        for data in client_list:
            Cliente.objects.create(razao_social=data['razao_social'],
                                   nome_fantasia=data['nome_fantasia'],
                                   documento=data['documento'],
                                   mensalista=data['mensalista'],
                                   ramo=data['ramo'],
                                   tipo=data['tipo'])
        print('Clientes Importado com Sucesso !')



    def handle(self, *args, **options):
        self.init_client()
