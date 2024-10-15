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