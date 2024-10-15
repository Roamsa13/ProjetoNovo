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