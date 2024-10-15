# data_validation.py

from datetime import datetime

def validar_string(valor, nome_campo):
    """
    Valida se o valor é uma string não vazia.
    
    :param valor: Valor a ser validado.
    :param nome_campo: Nome do campo para exibir mensagens de erro.
    :return: String validada ou None.
    """
    if isinstance(valor, str) and valor.strip() != '':
        return valor.strip()
    else:
        print(f"Valor inválido para {nome_campo}. Por favor, insira um texto válido.")
        return None

def validar_float(valor, nome_campo):
    """
    Valida se o valor pode ser convertido para float.
    
    :param valor: Valor a ser validado.
    :param nome_campo: Nome do campo para exibir mensagens de erro.
    :return: Float validado ou None.
    """
    try:
        valor_float = float(valor)
        if valor_float >= 0:
            return valor_float
        else:
            print(f"Valor inválido para {nome_campo}. Por favor, insira um número positivo.")
            return None
    except ValueError:
        print(f"Valor inválido para {nome_campo}. Por favor, insira um número válido.")
        return None

def validar_data(valor, nome_campo):
    """
    Valida se a data está no formato AAAA-MM-DD.
    
    :param valor: Valor a ser validado.
    :param nome_campo: Nome do campo para exibir mensagens de erro.
    :return: Objeto datetime ou None.
    """
    try:
        data = datetime.strptime(valor, '%Y-%m-%d')
        return data
    except ValueError:
        print(f"Formato de data inválido para {nome_campo}. Use AAAA-MM-DD.")
        return None