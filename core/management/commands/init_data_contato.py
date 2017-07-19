import pymysql
from django.core.management.base import BaseCommand

from core.models import Cliente, Contato


class Command(BaseCommand):
    def connect(self, query):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='grafica')
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor

    def init_contact(self):
        print('Varrendo Contatos')
        cursor = self.connect('select * from contato')

        columns = tuple([desc[0] for desc in cursor.description])
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        print('importando dados...')
        for row in rows:
            Contato.objects.create(
                nome=row['nome'],
                sobre_nome=row['sobrenome'],
                observacao=row['descricao'],
            )
        print('Contatos importado com sucesso!')


    def handle(self, *args, **options):
        self.init_contact()
