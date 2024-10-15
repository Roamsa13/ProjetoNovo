import oracledb
import os

def connect_to_db():
    oracledb.init_oracle_client(lib_dir=os.getenv('ORACLE_HOME'))

    connection = oracledb.connect(
        user=os.getenv('RM559457'),
        password=os.getenv('130801'),
        dsn=os.getenv('oracle.fiap.com.br:1521/ORCL')
    )
    return connection

if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        print("Conexão estabelecida com sucesso!")
    else:
        print("Falha na conexão.")
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
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Erro ao executar a consulta: {error.message}")
        return None
    finally:
        cursor.close()

if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        print("Conexão estabelecida com sucesso!")
        # Você pode chamar outras funções aqui, como initialize_database(conn)
        conn.close()
    else:
        print("Falha na conexão.")