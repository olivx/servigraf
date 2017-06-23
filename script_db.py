import os
import pymysql

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "servigraf.settings")
    import django

    django.setup()

    from core.models import Cliente

    def connect(query):
        """Conecta com banco de dados e devolve um cursor """
        con = pymysql.connect('localhost', 'root', 'root', 'grafica')
        cursor = con.cursor()
        cursor.execute(query)

        return cursor


    def init_client():
        """Faz o cursor.fetchall e o insert parao banco que estamo testando"""
        cursor = connect('select * from cliente')

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
            print(client_list)
        for data in client_list:
            Cliente.objects.create(razao_social=data['razao_social'],
                                   nome_fantasia=data['nome_fantasia'],
                                   documento=data['documento'],
                                   mensalista=data['mensalista'],
                                   ramo=data['ramo'],
                                   tipo=data['tipo'])

if __name__ == '__main__':
    init_client()
