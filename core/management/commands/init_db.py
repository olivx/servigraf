import pymysql
from django.core.management.base import BaseCommand

from catalogo.models import Produto
from core.models import Cliente, Contato, Endereco


class Command(BaseCommand):
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = 'root'
        self.db_name = 'grafica'

    def add_arguments(self, parser):

        parser.add_argument('--all', '-a',
                            action='store_true',
                            help='inicializa todas as tabelas')

        parser.add_argument('--client', '-cli',
                            action='store_true',
                            help='iniciliza a tabela de clientes')
        parser.add_argument('--contact', '-cont',
                            action='store_true',
                            help='inicializa a tablça de  contatos')

        parser.add_argument('--end', '-e',
                            action='store_true',
                            help='inicializa a tabela de endereço')

        parser.add_argument('--prod', '-p',
                            action='store_true',
                            help='inicializa a tabela de produtos')

    def connect(self, query):
        """Conecta com banco de dados e devolve um cursor """
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                               passwd=self.password, db=self.db_name)
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor

    def get_rows(self, cursor):
        columns = tuple([desc[0] for desc in cursor.description])
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return rows

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
            Cliente.objects.create(
                id=data['id'],
                razao_social=data['razao_social'],
                nome_fantasia=data['nome_fantasia'],
                documento=data['documento'],
                mensalista=data['mensalista'],
                ramo=data['ramo'],
                tipo=data['tipo'])
        print('Clientes Importado com Sucesso !')

    def init_contato(self):
        print('varrendo contato...')
        cursor = self.connect('select * from contato')

        print('importando contato de clientes dados...')
        for row in self.get_rows(cursor):
            cli = Cliente.objects.get(id=row['clienteid'])
            Contato.objects.create(
                nome=row['nome'],
                sobre_nome=row['sobrenome'],
                observacao=row['descricao'],
                cliente=cli
            )
        print('Contatos importado com sucesso!')

    def init_endereco(self):
        print('varrendo endereços..')
        cursor = self.connect('select * from end')

        print('importando dados de endereços de clientes...')
        for row in self.get_rows(cursor):
            if row['clienteid'] is not 0:
                cliente = Cliente.objects.get(id=row['clienteid'])

                tipo_end = 2
                if row['status'] == 'RESIDENCIAL':
                    tipo_end = 1
                if row['status'] == 'ENTREGA':
                    tipo_end = 3
                if row['status'] == 'COBRANÇA':
                    tipo_end = 4

                Endereco.objects.create(
                    cliente=cliente,
                    logradouro=row['tipo_lagradouro'],
                    endereco=row['rua'],
                    numero=row['largadouro'],
                    complemento=row['complemento'],
                    cep=row['cep'],
                    bairro=row['bairro'],
                    cidade=row['cidade'],
                    uf=row['estado'],
                    tipo_end=tipo_end,
                    observacao=row['obj']
                )

    def init_produtos(self):
        print('varrendo dados de produtos...')
        conn = self.connect('select * from produto')

        desc = tuple([desc[0] for desc in conn.description])
        rows = [dict(zip(desc, row)) for row in conn.fetchall()]

        print('importando produtos...')
        for row in rows:
            tipo = 1
            if row['tipo'] == 'SERVICO':
                tipo = 2

            Produto.objects.create(
                id=row['produtoid'],
                nome=row['nome'],
                desc=row['descricao'],
                quantidade=row['qdt'],
                valor=row['preco'],
                tipo=tipo,
                data_create=row['dataCadastro'],
                data_update=row['dataUpdate']

            )


    def handle(self, *args, **options):

        if options['client'] or options['all']:
            self.init_client()

        if options['contact'] or options['all']:
            self.init_contato()

        if options['end'] or options['all']:
            self.init_endereco()

        if options['prod'] or options['all']:
            self.init_produtos()
