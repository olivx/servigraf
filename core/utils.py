import re

from django.core.paginator import PageNotAnInteger
from pure_pagination import Paginator


def is_cpf_or_cnpj(valor):
    # Remove caracteres invalidos do valor
    valor = re.findall('\d+', str(valor))
    valor = ''.join(valor)

    # Verifica se é um CPF
    if len(valor) == 11:
        return 'CPF'

    # Verifica  se é um  CNPJ
    elif len(valor) == 14:
        return 'CNPJ'

    else:
        return False


def valida_cpf_cnpj(valor):
    """Verifica se é CPF pi CNPJ"""
    valida = is_cpf_or_cnpj(valor)

    valor = re.findall('\d+', str(valor))
    valor = ''.join(valor)

    if valida == 'CPF':
        #  Retorna true para cpf válido
        return validar_cpf(valor);

    elif valida == 'CNPJ':
        # Retorna true para CNPJ válido
        return validar_cnpj(valor)
    # Não retorna nada
    else:
        return False


def formata_cpf_cnpj(valor):
    # O valor formatado
    formatado = False

    # Verifica se é CPF ou CNPJ
    valida = is_cpf_or_cnpj(valor)

    # Valida CPF
    if valida == 'CPF':
        if validar_cpf(valor):
            # Formata o CPF  ###.###.###-##
            formatado = '{0}.{1}.{2}-{3}'.format(valor[:3], valor[3:6], valor[6:9], valor[9:])


    # Valida CNPJ
    elif valida == 'CNPJ':
        if validar_cnpj(valor):
            #  Formata o CNPJ  ##.###.###/####-##
            formatado = '{0}.{1}.{2}/{3}-{4}'.format(valor[:2], valor[2:5], valor[5:8], valor[8:12], valor[12:])

    # Retorna o valor
    return formatado


def validar_cpf(cpf):
    cpf = ''.join(re.findall('\d+', str(cpf)))
    if (not cpf) or (len(cpf) < 11):
        return False

    # Pega apenas os 9 primeiros dígitos do CPF e gera os 2 dígitos que faltam
    inteiros = list(map(int, cpf))
    novo = inteiros[:9]
    while len(novo) < 11:
        r = sum([(len(novo) + 1 - i) * v for i, v in enumerate(novo)]) % 11

        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return cpf
    return False


def validar_cnpj(cnpj):
    cnpj = ''.join(re.findall('\d', str(cnpj)))
    if (not cnpj) or (len(cnpj) < 14):
        return False

    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = list(map(int, cnpj))
    novo = inteiros[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return cnpj
    return False


def paginator(request, object_list, por_page=5):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    pages = Paginator(object_list, por_page, request=request)
    objects_paginated  = pages.page(page)
    return objects_paginated