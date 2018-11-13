import os

import random
import re
from faker import Faker
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from catalogo.models import Produto,  GroupProduct
from core.models import Cliente, Contato, Endereco, Email, Telefone


class Command(BaseCommand):

    def __init__(self):
        self.fake = Faker('pt_BR')

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


    def init_client(self):
        '''create fake cientes to teste'''
        print('creating fake clientes....')
        client_list = []
        list_ramo = ['grafica', 'arquitetura', 'tecnologia', 'entretenimento', 'segurança', 'construção', 'restaurante','outros']
        _tipo = random.randint(1,2),
        _cpf_cnpj = self.fake.cnpj() if _tipo == 2 else self.fake.cpf()
        _mensalista = True if random.randint(1,3000) % 4 == 0 else False
        _user =  random.choice(User.objects.all())
        for _ in range(100):
            data = {
                'razao_social': f'{self.fake.catch_phrase_attribute()} {self.fake.company()} ',
                'nome_fantasia': f'{self.fake.catch_phrase_attribute()} {self.fake.company()} ',
                'tipo': random.randint(1,2),
                'documento': _cpf_cnpj,
                'user': _user,
                'ramo': random.choice(list_ramo),
                'mensalista': _mensalista,
            }
            client_list.append(Cliente(**data))
        Cliente.objects.bulk_create(client_list)

    def init_contato(self):
        print('create fake cliente ....')
        list_contatos = []
        list_emails = []
        list_phones = []

        for _ in range(300):
            cliente = random.choice(Cliente.objects.all())
            data = {
                'nome':self.fake.first_name(),
                'sobre_nome': self.fake.last_name(),
                'observacao': self.fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                'cliente': cliente
            }
            list_contatos.append(Contato(**data))
        Contato.objects.bulk_create(list_contatos)

        contatos = Contato.objects.all()
        for contato in contatos:
            data = {
                'email': self.fake.ascii_free_email(),
                'contato': contato
            }
            list_emails.append(Email(**data))
        Email.objects.bulk_create(list_emails)

        for contato in contatos:
            data = {
                'telefone': self.fake.msisdn(),
                'tipo': random.randint(1,9),
                'contato': contato
            }
            list_phones.append(Telefone(**data))
        Telefone.objects.bulk_create(list_phones)

    def init_endereco(self):
        print('creando fake endereços de clientes...')
        list_end = []
        for _ in range(400):
            complemento_list = ['ap', 'casa', '']
            tipo_comp = random.choice(complemento_list)
            cliente =  random.choice(Cliente.objects.all())
            if tipo_comp == 'ap':
                tipo_comp = '%s %s' % (tipo_comp, random.randint(10, 200))
            if tipo_comp == 'casa':
                tipo_comp = '%s %s' % (tipo_comp, random.randint(1, 5))

            tipo_end = random.randint(1, 4)
            data = {
                'cliente':cliente,
                'logradouro': self.fake.street_prefix(),
                'endereco': self.fake.street_name(),
                'numero': self.fake.building_number(),
                'complemento': tipo_comp,
                'cep': self.fake.postcode(),
                'bairro': self.fake.neighborhood(),
                'cidade': self.fake.city(),
                'uf': self.fake.state_abbr(),
                'tipo_end':tipo_end,
                'observacao':self.fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
            }
            list_end.append(Endereco(**data))
        Endereco.objects.bulk_create(list_end)

    def init_produtos(self):
        print('create fake produtos...')
        list_prod = []
        list_group = []

        for _  in range(20):
            data = {
                'group': self.fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                'desc': self.fake.sentence(nb_words=20, variable_nb_words=True, ext_word_list=None)
            }
            list_group.append(GroupProduct(**data))

        for _ in range(600):
            tipo = random.randint(1,2)
            quantidade = random.randint(1,200)
            title = self.fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
            description = self.fake.sentence(nb_words=20, variable_nb_words=True, ext_word_list=None)
            val = round(random.uniform(0.5, 95.9),2)
            data = {
                'nome': title,
                'desc': description,
                'quantidade': quantidade,
                'valor': val,
                'tipo': tipo,
                'group': random.choice(list_group),
                'data_create': self.fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None),
                'data_update': self.fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
            }
            list_prod.append(Produto(**data))

    def handle(self, *args, **options):

        if User.objects.count() < 30:
            user_list = []
            for _ in range(30):
                data = {
                    'first_name': self.fake.first_name(),
                    'last_name': self.fake.last_name(),
                    'username': self.fake.ascii_free_email(),
                    'email': self.fake.ascii_free_email(),
                    'password':'hashedPasswordStringPastedHereFromStep1!',
                    'is_active':True,
                }
                user_list.append(User(**data))
            User.objects.bulk_create(user_list)

        if options['client'] or options['all']:
            self.init_client()

        if options['contact'] or options['all']:
            self.init_contato()

        if options['end'] or options['all']:
            self.init_endereco()
        #
        if options['prod'] or options['all']:
            self.init_produtos()
