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