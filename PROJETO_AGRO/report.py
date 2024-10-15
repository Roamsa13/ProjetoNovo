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