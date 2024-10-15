# teste_conexao.py

from database import connect_to_db

def teste():
    connection = connect_to_db()
    if connection:
        print("Conexão bem-sucedida!")
        connection.close()
    else:
        print("Falha na conexão.")

if __name__ == '__main__':
    teste()