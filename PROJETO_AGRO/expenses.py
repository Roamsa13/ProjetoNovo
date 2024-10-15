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