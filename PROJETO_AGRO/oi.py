    # database.py

import cx_Oracle
import os

def connect_to_db():
    """
    Estabelece uma conexão com o banco de dados Oracle usando credenciais das variáveis de ambiente.
    
    :return: Objeto de conexão ou None em caso de erro.
    """
    try:
        connection = cx_Oracle.connect(
            user=os.getenv('RM559457'),        # Usuário obtido das variáveis de ambiente
            password=os.getenv('130801'),# Senha obtida das variáveis de ambiente
            dsn=os.getenv('oracle.fiap.com.br:1521/ORCL')           # DSN obtido das variáveis de ambiente
        )
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Erro ao conectar ao banco de dados: {error.message}")
        return None

def initialize_database(connection):
    """
    Inicializa o banco de dados criando as tabelas necessárias.
    
    :param connection: Objeto de conexão com o banco de dados Oracle.
    """
    try:
        cursor = connection.cursor()
        with open('initialize_db.sql', 'r') as f:
            sql_commands = f.read()
        cursor.execute(sql_commands)
        connection.commit()
        print("Banco de dados inicializado com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        cursor.close()

def execute_query(connection, query, params=None):
    """
    Executa uma consulta SQL no banco de dados Oracle.
    
    :param connection: Objeto de conexão com o banco de dados Oracle.
    :param query: String com a consulta SQL.
    :param params: Dicionário com os parâmetros da consulta (opcional).
    :return: Resultado da consulta ou None.
    """
    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return None
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Erro ao executar a consulta: {error.message}")
        return None
    finally:
        cursor.close()

        #####
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
####
# crop_management.py

from data_validation import validar_string, validar_float, validar_data
from database import connect_to_db
from datetime import datetime

def cadastrar_propriedade():
    """
    Cadastra uma nova propriedade no banco de dados Oracle.
    """
    nome_fazenda = input("Nome da fazenda: ")
    nome_fazenda = validar_string(nome_fazenda, "Nome da fazenda")
    if nome_fazenda is None:
        return

    localizacao = input("Localização (cidade/estado): ")
    localizacao = validar_string(localizacao, "Localização")
    if localizacao is None:
        return

    area_total = input("Área total (hectares): ")
    area_total = validar_float(area_total, "Área total")
    if area_total is None:
        return

    area_cultivada = input("Área cultivada (hectares): ")
    area_cultivada = validar_float(area_cultivada, "Área cultivada")
    if area_cultivada is None:
        return

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = """
                INSERT INTO propriedades (nome_fazenda, localizacao, area_total, area_cultivada)
                VALUES (:nome_fazenda, :localizacao, :area_total, :area_cultivada)
            """
            cursor.execute(sql, {
                'nome_fazenda': nome_fazenda,
                'localizacao': localizacao,
                'area_total': area_total,
                'area_cultivada': area_cultivada
            })
            connection.commit()
            print("Propriedade cadastrada com sucesso!")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Erro ao cadastrar propriedade: {error.message}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Não foi possível conectar ao banco de dados.")

def cadastrar_cultura():
    """
    Cadastra uma nova cultura associada a uma propriedade no banco de dados Oracle.
    """
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            # Listar propriedades disponíveis
            cursor.execute("SELECT id_propriedade, nome_fazenda FROM propriedades")
            propriedades = cursor.fetchall()
            if not propriedades:
                print("Nenhuma propriedade cadastrada. Cadastre uma propriedade primeiro.")
                return

            print("\nPropriedades disponíveis:")
            for prop in propriedades:
                print(f"ID: {prop[0]}, Nome: {prop[1]}")

            id_propriedade = input("Selecione o ID da propriedade: ")
            if not id_propriedade.isdigit():
                print("ID inválido.")
                return
            id_propriedade = int(id_propriedade)

            # Verificar se a propriedade existe
            cursor.execute("SELECT COUNT(*) FROM propriedades WHERE id_propriedade = :id", {'id': id_propriedade})
            count = cursor.fetchone()[0]
            if count == 0:
                print("ID de propriedade não encontrado.")
                return

            nome_cultura = input("Nome da cultura: ")
            nome_cultura = validar_string(nome_cultura, "Nome da cultura")
            if nome_cultura is None:
                return

            area_plantio = input("Área de plantio (hectares): ")
            area_plantio = validar_float(area_plantio, "Área de plantio")
            if area_plantio is None:
                return

            data_plantio = input("Data de plantio (AAAA-MM-DD): ")
            data_plantio = validar_data(data_plantio, "Data de plantio")
            if data_plantio is None:
                return

            estadio_desenvolvimento = input("Estágio de desenvolvimento: ")
            estadio_desenvolvimento = validar_string(estadio_desenvolvimento, "Estágio de desenvolvimento")
            if estadio_desenvolvimento is None:
                return

            sql = """
                INSERT INTO culturas (id_propriedade, nome_cultura, area_plantio, data_plantio, estadio_desenvolvimento)
                VALUES (:id_propriedade, :nome_cultura, :area_plantio, :data_plantio, :estadio_desenvolvimento)
            """
            cursor.execute(sql, {
                'id_propriedade': id_propriedade,
                'nome_cultura': nome_cultura,
                'area_plantio': area_plantio,
                'data_plantio': data_plantio,
                'estagio_desenvolvimento': estadio_desenvolvimento
            })
            connection.commit()
            print("Cultura cadastrada com sucesso!")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Erro ao cadastrar cultura: {error.message}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Não foi possível conectar ao banco de dados.")

        ###

        # climate.py

from data_validation import validar_string
from database import connect_to_db
import requests
import os
from datetime import datetime

def registrar_dados_climaticos():
    """
    Registra novos dados climáticos no banco de dados Oracle.
    """
    localizacao = input("Localização (cidade): ")
    localizacao = validar_string(localizacao, "Localização")
    if localizacao is None:
        return

    # Obter a chave de API das variáveis de ambiente
    api_key = os.getenv('92cfd369706cc347d8a6280dfb9f31e5')
    if not api_key:
        print("Chave de API não configurada. Defina a variável de ambiente OPENWEATHER_API_KEY.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={localizacao}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        dados = response.json()

        if dados.get('cod') != 200:
            print(f"Erro ao obter dados climáticos: {dados.get('message')}")
            return

        temperatura = dados['main']['temp']
        umidade = dados['main']['humidity']
        precipitacao = dados['rain']['1h'] if 'rain' in dados and '1h' in dados['rain'] else 0

    except Exception as e:
        print(f"Erro ao obter dados climáticos: {e}")
        return

    data_registro = datetime.now()

    # Calcular ETo (simplificado)
    eto = (0.408 * (temperatura + 17.8)) / (temperatura + 237.3)

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = """
                INSERT INTO dados_climaticos (data_registro, localizacao, temperatura, umidade, precipitacao, eto)
                VALUES (:data_registro, :localizacao, :temperatura, :umidade, :precipitacao, :eto)
            """
            cursor.execute(sql, {
                'data_registro': data_registro,
                'localizacao': localizacao,
                'temperatura': temperatura,
                'umidade': umidade,
                'precipitacao': precipitacao,
                'eto': eto
            })
            connection.commit()
            print("Dados climáticos registrados com sucesso!")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Erro ao registrar dados climáticos: {error.message}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Não foi possível conectar ao banco de dados.")
        ###
        # irrigation.py

from data_validation import validar_float
from database import connect_to_db
import cx_Oracle

def calcular_necessidade_irrigacao():
    """
    Calcula a necessidade hídrica de uma cultura específica.
    """
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            # Listar culturas disponíveis
            cursor.execute("""
                SELECT c.id_cultura, c.nome_cultura, p.localizacao
                FROM culturas c
                JOIN propriedades p ON c.id_propriedade = p.id_propriedade
            """)
            culturas = cursor.fetchall()
            if not culturas:
                print("Nenhuma cultura cadastrada. Cadastre uma cultura primeiro.")
                return

            print("\nCulturas disponíveis:")
            for cultura in culturas:
                print(f"ID: {cultura[0]}, Nome: {cultura[1]}, Localização: {cultura[2]}")

            id_cultura = input("Selecione o ID da cultura: ")
            if not id_cultura.isdigit():
                print("ID inválido.")
                return
            id_cultura = int(id_cultura)

            # Verificar se a cultura existe e obter a localização
            cursor.execute("""
                SELECT p.localizacao
                FROM culturas c
                JOIN propriedades p ON c.id_propriedade = p.id_propriedade
                WHERE c.id_cultura = :id_cultura
            """, {'id_cultura': id_cultura})
            result = cursor.fetchone()
            if not result:
                print("ID de cultura não encontrado.")
                return
            localizacao = result[0]

            # Obter os dados climáticos mais recentes para a localização
            cursor.execute("""
                SELECT eto
                FROM dados_climaticos
                WHERE localizacao = :localizacao
                ORDER BY data_registro DESC
            """, {'localizacao': localizacao})
            dados_climaticos = cursor.fetchone()
            if not dados_climaticos:
                print("Nenhum dado climático encontrado para esta localização.")
                return
            eto = dados_climaticos[0]

            # Obter o coeficiente da cultura (Kc)
            kc = input("Informe o coeficiente da cultura (Kc): ")
            kc = validar_float(kc, "Coeficiente da cultura")
            if kc is None:
                return

            # Calcular a necessidade hídrica
            necessidade_hidrica = eto * kc
            print(f"A necessidade hídrica é de {necessidade_hidrica:.2f} mm/dia.")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Erro ao calcular a necessidade de irrigação: {error.message}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Não foi possível conectar ao banco de dados.")
        ####
        # expenses.py

from data_validation import validar_float
from database import connect_to_db
from datetime import datetime
import cx_Oracle

def registrar_gastos():
    """
    Registra uma nova despesa no banco de dados Oracle.
    """
    consumo_agua = input("Consumo de água (m³): ")
    consumo_agua = validar_float(consumo_agua, "Consumo de água")
    if consumo_agua is None:
        return

    consumo_energia = input("Consumo de energia (kWh): ")
    consumo_energia = validar_float(consumo_energia, "Consumo de energia")
    if consumo_energia is None:
        return

    custo_agua = input("Custo da água (R$): ")
    custo_agua = validar_float(custo_agua, "Custo da água")
    if custo_agua is None:
        return

    custo_energia = input("Custo da energia (R$): ")
    custo_energia = validar_float(custo_energia, "Custo da energia")
    if custo_energia is None:
        return

    data_registro = datetime.now()

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = """
                INSERT INTO gastos (data_registro, consumo_agua, consumo_energia, custo_agua, custo_energia)
                VALUES (:data_registro, :consumo_agua, :consumo_energia, :custo_agua, :custo_energia)
            """
            cursor.execute(sql, {
                'data_registro': data_registro,
                'consumo_agua': consumo_agua,
                'consumo_energia': consumo_energia,
                'custo_agua': custo_agua,
                'custo_energia': custo_energia
            })
            connection.commit()
            print("Gastos registrados com sucesso!")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Erro ao registrar gastos: {error.message}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Não foi possível conectar ao banco de dados.")
####

# report.py

from database import connect_to_db
import cx_Oracle
from tabulate import tabulate

def gerar_relatorios():
    """
    Exibe o menu de geração de relatórios e chama a função correspondente.
    """
    while True:
        print("\n--- Gerar Relatórios ---")
        print("1. Relatório de Gastos")
        print("2. Relatório de Necessidade Hídrica")
        print("3. Voltar ao Menu Principal")

        opcao = input("Selecione uma opção: ")

        if opcao == '1':
            gerar_relatorio_gastos()
        elif opcao == '2':
            gerar_relatorio_necessidade_hidrica()
        elif opcao == '3':
            return
        else:
            print("Opção inválida.")

def gerar_relatorio_gastos():
    """
    Gera e exibe o relatório de gastos.
    """
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = """
                SELECT data_registro, consumo_agua, consumo_energia, custo_agua, custo_energia
                FROM gastos
                ORDER BY data_registro DESC
            """
            cursor.execute(sql)
            gastos = cursor.fetchall()
            if not gastos:
                print("Nenhum gasto registrado.")
                return

            # Preparar dados para exibição
            headers = ["Data de Registro", "Consumo de Água (m³)", "Consumo de Energia (kWh)", "Custo da Água (R$)", "Custo da Energia (R$)"]
            print("\n--- Relatório de Gastos ---")
            print(tabulate(gastos, headers=headers, tablefmt="grid"))
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Erro ao gerar relatório de gastos: {error.message}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Não foi possível conectar ao banco de dados.")

def gerar_relatorio_necessidade_hidrica():
    """
    Gera e exibe o relatório de necessidade hídrica.
    """
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            # Selecionar culturas e suas localizações
            sql_culturas = """
                SELECT c.nome_cultura, p.localizacao, d.eto
                FROM culturas c
                JOIN propriedades p ON c.id_propriedade = p.id_propriedade
                JOIN (
                    SELECT localizacao, eto, data_registro
                    FROM dados_climaticos
                    WHERE (localizacao, data_registro) IN (
                        SELECT localizacao, MAX(data_registro)
                        FROM dados_climaticos
                        GROUP BY localizacao
                    )
                ) d ON p.localizacao = d.localizacao
            """
            cursor.execute(sql_culturas)
            dados = cursor.fetchall()
            if not dados:
                print("Nenhum dado disponível para gerar o relatório de necessidade hídrica.")
                return

            # Preparar dados para exibição
            headers = ["Nome da Cultura", "Localização", "ETo"]
            print("\n--- Relatório de Necessidade Hídrica ---")
            print(tabulate(dados, headers=headers, tablefmt="grid"))
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Erro ao gerar relatório de necessidade hídrica: {error.message}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Não foi possível conectar ao banco de dados.")
        ####
        # main.py
# main.py

from database import connect_to_db
from data_validation import validar_string, validar_float, validar_data
import sys
import pandas as pd
from tabulate import tabulate

# Menu de Navegação
home = """
    ╔═══════╣ PROJETO AGRONEGÓCIO ╠═══════╗
    ║                                ║
    ║    1 -> Cadastrar Propriedade  ║
    ║    2 -> Cadastrar Cultura       ║
    ║    3 -> Registrar Dados Climáticos ║
    ║    4 -> Calcular Necessidade de Irrigação ║
    ║    5 -> Registrar Gastos        ║
    ║    6 -> Gerar Relatórios        ║
    ║    7 -> Sair                     ║
    ║                                ║
    ╚════════════════════════════════╝
"""

# Função para obter uma opção válida do menu
def obter_opcao_menu():
    while True:
        opcao = input("Escolha uma opção: ")
        if opcao.isdigit() and 1 <= int(opcao) <= 7:
            return int(opcao)
        else:
            print("Opção inválida. Por favor, insira um número entre 1 e 7.")

# Função para voltar ao menu
def voltar_menu():
    input("\nPressione Enter para voltar ao menu principal...")
    return

# Função para obter um número válido (float)
def obter_numero(mensagem):
    while True:
        valor = input(mensagem)
        try:
            numero = float(valor)
            if numero > 0:
                return numero
            else:
                print("Por favor, insira um número maior que zero.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

# Função para obter um número inteiro válido
def obter_inteiro(mensagem):
    while True:
        valor = input(mensagem)
        if valor.isdigit():
            return int(valor)
        else:
            print("Entrada inválida. Por favor, insira um número inteiro válido.")

# Função para obter a cultura válida
def obter_cultura():
    culturas_disponiveis = ['alface', 'tomate']
    while True:
        cultura = input("Digite o tipo de cultura (Alface/Tomate): ").strip().lower()
        if cultura in culturas_disponiveis:
            return cultura.capitalize()
        else:
            print("Opção inválida. Por favor, escolha entre 'Alface' ou 'Tomate'.")

# Função para formatar os nomes das colunas
def formatar_colunas(colunas):
    colunas_formatadas = []
    for coluna in colunas:
        coluna = coluna.replace('_', ' ').title()
        colunas_formatadas.append(coluna)
    return colunas_formatadas

# Função para cadastrar propriedade
def cadastrar_propriedade():
    nome_fazenda = input("Nome da fazenda: ")
    nome_fazenda = validar_string(nome_fazenda, "Nome da fazenda")
    if nome_fazenda is None:
        return

    localizacao = input("Localização (cidade/estado): ")
    localizacao = validar_string(localizacao, "Localização")
    if localizacao is None:
        return

    area_total = input("Área total (hectares): ")
    area_total = validar_float(area_total, "Área total")
    if area_total is None:
        return

    area_cultivada = input("Área cultivada (hectares): ")
    area_cultivada = validar_float(area_cultivada, "Área cultivada")
    if area_cultivada is None:
        return

    # Conectar ao banco de dados
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            sql = """
                INSERT INTO propriedades (nome_fazenda, localizacao, area_total, area_cultivada)
                VALUES (:nome_fazenda, :localizacao, :area_total, :area_cultivada)
            """
            cursor.execute(sql, {
                'nome_fazenda': nome_fazenda,
                'localizacao': localizacao,
                'area_total': area_total,
                'area_cultivada': area_cultivada
            })
            connection.commit()
            print("Propriedade cadastrada com sucesso!")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Erro ao inserir dados: {error.message}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Não foi possível conectar ao banco de dados.")
    voltar_menu()

# Função principal
def main():
    while True:
        print(home)
        opcao = obter_opcao_menu()

        if opcao == 1:
            cadastrar_propriedade()
        elif opcao == 2:
            # Implementar Cadastrar Cultura
            print("Funcionalidade ainda não implementada.")
            voltar_menu()
        elif opcao == 3:
            # Implementar Registrar Dados Climáticos
            print("Funcionalidade ainda não implementada.")
            voltar_menu()
        elif opcao == 4:
            # Implementar Calcular Necessidade de Irrigação
            print("Funcionalidade ainda não implementada.")
            voltar_menu()
        elif opcao == 5:
            # Implementar Registrar Gastos
            print("Funcionalidade ainda não implementada.")
            voltar_menu()
        elif opcao == 6:
            # Implementar Gerar Relatórios
            print("Funcionalidade ainda não implementada.")
            voltar_menu()
        elif opcao == 7:
            print("Saindo do programa.")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
